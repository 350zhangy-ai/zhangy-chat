#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AI 助手核心模块 - 问答、情绪疏导、内容辅助（R3 版本）
支持心情适配、预设联动、实用回复
"""

import random
from typing import Optional, List, Dict
from datetime import datetime


class Assistant:
    """AI 助手类"""

    def __init__(self, config: Optional[Dict] = None, 
                 mood_manager=None, preset_manager=None):
        self.config = config or {}
        self.name = self.config.get('personality', {}).get('name', 'zhangy')
        self.style = self.config.get('personality', {}).get('说话风格', [])
        
        # 心情管理器（可选）
        self.mood_manager = mood_manager
        
        # 预设管理器（可选）
        self.preset_manager = preset_manager

        # 实用回复库 - 针对常见问题给出具体答案
        self.practical_responses = {
            "视频": {
                "keywords": ["视频", "剪辑", "拍摄"],
                "response": """## 📹 视频制作建议

**快速上手方案**:

1. **手机拍摄**
   - 横屏拍摄（16:9）适合 YouTube/B 站
   - 竖屏拍摄（9:16）适合抖音/快手
   - 保持稳定，可用三脚架

2. **剪辑软件推荐**
   - 新手：剪映（手机/电脑版）- 免费、模板多
   - 进阶：Premiere Pro - 专业功能全
   - 免费替代：DaVinci Resolve - 调色强大

3. **内容结构**
   - 开头 3 秒抓住注意力
   - 中间内容有价值/有趣
   - 结尾引导点赞关注

**需要我帮你规划具体视频内容吗？**"""
            },
            "学习": {
                "keywords": ["学习", "考试", "复习", "备考"],
                "response": """## 📚 学习计划建议

**高效学习法**:

1. **番茄工作法**
   - 专注 25 分钟 + 休息 5 分钟
   - 4 个番茄后休息 15-30 分钟

2. **费曼学习法**
   - 选择概念 → 尝试讲解 → 发现盲点 → 重新学习

3. **复习节奏**
   - 当天复习（24 小时内）
   - 第 3 天复习
   - 第 7 天复习
   - 第 14 天复习

**需要我帮你制定具体学习计划吗？**"""
            },
            "工作": {
                "keywords": ["工作", "上班", "职场", "同事"],
                "response": """## 💼 工作效率建议

**提升效率方法**:

1. **任务优先级**
   - 紧急且重要 → 立即做
   - 重要不紧急 → 安排时间做
   - 紧急不重要 → 委托别人
   - 不紧急不重要 → 可以不做

2. **沟通技巧**
   - 邮件：主题清晰、内容简洁、行动明确
   - 会议：提前准备议程、控制时间、记录结论
   - 汇报：结论先行、数据支撑、方案备选

3. **时间管理**
   - 早上处理最难的任务
   - 下午处理常规工作
   - 批量处理邮件和消息

**有具体工作问题可以详细说说～**"""
            },
            "健康": {
                "keywords": ["健康", "运动", "减肥", "健身", "生病"],
                "response": """## 💚 健康建议

**日常保健**:

1. **运动建议**
   - 每周 150 分钟中等强度运动
   - 力量训练 2-3 次/周
   - 日常多走动，少久坐

2. **饮食建议**
   - 多吃蔬菜水果
   - 控制糖分摄入
   - 每天喝足够的水（1.5-2L）

3. **睡眠建议**
   - 保证 7-8 小时睡眠
   - 固定作息时间
   - 睡前 1 小时不用电子设备

*注：如有身体不适，请及时就医*"""
            },
            "旅行": {
                "keywords": ["旅行", "旅游", "出去玩", "景点"],
                "response": """## ✈️ 旅行规划建议

**出行准备**:

1. **目的地选择**
   - 确定预算和时间
   - 查天气和最佳季节
   - 了解当地文化和禁忌

2. **行程规划**
   - 不要排太满，留休息时间
   - 景点按区域分组，减少路途
   - 备选方案应对突发情况

3. **必备物品**
   - 证件：身份证/护照
   - 电子：充电器、转换插头
   - 药品：感冒药、肠胃药、创可贴

**想去哪里玩？我可以帮你细化行程～**"""
            },
            "购物": {
                "keywords": ["购物", "买", "推荐", "好物"],
                "response": """## 🛒 购物建议

**理性消费原则**:

1. **购买前三问**
   - 我真的需要吗？
   - 使用频率会高吗？
   - 有替代品吗？

2. **比价技巧**
   - 多平台对比价格
   - 关注促销节点（618、双 11）
   - 查看历史价格（用价格追踪工具）

3. **避坑指南**
   - 看差评而非好评
   - 注意退换货政策
   - 警惕"限时抢购"套路

