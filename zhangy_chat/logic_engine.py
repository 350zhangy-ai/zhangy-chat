#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
逻辑推理引擎 - 智能问答核心
语义解析 → 逻辑推理 → 情境适配 → 答案生成
"""

import re
from typing import Dict, List, Optional, Tuple
from datetime import datetime


class LogicEngine:
    """逻辑推理引擎"""
    
    def __init__(self):
        # 问题类型映射
        self.question_patterns = {
            "why": {
                "patterns": ["为什么", "为啥", "何以", "为何"],
                "type": "causal"  # 因果推理
            },
            "how": {
                "patterns": ["怎么", "如何", "怎样", "咋"],
                "type": "procedural"  # 流程推理
            },
            "what": {
                "patterns": ["什么", "啥", "哪些", "哪个"],
                "type": "definitional"  # 定义/选择推理
            },
            "whether": {
                "patterns": ["要不要", "能不能", "该不该", "是否", "好吗"],
                "type": "decisional"  # 决策推理
            },
            "compare": {
                "patterns": ["哪个更好", "有什么区别", "对比", "vs"],
                "type": "comparative"  # 比较推理
            }
        }
        
        # 常见问题的逻辑模板
        self.logic_templates = {
            "加班效率": {
                "keywords": ["加班", "效率", "越久越低"],
                "logic_chain": [
                    "注意力是有限资源，长时间工作会消耗",
                    "大脑疲劳后，单位时间产出下降",
                    "熬夜加班影响第二天状态，形成恶性循环"
                ],
                "conclusion": "所以不是工作时间越长越好，而是要在高效时段做重要的事"
            },
            "坚持困难": {
                "keywords": ["坚持", "很难", "放弃", "做不到"],
                "logic_chain": [
                    "坚持需要持续的意志力和正向反馈",
                    "目标太大或太远时，短期看不到回报容易动摇",
                    "环境诱惑和即时满足会不断消耗决心"
                ],
                "conclusion": "所以坚持不是靠硬撑，而是把大目标拆成小步骤，让自己不断看到进展"
            },
            "努力没回报": {
                "keywords": ["努力", "没回报", "没效果", "白努力"],
                "logic_chain": [
                    "努力的方向可能和目标不匹配",
                    "回报有延迟，可能还没到显现的时候",
                    "努力的方式可能不够高效，需要调整方法"
                ],
                "conclusion": "所以不是努力没用，而是需要检查方向、方法和时间三个维度"
            },
            "拖延": {
                "keywords": ["拖延", "不想动", "懒得", "等会再说"],
                "logic_chain": [
                    "拖延往往不是因为懒，而是任务太难或太模糊",
                    "大脑天然抗拒不确定性和高难度",
                    "越拖越焦虑，越焦虑越不想开始"
                ],
                "conclusion": "所以破解拖延不是靠自责，而是把任务拆到最小可执行步骤，先做 5 分钟再说"
            },
            "选择困难": {
                "keywords": ["纠结", "选哪个", "不知道选啥", "选择困难"],
                "logic_chain": [
                    "选择困难往往是因为想同时满足所有条件",
                    "但任何选择都有机会成本，得到一些就会失去另一些",
                    "没有完美的选择，只有当下最适合的"
                ],
                "conclusion": "所以先明确自己最在意的是什么，然后接受其他方面的不完美"
            }
        }
    
    def analyze(self, query: str, context: Optional[Dict] = None) -> Dict:
        """
        分析问题并生成回答
        
        Args:
            query: 用户问题
            context: 上下文信息（情绪、身份等）
            
        Returns:
            包含推理结果的字典
        """
        # 1. 语义解析 - 识别问题类型
        question_type = self._parse_question_type(query)
        
        # 2. 检查是否有预设逻辑模板
        template_match = self._match_template(query)
        
        if template_match:
            return self._generate_from_template(query, template_match, context)
        
        # 3. 根据问题类型进行逻辑推理
        return self._reason_by_type(query, question_type, context)
    
    def _parse_question_type(self, query: str) -> str:
        """解析问题类型"""
        for q_type, info in self.question_patterns.items():
            if any(pattern in query for pattern in info["patterns"]):
                return info["type"]
        return "general"  # 一般性问题
    
    def _match_template(self, query: str) -> Optional[Dict]:
        """匹配预设逻辑模板"""
        for name, template in self.logic_templates.items():
            if any(keyword in query for keyword in template["keywords"]):
                return template
        return None
    
    def _generate_from_template(self, query: str, template: Dict, 
                                 context: Optional[Dict] = None) -> Dict:
        """从模板生成回答"""
        logic_chain = template["logic_chain"]
        conclusion = template["conclusion"]
        
        # 根据情境调整表述
        if context and context.get("emotion") in ["anxiety", "frustrated"]:
            # 情绪低落时，语气更温和
            prefix = "我理解你的感受，这个问题其实很多人都会遇到。\n\n"
            logic_prefix = "我们来一起分析一下：\n"
            conclusion_prefix = "所以啊，"
        else:
            prefix = ""
            logic_prefix = ""
            conclusion_prefix = "所以"
        
        return {
            "type": "logic_reasoning",
            "content": f"""{prefix}{logic_prefix}{''.join([f'{i+1}. {point}\n' for i, point in enumerate(logic_chain)])}\n{conclusion_prefix}{conclusion}""",
            "logic_chain": logic_chain,
            "conclusion": conclusion
        }
    
    def _reason_by_type(self, query: str, question_type: str, 
                        context: Optional[Dict] = None) -> Dict:
        """根据问题类型进行推理"""
        
        if question_type == "causal":
            return self._causal_reasoning(query, context)
        elif question_type == "procedural":
            return self._procedural_reasoning(query, context)
        elif question_type == "decisional":
            return self._decisional_reasoning(query, context)
        elif question_type == "comparative":
            return self._comparative_reasoning(query, context)
        else:
            return self._general_reasoning(query, context)
    
    def _causal_reasoning(self, query: str, context: Optional[Dict] = None) -> Dict:
        """因果推理 - 回答'为什么'类问题"""
        # 提取核心主题
        topic = self._extract_topic(query)
        
        reasoning = f"""关于「{topic}」，我来帮你分析一下背后的原因：

