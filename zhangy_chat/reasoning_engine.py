#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
推理引擎 - 轻量级思维链推理
参考 DeepSeek-R1 的推理理念，适配本地轻量级场景
"""

from typing import Dict, List, Optional


class ReasoningEngine:
    """推理引擎（轻量版）"""
    
    def __init__(self):
        # 推理模式配置
        self.reasoning_config = {
            "enable_step_by_step": True,  # 启用分步推理
            "enable_self_check": True,    # 启用自我检查
            "max_steps": 5                # 最大推理步骤
        }
    
    def reason(self, query: str) -> Dict:
        """
        对问题进行分步推理
        
        返回格式:
        {
            "reasoning_steps": [...],  # 推理步骤
            "conclusion": "...",       # 结论
            "confidence": 0.8          # 置信度
        }
        """
        # 1. 分析问题类型
        analysis = self._analyze_query(query)
        
        # 2. 分步推理
        steps = self._step_by_step_reasoning(query, analysis)
        
        # 3. 自我检查
        checked_steps = self._self_check(steps) if self.reasoning_config["enable_self_check"] else steps
        
        # 4. 得出结论
        conclusion = self._draw_conclusion(checked_steps, analysis)
        
        return {
            "reasoning_steps": checked_steps,
            "conclusion": conclusion,
            "analysis": analysis
        }
    
    def _analyze_query(self, query: str) -> Dict:
        """分析问题类型和核心诉求"""
        analysis = {
            "type": "general",
            "keywords": [],
            "core_ask": "",
            "context": {}
        }
        
        # 问题类型识别
        if any(w in query for w in ["为什么", "为啥", "何以"]):
            analysis["type"] = "why"
            analysis["core_ask"] = "原因分析"
        elif any(w in query for w in ["怎么", "如何", "怎样"]):
            analysis["type"] = "how"
            analysis["core_ask"] = "方法建议"
        elif any(w in query for w in ["要不要", "该不该", "是否"]):
            analysis["type"] = "whether"
            analysis["core_ask"] = "决策建议"
        elif any(w in query for w in ["哪个", "什么", "哪些"]):
            analysis["type"] = "what"
            analysis["core_ask"] = "信息/选择"
        
        # 提取关键词
        analysis["keywords"] = self._extract_keywords(query)
        
        return analysis
    
    def _extract_keywords(self, query: str) -> List[str]:
        """提取关键词"""
        # 简化版关键词提取
        stop_words = ["的", "了", "是", "在", "我", "有", "和", "就", "不", "你", "这", "那", "吗", "呢", "啊", "呀", "吧"]
        words = []
        for char in query:
            if char not in stop_words and char.isalnum():
                words.append(char)
        
        # 返回有意义的词组（简化处理）
        return list(set(query.replace(" ", "")))[:5]
    
    def _step_by_step_reasoning(self, query: str, analysis: Dict) -> List[str]:
        """分步推理"""
        steps = []
        
        if analysis["type"] == "why":
            steps = self._reason_why(query, analysis)
        elif analysis["type"] == "how":
            steps = self._reason_how(query, analysis)
        elif analysis["type"] == "whether":
            steps = self._reason_whether(query, analysis)
        else:
            steps = self._reason_general(query, analysis)
        
        return steps[:self.reasoning_config["max_steps"]]
    
    def _reason_why(self, query: str, analysis: Dict) -> List[str]:
        """因果推理"""
        return [
            "第一步：识别问题中的因果关系",
            "第二步：分析可能的原因（内因/外因）",
            "第三步：评估每个原因的可能性",
            "第四步：找出主要原因和次要原因",
            "第五步：总结因果链条"
        ]
    
    def _reason_how(self, query: str, analysis: Dict) -> List[str]:
        """流程推理"""
        return [
            "第一步：明确目标和期望结果",
            "第二步：列出必要的条件和资源",
            "第三步：拆解为可执行的步骤",
            "第四步：评估每个步骤的可行性",
            "第五步：给出行动建议"
        ]
    
    def _reason_whether(self, query: str, analysis: Dict) -> List[str]:
        """决策推理"""
        return [
            "第一步：明确决策的核心诉求",
            "第二步：列出所有可选方案",
            "第三步：分析每个方案的利弊",
            "第四步：评估风险和收益",
            "第五步：给出决策建议"
        ]
    
    def _reason_general(self, query: str, analysis: Dict) -> List[str]:
        """一般推理"""
        return [
            "第一步：理解问题的核心",
            "第二步：分析相关因素",
            "第三步：梳理因素间的关系",
            "第四步：得出初步结论",
            "第五步：验证结论的合理性"
        ]
    
    def _self_check(self, steps: List[str]) -> List[str]:
        """自我检查 - 优化推理步骤"""
        checked = []
        for i, step in enumerate(steps):
            # 添加检查标记
            checked.append(f"[思考] {step}")
        return checked
    
    def _draw_conclusion(self, steps: List[str], analysis: Dict) -> str:
        """得出结论"""
        if analysis["type"] == "why":
            return "综上所述，这个问题的原因需要从多个维度分析，我建议你先从最主要的因素入手。"
        elif analysis["type"] == "how":
            return "综上所述，按照上述步骤行动，可以逐步达到目标。关键是第一步要迈出去。"
        elif analysis["type"] == "whether":
            return "综上所述，建议权衡利弊后做出选择，没有完美的决定，只有当下最适合的。"
        else:
            return "综上所述，这个问题需要结合具体情况分析，建议你再补充一些细节。"
    
    def format_reasoning(self, result: Dict) -> str:
        """格式化推理过程输出"""
        output = []
        output.append("## 推理过程\n")
        
        for i, step in enumerate(result["reasoning_steps"], 1):
            output.append(f"**步骤{i}**: {step}")
        
        output.append(f"\n## 结论\n{result['conclusion']}")
        
        return "\n\n".join(output)