**具体想买什么？可以帮你分析～**"""
            }
        }

        # 情绪疏导话术库（基础版）
        self.emotional_responses = {
            "anxiety": [
                "我理解你现在的感受。焦虑是正常的情绪反应，让我们一起深呼吸，慢慢分析问题。",
                "感到焦虑时，可以试试：1) 深呼吸 5 次 2) 把担忧写下来 3) 专注于当下能做的事",
                "你已经在努力了，这很棒。让我们把大问题拆成小步骤，一步一步来。"
            ],
            "frustrated": [
                "遇到挫折确实让人沮丧。不过你已经走了这么远，不妨休息一下再出发。",
                "挫折是成长的一部分。要不要先暂停一下，做些喜欢的事调整状态？",
                "我理解你的感受。有时候暂时放下问题，反而能找到新的解决思路。"
            ],
            "tired": [
                "辛苦了！适当的休息是为了更好地前进。要不要先放松一下？",
                "疲惫的时候，效率会下降。建议先休息，等状态恢复再继续。",
                "你已经做得很好了。记得照顾好自己，休息也是重要的任务。"
            ],
            "overwhelmed": [
                "事情太多时确实容易感到压力。让我们先列出优先级，一件一件来处理。",
                "深呼吸，你不需要一次性解决所有问题。先找出最重要的那件事。",
                "我理解这种被压得喘不过气的感觉。让我们先暂停，重新规划一下。"
            ]
        }

        # 内容辅助模板
        self.content_templates = {
            "polish": "## 润色建议\n\n**原文**: {text}\n\n**优化后**:\n{polished}\n\n**修改说明**:\n{notes}",
            "summary": "## 内容摘要\n\n**核心要点**:\n{points}\n\n**一句话总结**: {summary}",
            "outline": "## 大纲建议\n\n{outline}"
        }
    
    def _get_mood_prefix(self) -> str:
        """获取心情前缀"""
        if self.mood_manager:
            return self.mood_manager.get_response_prefix()
        return ""
    
    def _get_mood_suffix(self) -> str:
        """获取心情后缀"""
        if self.mood_manager:
            return self.mood_manager.get_response_suffix()
        return ""
    
    def _apply_mood_style(self, response: str) -> str:
        """应用心情风格到回复"""
        if not self.mood_manager:
            return response
        
        prefix = self._get_mood_prefix()
        suffix = self._get_mood_suffix()
        
        # 如果是效率模式，精简回复
        if self.mood_manager.is_efficiency_mode():
            # 移除冗余内容
            response = response.split('\n\n---\n')[0]
        
        # 组装回复
        parts = []
        if prefix:
            parts.append(prefix)
        parts.append(response)
        if suffix:
            parts.append(suffix)
        
        return "\n\n".join(parts)

    def chat(self, query: str) -> str:
        """通用对话"""
        # 1. 先检查简单对话
        simple_response = self._check_simple_query(query)
        if simple_response:
            return self._apply_mood_style(simple_response)
        
        # 2. 检测情绪关键词
        emotion = self._detect_emotion(query)
        if emotion:
            response = self._emotional_response(emotion, query)
            return self._apply_mood_style(response)

        # 3. 检查实用回复库
        practical_response = self._check_practical_query(query)
        if practical_response:
            return self._apply_mood_style(practical_response)

        # 4. 检查功能类型
        if self._is_task_related(query):
            response = self._task_response(query)
            return self._apply_mood_style(response)

        if self._is_content_help(query):
            response = self._content_help(query)
            return self._apply_mood_style(response)

        # 5. 默认问答
        response = self._qa_response(query)
        return self._apply_mood_style(response)
    
    def _check_simple_query(self, query: str) -> Optional[str]:
        """检查简单对话"""
        simple_queries = {
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
            "无聊": "无聊的话，可以看看书、运动一下，或者跟我聊聊天呀～",
            "开心": "开心就好！保持好心情～",
            "难过": "怎么了？想聊聊吗？我在这里陪着你。"
        }
        
        for key, response in simple_queries.items():
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

    def _detect_emotion(self, text: str) -> Optional[str]:
        """检测情绪"""
        anxiety_words = ['焦虑', '担心', '害怕', '紧张', '不安', '慌']
        frustrated_words = ['沮丧', '挫败', '失望', '灰心', '郁闷', '烦']
        tired_words = ['累', '疲惫', '疲倦', '困', '辛苦', '乏力']
        overwhelmed_words = ['压力大', '喘不过气', '太多事', '应付不来', '崩溃']

        if any(w in text for w in anxiety_words):
            return "anxiety"
        if any(w in text for w in frustrated_words):
            return "frustrated"
        if any(w in text for w in tired_words):
            return "tired"
        if any(w in text for w in overwhelmed_words):
            return "overwhelmed"
        return None

    def _emotional_response(self, emotion: str, query: str) -> str:
        """情绪疏导回复"""
        responses = self.emotional_responses.get(emotion, [])
        base_response = random.choice(responses) if responses else "我理解你的感受，想和我多聊聊吗？"
        
        # 如果心情管理器处于共情模式，增强共情回复
        if self.mood_manager and self.mood_manager.is_empathetic_mode():
            return f"""## {self.name} 想说

