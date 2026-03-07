#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AI 助手核心模块 - 问答、情绪疏导、内容辅助
"""

import random
from typing import Optional, List, Dict
from datetime import datetime


class Assistant:
    """AI 助手类"""
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.name = self.config.get('personality', {}).get('name', 'zhangy')
        self.style = self.config.get('personality', {}).get('说话风格', [])
        
        # 情绪疏导话术库
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
    
    def chat(self, query: str) -> str:
        """通用对话"""
        # 检测情绪关键词
        emotion = self._detect_emotion(query)
        
        if emotion:
            return self._emotional_response(emotion, query)
        
        # 检测功能类型
        if self._is_task_related(query):
            return self._task_response(query)
        
        if self._is_content_help(query):
            return self._content_help(query)
        
        # 默认问答
        return self._qa_response(query)
    
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
        return f"""## 任务建议

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
        return f"""## {self.name} 分析

**问题**: {query}

### 解决方案

针对您的问题，建议如下：

1. **诊断分析**: 识别问题的关键因素
2. **执行方案**: 提供具体可操作的步骤
3. **验证方法**: 确保方案有效性

### 实施建议

请根据上述方案执行，如需进一步协助，请提供更多细节。

---
*{self.name} - 理性温柔，高效陪伴*
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
        return tips[day % len(tips)]