**可能的原因**:
1. 从规律来看，任何事情都有其内在逻辑
2. 需要结合具体情境来分析
3. 可能有多重因素共同作用

**建议思路**:
- 先明确具体是什么情况
- 找出关键影响因素
- 逐一分析每个因素的作用

你能再多说点具体情境吗？这样我能分析得更准确～"""

        return {
            "type": "causal_reasoning",
            "content": reasoning,
            "topic": topic
        }
    
    def _procedural_reasoning(self, query: str, context: Optional[Dict] = None) -> Dict:
        """流程推理 - 回答'怎么做'类问题"""
        topic = self._extract_topic(query)
        
        reasoning = f"""关于「{topic}」怎么做，我给你一个通用思路：

**行动框架**:
1. **明确目标** - 先想清楚最终要达到什么状态
2. **拆解步骤** - 把大目标拆成可执行的小步骤
3. **准备资源** - 列出需要的时间、工具、人脉等
4. **开始行动** - 从最简单的一步开始
5. **调整优化** - 根据反馈不断调整方法

**关键提醒**:
- 不要等"完美时机"，现在就开始
- 第一步可以很小，但一定要迈出去
- 遇到问题很正常，边做边解决

具体到你的情况，可以跟我说说细节，我帮你细化方案～"""

        return {
            "type": "procedural_reasoning",
            "content": reasoning,
            "topic": topic
        }
    
    def _decisional_reasoning(self, query: str, context: Optional[Dict] = None) -> Dict:
        """决策推理 - 回答'要不要/该不该'类问题"""
        topic = self._extract_topic(query)
        
        reasoning = f"""关于「{topic}」这个选择，我帮你梳理一下决策思路：

**决策框架**:
1. **明确核心诉求** - 你最在意的是什么？
2. **列出选项** - 有哪些可选方案？
3. **评估利弊** - 每个选项的得失是什么？
4. **考虑承受力** - 最坏结果能接受吗？
5. **设定止损点** - 什么情况下要调整？

**建议**:
- 没有完美的选择，只有当下最适合的
- 小决定可以快速试错，大决定要慎重
- 有时候"不选择"也是一种选择

你具体是在纠结什么？说说看，我帮你一起分析～"""

        return {
            "type": "decisional_reasoning",
            "content": reasoning,
            "topic": topic
        }
    
    def _comparative_reasoning(self, query: str, context: Optional[Dict] = None) -> Dict:
        """比较推理 - 回答'哪个更好/有什么区别'类问题"""
        topic = self._extract_topic(query)
        
        reasoning = f"""关于「{topic}」的对比，我给你一个分析框架：

**对比维度**:
1. **核心差异** - 本质区别在哪里？
2. **适用场景** - 各自适合什么情况？
3. **成本投入** - 时间、金钱、精力各需要多少？
4. **长期价值** - 哪个更符合你的长远目标？

**选择建议**:
- 不要只看表面，要看底层逻辑
- 适合别人的不一定适合你
- 有时候可以都要，有时候必须取舍

你具体是在对比什么？说说看，我帮你详细分析～"""

        return {
            "type": "comparative_reasoning",
            "content": reasoning,
            "topic": topic
        }
    
    def _general_reasoning(self, query: str, context: Optional[Dict] = None) -> Dict:
        """一般性推理 - 其他问题"""
        reasoning = f"""关于你说的「{query}」，我来帮你分析一下：

**分析思路**:
1. 先明确核心问题是什么
2. 找出关键影响因素
3. 梳理各因素之间的关系
4. 得出初步结论

**建议**:
- 复杂问题拆成小问题逐个突破
- 多问几个"为什么"找到根本原因
- 必要时寻求专业意见

你能再多说点具体情境吗？这样我能给到更有针对性的建议～"""

        return {
            "type": "general_reasoning",
            "content": reasoning,
            "topic": query
        }
    
    def _extract_topic(self, query: str) -> str:
        """提取问题核心主题"""
        # 移除疑问词
        clean_query = query
        for info in self.question_patterns.values():
            for pattern in info["patterns"]:
                clean_query = clean_query.replace(pattern, "")
        
        # 清理空白和标点
        clean_query = re.sub(r'[^\w\s\u4e00-\u9fff]', '', clean_query).strip()
        
        return clean_query if clean_query else query
