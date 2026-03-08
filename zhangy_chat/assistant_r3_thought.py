#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AI 助手核心模块 - R3 思考可见版
思考过程可见，类似 MiniMind 的 CoT 展示
"""

import random
from typing import Optional, Dict
from datetime import datetime


class Assistant:
    """AI 助手类 (R3 思考可见版)"""

    def __init__(self, config: Optional[Dict] = None, 
                 mood_manager=None, preset_manager=None,
                 memory_manager=None):
        self.config = config or {}
        self.name = self.config.get('personality', {}).get('name', 'zhangy')
        
        # R3 管理器
        self.mood_manager = mood_manager
        self.preset_manager = preset_manager
        self.memory_manager = memory_manager
        
        # 思考过程记录
        self.thought_process = []
        
        # 超大全实用回复库
        self.practical_responses = self._init_practical_responses()
        
        # 简单对话库
        self.simple_queries = {
            "你叫什么": f"我叫 {self.name}，是你的专属 AI 助手～",
            "你是谁": f"我是 {self.name}，一个本地 AI 助手～",
            "你好": "你好呀！有什么我可以帮你的吗？",
            "早上好": "早上好！今天也要加油哦～",
            "谢谢": "不客气～有其他问题随时找我！",
            "再见": "再见！有需要随时叫我～",
        }

    def _init_practical_responses(self) -> Dict:
        """初始化实用回复库"""
        return {
            "饿": {
                "keywords": ["饿", "吃饭", "吃东西", "食堂", "外卖"],
                "response": """## 吃饭建议

**快速解决**:
- 点外卖：美团/饿了么
- 楼下快餐：10-15 元
- 泡面 + 蛋：5 分钟

想好吃啥了吗？"""
            },
            "编程": {
                "keywords": ["编程", "代码", "python", "写程序", "bug"],
                "response": """## 编程建议

**学习路线**:
- 入门：Python
- 前端：HTML/CSS/JS
- 后端：Java/Go/Node.js

具体遇到啥问题了？"""
            },
            "工作": {
                "keywords": ["工作", "上班", "辞职", "跳槽", "加班"],
                "response": """## 工作建议

**职场生存**:
- 少说话多做事
- 老板画饼听听就好
- 身体最重要

工作上遇到啥事了？"""
            },
            "学习": {
                "keywords": ["学习", "考试", "考研", "复习"],
                "response": """## 学习建议

**高效方法**:
- 番茄钟：25 分钟专注
- 费曼技巧：讲给别人听
- 错题本：定期复习

在准备啥考试？"""
            },
            "累": {
                "keywords": ["累", "辛苦", "疲惫", "熬夜"],
                "response": """## 休息建议

**快速恢复**:
- 小睡 20 分钟
- 洗个热水澡
- 听点轻音乐

最近太辛苦了吧～"""
            },
            "压力": {
                "keywords": ["压力", "焦虑", "担心", "崩溃"],
                "response": """## 减压建议

**即时缓解**:
- 深呼吸：4-7-8 呼吸法
- 出去走走
- 找人聊聊

你不是一个人，有需要随时找我～"""
            }
        }

    def chat(self, query: str, show_thought: bool = True) -> str:
        """
        通用对话 - 带思考过程
        
        Args:
            query: 用户问题
            show_thought: 是否显示思考过程
        """
        # 清空思考记录
        self.thought_process = []
        
        if show_thought:
            self.thought_process.append(" 思考中...")
        
        # 1. 简单对话直接回复
        simple_response = self._check_simple_query(query)
        if simple_response:
            if show_thought:
                self._record_thought("识别为简单对话", "直接回复")
            return self._format_response(simple_response, show_thought)
        
        # 2. 情感识别
        emotion = self._detect_emotion(query)
        if show_thought:
            self._record_thought("情感分析", f"识别到情绪：{emotion or '平静'}")
        
        # 3. 实用回复
        practical_response = self._check_practical_query(query)
        if practical_response:
            if show_thought:
                self._record_thought("匹配实用回复库", "找到相关建议")
            return self._format_response(practical_response, show_thought)
        
        # 4. 逻辑推理
        if show_thought:
            self._record_thought("问题分析", "未找到匹配回复，启动逻辑推理")
            self._record_thought("推理类型", self._analyze_question_type(query))
        
        response = self._default_response(query)
        return self._format_response(response, show_thought)

    def _record_thought(self, step: str, content: str):
        """记录思考步骤"""
        self.thought_process.append(f"  ├─ {step}: {content}")

    def _format_response(self, response: str, show_thought: bool) -> str:
        """格式化输出（带思考过程）"""
        if not show_thought or not self.thought_process:
            return response
        
        # 组装思考过程
        thought_output = "\n".join(self.thought_process)
        
        return f"""{thought_output}
  └─ [OK] 回答生成

---

{response}"""

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

    def _detect_emotion(self, query: str) -> Optional[str]:
        """检测情绪"""
        emotions = {
            "焦虑": ["焦虑", "担心", "害怕", "紧张"],
            "沮丧": ["沮丧", "失落", "灰心"],
            "生气": ["生气", "愤怒", "烦"],
            "疲惫": ["累", "疲惫", "困", "辛苦"],
            "压力": ["压力", "崩溃", "喘不过气"]
        }
        for emotion, keywords in emotions.items():
            if any(w in query for w in keywords):
                return emotion
        return None

    def _analyze_question_type(self, query: str) -> str:
        """分析问题类型"""
        if any(w in query for w in ["为什么", "为啥"]):
            return "因果推理"
        elif any(w in query for w in ["怎么", "如何"]):
            return "流程推理"
        elif any(w in query for w in ["要不要", "该不该"]):
            return "决策推理"
        else:
            return "一般性问题"

    def _default_response(self, query: str) -> str:
        """默认回复"""
        if len(query) < 5:
            return f"""## {self.name} 的分析

你提到「{query}」，能再多说点吗？

比如：
- 具体是什么情况？
- 遇到了什么问题？

说得越详细，我越能帮到你～"""

        return f"""## {self.name} 的分析

关于「{query}」，我给你一些建议：

**分析思路**:
1. 先明确核心问题
2. 找出关键因素
3. 逐一分析

**建议**:
- 从小事做起
- 多查资料
- 找人请教

具体到你的情况，可以多说点细节～"""

    def get_daily_tip(self) -> str:
        """每日小贴士"""
        tips = [
            "今天也要记得适当休息，效率比时长更重要。",
            "完成一个小任务也是进步，为自己点赞！",
            "遇到困难时，不妨换个角度思考问题。",
        ]
        return tips[datetime.now().weekday() % len(tips)]

    def set_mood_manager(self, mood_manager):
        self.mood_manager = mood_manager

    def set_preset_manager(self, preset_manager):
        self.preset_manager = preset_manager
