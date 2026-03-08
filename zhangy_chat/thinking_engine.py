#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
思考决策引擎 - R3 思考式响应核心
需求拆解、逻辑推理、情绪共情、个性化适配
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime


class ThinkingEngine:
    """思考决策引擎"""

    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

        # 思考配置
        self.thinking_mode = True  # 是否开启思考模式
        self.thinking_depth = "mid"  # light/mid/heavy
        self.show_thinking_process = False  # 是否显示思考过程

        # 用户画像数据（用于个性化思考）
        self.user_profile = self._load_user_profile()

        # 思考历史记录（用于上下文分析）
        self.thinking_history = []

    def _load_user_profile(self) -> Dict:
        """加载用户画像"""
        profile_path = self.data_dir / "user_profile.json"
        if profile_path.exists():
            with open(profile_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "work_hours": {"start": 9, "end": 18},
            "peak_efficiency": [9, 10, 14, 15],  # 高效时段
            "task_completion_rate": 0.8,
            "procrastination_triggers": ["complex_task", "unclear_deadline"],
            "learning_style": "visual",
            "stress_level": "medium",
            "preferred_response_style": "concise"
        }

    def _save_user_profile(self):
        """保存用户画像"""
        profile_path = self.data_dir / "user_profile.json"
        with open(profile_path, 'w', encoding='utf-8') as f:
            json.dump(self.user_profile, f, ensure_ascii=False, indent=2)

    def think(self, query: str, context: Optional[Dict] = None) -> Dict:
        """
        思考流程 - 核心方法

        Args:
            query: 用户输入
            context: 上下文信息（情绪、历史对话等）

        Returns:
            思考结果字典
        """
        if not self.thinking_mode:
            return {"mode": "simple", "response_type": "direct"}

        # 1. 需求拆解
        needs_analysis = self._analyze_needs(query, context)

        # 2. 情绪识别
        emotion_analysis = self._analyze_emotion(query, context)

        # 3. 上下文关联
        context_relevance = self._analyze_context(query, context)

        # 4. 个性化适配
        personalization = self._personalize_response(needs_analysis, emotion_analysis)

        # 5. 生成思考结论
        thinking_result = {
            "mode": "thinking",
            "depth": self.thinking_depth,
            "needs": needs_analysis,
            "emotion": emotion_analysis,
            "context": context_relevance,
            "personalization": personalization,
            "suggested_response_style": self._suggest_response_style(personalization),
            "timestamp": datetime.now().isoformat()
        }

        # 记录思考历史
        self.thinking_history.append(thinking_result)
        if len(self.thinking_history) > 50:
            self.thinking_history = self.thinking_history[-50:]

        return thinking_result

    def _analyze_needs(self, query: str, context: Optional[Dict]) -> Dict:
        """需求拆解分析"""
        # 关键词匹配需求类型
        needs_types = {
            "task_management": ["任务", "待办", "计划", "安排", "提醒"],
            "goal_planning": ["目标", "规划", "想要", "希望", "打算"],
            "knowledge_query": ["怎么", "如何", "为什么", "什么", "哪些"],
            "emotional_support": ["烦", "累", "焦虑", "压力", "难过", "开心"],
            "decision_making": ["要不要", "该不该", "选哪个", "纠结"],
            "daily_chat": ["你好", "在吗", "哈哈", "谢谢"]
        }

        detected_needs = []
        for need_type, keywords in needs_types.items():
            if any(kw in query for kw in keywords):
                detected_needs.append(need_type)

        # 潜在需求推断
        potential_needs = self._infer_potential_needs(query, detected_needs)

        return {
            "explicit_needs": detected_needs,
            "potential_needs": potential_needs,
            "core_ask": self._extract_core_ask(query),
            "urgency": self._assess_urgency(query, context)
        }

    def _infer_potential_needs(self, query: str, detected_needs: List[str]) -> List[str]:
        """推断潜在需求"""
        potential = []

        # 基于用户画像推断
        if "task_management" in detected_needs:
            if self.user_profile.get("procrastination_triggers"):
                potential.append("may_need_task_breakdown")

        if "goal_planning" in detected_needs:
            if self.user_profile.get("peak_efficiency"):
                potential.append("may_need_time_allocation")

        if "emotional_support" in detected_needs:
            potential.append("needs_empathy_first")

        return potential

    def _extract_core_ask(self, query: str) -> str:
        """提取核心诉求"""
        # 简化版：移除语气词，保留核心内容
        core = query.strip()
        for word in ["请问", "帮我", "我想", "能不能", "可以吗"]:
            core = core.replace(word, "")
        return core.strip()[:50]

    def _assess_urgency(self, query: str, context: Optional[Dict]) -> str:
        """评估紧急程度"""
        urgent_keywords = ["急", "马上", "现在", "赶紧", "快点", "今天", "立刻"]
        if any(kw in query for kw in urgent_keywords):
            return "high"

        # 基于时间推断
        current_hour = datetime.now().hour
        work_hours = self.user_profile.get("work_hours", {})
        if work_hours.get("start", 9) <= current_hour <= work_hours.get("end", 18):
            return "medium"

        return "low"

    def _analyze_emotion(self, query: str, context: Optional[Dict]) -> Dict:
        """情绪识别分析"""
        emotion_keywords = {
            "anxious": ["焦虑", "担心", "害怕", "紧张", "慌"],
            "frustrated": ["烦", "郁闷", "沮丧", "失望", "心累"],
            "angry": ["生气", "愤怒", "火大", "憋屈"],
            "tired": ["累", "疲惫", "困", "熬不住"],
            "happy": ["开心", "高兴", "爽", "美滋滋"],
            "neutral": []
        }

        detected_emotion = "neutral"
        intensity = 1

        for emotion, keywords in emotion_keywords.items():
            for kw in keywords:
                if kw in query:
                    detected_emotion = emotion
                    intensity = 2
                    # 强度词检测
                    if any(s in query for s in ["特别", "非常", "超级", "太", "极了"]):
                        intensity = 3
                    break

        # 结合上下文情绪
        if context and context.get("recent_emotion"):
            if context["recent_emotion"] == detected_emotion:
                intensity += 1

        return {
            "emotion": detected_emotion,
            "intensity": min(intensity, 3),
            "needs_empathy": detected_emotion in ["anxious", "frustrated", "tired"],
            "suggested_tone": self._get_suggested_tone(detected_emotion)
        }

    def _get_suggested_tone(self, emotion: str) -> str:
        """建议回应语气"""
        tone_map = {
            "anxious": "gentle_comfort",
            "frustrated": "empathy_first",
            "angry": "validate_then_calm",
            "tired": "care_and_rest",
            "happy": "share_and_celebrate",
            "neutral": "professional"
        }
        return tone_map.get(emotion, "professional")

    def _analyze_context(self, query: str, context: Optional[Dict]) -> Dict:
        """上下文关联分析"""
        if not context:
            return {"has_context": False, "related_topics": []}

        related_topics = []

        # 检查与历史对话的关联
        if context.get("recent_topics"):
            for topic in context["recent_topics"]:
                if topic in query:
                    related_topics.append(topic)

        # 检查与任务/目标的关联
        if context.get("active_tasks"):
            for task in context["active_tasks"]:
                if task.get("title") in query:
                    related_topics.append(f"task:{task['title']}")

        return {
            "has_context": len(related_topics) > 0,
            "related_topics": related_topics,
            "context_depth": len(related_topics)
        }

    def _personalize_response(self, needs: Dict, emotion: Dict) -> Dict:
        """个性化适配"""
        return {
            "response_length": "short" if emotion["intensity"] >= 2 else "medium",
            "emoji_usage": False,  # Windows 兼容性
            "structure": "empathy_first" if emotion["needs_empathy"] else "solution_first",
            "detail_level": self.thinking_depth,
            "user_preference": self.user_profile.get("preferred_response_style", "concise")
        }

    def _suggest_response_style(self, personalization: Dict) -> Dict:
        """建议回应风格"""
        return {
            "start_with_empathy": personalization["structure"] == "empathy_first",
            "keep_concise": personalization["response_length"] == "short",
            "add_structure": personalization["detail_level"] in ["mid", "heavy"],
            "include_action_items": personalization["user_preference"] == "action_oriented"
        }

    def get_thinking_summary(self, thinking_result: Dict) -> str:
        """获取思考过程摘要（用于可视化）"""
        if not self.show_thinking_process:
            return ""

        summary_parts = []

        # 需求分析
        needs = thinking_result.get("needs", {})
        if needs.get("explicit_needs"):
            summary_parts.append(f"识别需求：{', '.join(needs['explicit_needs'])}")

        # 情绪识别
        emotion = thinking_result.get("emotion", {})
        if emotion.get("emotion") != "neutral":
            summary_parts.append(f"情绪状态：{emotion['emotion']} (强度{emotion['intensity']})")

        # 个性化建议
        if thinking_result.get("personalization", {}).get("structure") == "empathy_first":
            summary_parts.append("策略：先共情再解答")
        else:
            summary_parts.append("策略：直接解答")

        return " -> ".join(summary_parts)

    def set_thinking_mode(self, mode: bool):
        """设置思考模式开关"""
        self.thinking_mode = mode

    def set_thinking_depth(self, depth: str):
        """设置思考深度"""
        if depth in ["light", "mid", "heavy"]:
            self.thinking_depth = depth

    def update_user_profile(self, updates: Dict):
        """更新用户画像"""
        self.user_profile.update(updates)
        self._save_user_profile()

    def get_user_insights(self) -> Dict:
        """获取用户洞察（用于思考式建议）"""
        return {
            "peak_hours": self.user_profile.get("peak_efficiency", [9, 10]),
            "completion_rate": self.user_profile.get("task_completion_rate", 0.8),
            "procrastination_triggers": self.user_profile.get("procrastination_triggers", []),
            "stress_level": self.user_profile.get("stress_level", "medium"),
            "preferred_style": self.user_profile.get("preferred_response_style", "concise")
        }