{base_response}

我在这里陪着你，有什么想说的都可以告诉我。
"""
        
        return f"""## {self.name} 想说

{base_response}

---
*如果你需要具体建议，可以告诉我更多细节*
"""

    def _is_task_related(self, query: str) -> bool:
        """判断是否与任务相关"""
        task_keywords = ['任务', '待办', '计划', '安排', '提醒', '目标', '习惯']
        return any(k in query for k in task_keywords)

    def _task_response(self, query: str) -> str:
        """任务相关回复"""
        # 根据预设调整回复
        if self.preset_manager and self.preset_manager.is_focus_mode():
            return """## 任务建议

1. **明确优先级**: 区分重要紧急程度
2. **拆解大任务**: 分解为小步骤
3. **设置截止时间**: 合理期限
4. **定期复盘**: 回顾调整

使用 `/add` 添加任务，`/review` 生成复盘。
"""
        
        return """## 任务建议

关于任务管理，建议如下：

1. **明确优先级**: 区分重要紧急程度
2. **拆解大任务**: 将复杂任务分解为小步骤
3. **设置截止时间**: 给每个任务设定合理期限
4. **定期复盘**: 回顾完成情况，调整计划

---
*你可以使用 /add 指令添加任务，/review 生成复盘报告*
"""

    def _is_content_help(self, query: str) -> bool:
        """判断是否需要内容辅助"""
        content_keywords = ['润色', '修改', '优化', '总结', '摘要', '大纲', '整理']
        return any(k in query for k in content_keywords)

    def _content_help(self, query: str) -> str:
        """内容辅助回复"""
        if '润色' in query or '修改' in query or '优化' in query:
            return self._polish_help(query)
        if '总结' in query or '摘要' in query:
            return self._summary_help(query)
        if '大纲' in query:
            return self._outline_help(query)

        return "我可以帮你润色内容、生成摘要、制定大纲等。请提供具体内容或说明需求。"

    def _polish_help(self, query: str) -> str:
        """润色帮助"""
        return """## 内容润色

请提供需要润色的文本，我可以帮你：

1. **优化表达**: 使语言更流畅自然
2. **调整语气**: 适配不同场景（正式/ casual）
3. **修正语法**: 检查并修正语法错误
4. **提升逻辑**: 优化段落结构和逻辑连贯

---
*请直接发送需要润色的内容*
"""

    def _summary_help(self, query: str) -> str:
        """摘要帮助"""
        return """## 内容摘要

请提供需要总结的文本，我可以帮你：

1. **提取要点**: 梳理核心信息
2. **生成摘要**: 输出简洁概述
3. **一句话总结**: 提炼最关键信息

---
*请直接发送需要总结的内容*
"""

    def _outline_help(self, query: str) -> str:
        """大纲帮助"""
        return """## 大纲制定

请告诉我主题或内容方向，我可以帮你：

1. **文章大纲**: 结构化框架
2. **演讲大纲**: 逻辑清晰的演讲框架
3. **项目大纲**: 项目规划要点
4. **学习大纲**: 知识点梳理

---
*请说明主题和用途*
"""

    def _qa_response(self, query: str) -> str:
        """默认问答回复"""
        # 如果问题太短，尝试给出通用建议
        if len(query) < 5:
            return f"""## {self.name} 的分析

你问的是「{query}」，能再多说点细节吗？

比如：
- 具体是什么场景？
- 遇到了什么问题？
- 想要达到什么目的？

这样我能给你更有针对性的建议～
"""
        
        return f"""## {self.name} 分析

**问题**: {query}

这个问题涉及到一些具体情况，我需要更多信息才能给出有针对性的建议。

**可以告诉我更多细节吗？**
- 具体是什么场景？
- 遇到了什么困难？
- 已经尝试过哪些方法？

了解得越详细，我的建议会越实用～
"""

    def get_daily_tip(self) -> str:
        """获取每日小贴士"""
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
        
        # 根据心情调整小贴士
        if self.mood_manager:
            if self.mood_manager.is_empathetic_mode():
                return f"💚 {base_tip} 记得，你已经很好了。"
            elif self.mood_manager.is_efficiency_mode():
                return f"🎯 {base_tip} 保持专注，继续前进。"
            elif self.mood_manager.is_casual_mode():
                return f"😊 {base_tip} 享受当下～"
        
        return f"📌 {base_tip}"
    
    def set_mood_manager(self, mood_manager):
        """设置心情管理器"""
        self.mood_manager = mood_manager
    
    def set_preset_manager(self, preset_manager):
        """设置预设管理器"""
        self.preset_manager = preset_manager
