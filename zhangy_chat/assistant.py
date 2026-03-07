#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AI 助手核心模块 - R4 深度智能版
集成逻辑推理引擎 + 情感计算引擎
"""

from typing import Optional, Dict
from .logic_engine import LogicEngine
from .emotion_engine import EmotionEngine


class Assistant:
    """AI 助手类 (R4 - 深度智能版)"""

    def __init__(self, config: Optional[Dict] = None, 
                 mood_manager=None, preset_manager=None,
                 memory_manager=None):
        self.config = config or {}
        self.name = self.config.get('personality', {}).get('name', 'zhangy')
        
        # 原有管理器
        self.mood_manager = mood_manager
        self.preset_manager = preset_manager
        self.memory_manager = memory_manager
        
        # R4 新增引擎
        self.logic_engine = LogicEngine()
        self.emotion_engine = EmotionEngine()
        
        # 简单对话库
        self.simple_queries = {
            "你叫什么": f"我叫 {self.name}，是你的专属 AI 助手～",
            "你是谁": f"我是 {self.name}，一个本地 AI 助手，可以帮你管理任务、规划目标、聊天解闷～",
            "你好": "你好呀！有什么我可以帮你的吗？",
            "早上好": "早上好！今天也要加油哦～",
            "中午好": "中午好！吃饭了吗？记得休息一下～",
            "晚上好": "晚上好！忙了一天辛苦啦，记得早点休息～",
            "谢谢": "不客气～有其他问题随时找我！",
            "再见": "再见！有需要随时叫我～",
            "在吗": "在的在的～有什么可以帮你的？",
            "帮个忙": "没问题，说吧，什么事？",
            "哈哈": "开心就好～",
            "嗯": "嗯嗯，我在听～",
            "哦": "怎么了？有啥事吗？",
        }
        
        # 实用回复库（保留 R3 功能）
        self.practical_responses = {
            "饿": {
                "keywords": ["饿", "吃饭", "吃东西", "肚子", "食堂", "外卖", "做饭"],
                "response": """## 🍚 吃饭建议

**快速解决**:
- 点外卖：美团/饿了么，30 分钟送到
- 楼下快餐：10-15 元搞定
- 泡面 + 蛋：5 分钟，加根火腿更香

**健康选择**:
- 自己做饭：少油少盐，营养均衡
- 沙拉 + 鸡胸：减脂期首选
- 杂粮饭 + 蔬菜：饱腹感强

想好吃啥了吗？没的话我可以帮你推荐～"""
            },
            "累": {
                "keywords": ["累", "辛苦", "困", "乏", "疲惫"],
                "response": """## 😴 累了就休息休息

**快速恢复**:
- 小睡 20 分钟
- 洗个热水澡
- 听点轻音乐
- 出去走走

**长期调节**:
- 保证睡眠，别熬夜
- 适当运动，出出汗
- 周末彻底放松一天

最近是不是太辛苦了？好好休息休息吧～"""
            }
        }

    def chat(self, query: str) -> str:
        """
        通用对话 - R4 智能处理流程
        
        流程：简单对话 → 情感识别 → 逻辑推理 → 实用回复 → 默认回复
        """
        # 1. 简单对话直接回复
        simple_response = self._check_simple_query(query)
        if simple_response:
            return self._apply_emotion_style(simple_response)
        
        # 2. 情感识别（核心升级）
        emotion_result = self.emotion_engine.recognize(query)
        
        # 3. 逻辑推理（核心升级）
        logic_result = self.logic_engine.analyze(query, {
            "emotion": emotion_result["emotion"],
            "intensity": emotion_result["intensity"]
        })
        
        # 4. 检查是否有实用回复
        practical_response = self._check_practical_query(query)
        if practical_response:
            return self._apply_emotion_style(practical_response)
        
        # 5. 整合逻辑推理和情感回应
        return self._integrate_response(logic_result, emotion_result, query)
    
    def _check_simple_query(self, query: str) -> Optional[str]:
        """检查简单对话"""
        for key, response in self.simple_queries.items():
            if key in query:
                return response
        return None
    
    def _check_practical_query(self, query: str) -> Optional[str]:
        """检查实用回复库"""
        for category, data in self.practical_responses.items():
            for keyword in data["keywords"]:
                if keyword in query:
                    return data["response"]
        return None
    
    def _integrate_response(self, logic_result: Dict, emotion_result: Dict, 
                           original_query: str) -> str:
        """
        整合逻辑推理和情感回应
        
        策略：
        - 负面情绪：先共情，再解答
        - 正面情绪：先共鸣，再解答
        - 中性情绪：直接解答，适度关怀
        """
        emotion = emotion_result["emotion"]
        intensity = emotion_result["intensity"]
        logic_content = logic_result.get("content", "")
        
        # 判断是否需要情感回应
        if not self.emotion_engine.should_adjust_response(logic_content):
            return logic_content
        
        # 获取情感回应
        emotion_response = self.emotion_engine.respond(
            emotion, original_query, logic_content
        )
        
        # 整合策略
        if emotion in ["anxiety", "frustrated", "angry", "tired", "overwhelmed", "lonely"]:
            # 负面情绪：先共情，再解答
            return f"""{emotion_response}

---

**关于你说的这件事**，我来帮你分析一下：

{logic_content}"""
        
        elif emotion in ["happy", "proud"]:
            # 正面情绪：先共鸣，再轻量回应
            return f"""{emotion_response}

{logic_content}"""
        
        else:
            # 中性：直接解答
            return logic_content
    
    def _apply_emotion_style(self, response: str) -> str:
        """根据心情管理器调整风格（保留 R3 兼容）"""
        if self.mood_manager:
            prefix = self.mood_manager.get_response_prefix()
            suffix = self.mood_manager.get_response_suffix()
            
            if self.mood_manager.is_efficiency_mode():
                response = response.split('\n\n---\n')[0]
            
            parts = []
            if prefix:
                parts.append(prefix)
            parts.append(response)
            if suffix:
                parts.append(suffix)
            
            return "\n\n".join(parts)
        
        return response
    
    # R4 新增方法：逻辑推理专用
    def logic_chat(self, query: str) -> str:
        """
        纯逻辑推理模式（用于 /logic 指令）
        """
        result = self.logic_engine.analyze(query)
        return result.get("content", "这个问题我需要更多信息才能分析。")
    
    # R4 新增方法：情感管理
    def get_emotion_status(self) -> str:
        """获取当前情感状态"""
        return self.emotion_engine.get_emotion_summary()
    
    def clear_emotion_memory(self) -> str:
        """清除情感记忆"""
        return self.emotion_engine.clear_memory()
    
    def set_emotion_intensity(self, level: str) -> bool:
        """设置情感强度"""
        return self.emotion_engine.set_intensity_level(level)
    
    # 保留 R3 方法
    def get_daily_tip(self) -> str:
        """获取每日小贴士"""
        from datetime import datetime
        tips = [
            "今天也要记得适当休息，效率比时长更重要。",
            "完成一个小任务也是进步，为自己点赞！",
            "遇到困难时，不妨换个角度思考问题。",
            "今天的努力，是明天成功的基石。",
            "照顾好自己，才能更好地照顾他人。",
            "专注当下，不要为未发生的事过度担忧。",
            "适当的运动可以提升心情和效率。"
        ]
        day = datetime.now().weekday()
        base_tip = tips[day % len(tips)]
        
        if self.mood_manager:
            if self.mood_manager.is_empathetic_mode():
                return f"💚 {base_tip} 记得，你已经很好了。"
            elif self.mood_manager.is_efficiency_mode():
                return f"🎯 {base_tip} 保持专注，继续前进。"
        
        return f"📌 {base_tip}"
    
    def set_mood_manager(self, mood_manager):
        self.mood_manager = mood_manager
    
    def set_preset_manager(self, preset_manager):
        self.preset_manager = preset_manager
