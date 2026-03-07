#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
情感计算引擎 - 深度情感交互核心
情感识别 → 情感记忆 → 情感反馈
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import random


class EmotionEngine:
    """情感计算引擎"""
    
    # 情感分类与关键词
    EMOTION_CATEGORIES = {
        "anxiety": {  # 焦虑
            "keywords": ["焦虑", "担心", "害怕", "紧张", "慌", "不安", "忐忑"],
            "intensity_words": ["特别", "非常", "超级", "太", "极了"],
            "response_style": "gentle_comfort"
        },
        "frustrated": {  # 沮丧/失落
            "keywords": ["沮丧", "失落", "灰心", "失望", "心累", "没劲", "没意思"],
            "intensity_words": ["彻底", "完全", "真的", "实在"],
            "response_style": "empathy_first"
        },
        "angry": {  # 生气/愤怒
            "keywords": ["生气", "愤怒", "气死", "烦死", "火大", "恼火", "憋屈"],
            "intensity_words": ["特别", "超级", "太", "简直"],
            "response_style": "validate_then_calm"
        },
        "tired": {  # 疲惫
            "keywords": ["累", "疲惫", "疲倦", "困", "乏力", "熬不住", "撑不住"],
            "intensity_words": ["快", "要", "快不行了", "极了"],
            "response_style": "care_and_rest"
        },
        "overwhelmed": {  # 压力过大
            "keywords": ["压力大", "喘不过气", "太多事", "应付不来", "崩溃", "扛不住"],
            "intensity_words": ["快", "要", "实在", "真的"],
            "response_style": "prioritize_and_relieve"
        },
        "happy": {  # 开心
            "keywords": ["开心", "高兴", "爽", "爽翻", "美滋滋", "乐"],
            "intensity_words": ["特别", "超级", "太", "极了"],
            "response_style": "share_and_celebrate"
        },
        "proud": {  # 自豪/成就
            "keywords": ["自豪", "骄傲", "成就感", "终于", "熬出头"],
            "intensity_words": ["终于", "总算", "真的"],
            "response_style": "affirm_and_reinforce"
        },
        "lonely": {  # 孤独
            "keywords": ["孤独", "孤单", "一个人", "没人", "寂寞"],
            "intensity_words": ["总是", "一直", "永远"],
            "response_style": "accompany_and_understand"
        }
    }
    
    # 共情回复模板 - 真实有温度，不是程序化安慰
    EMPATHY_RESPONSES = {
        "anxiety": {
            "accept": [
                "换谁遇到这种事都会紧张的，这很正常。",
                "担心是正常的，说明你在乎这件事。",
                "我懂这种感觉，心里七上八下的确实不好受。"
            ],
            "understand": [
                "我知道你已经很努力让自己镇定下来了。",
                "这种不确定的感觉确实最熬人。",
                "你不用一个人扛着，说出来会好受点。"
            ],
            "support": [
                "先深呼吸一下，不用急着做决定。",
                "咱们一步一步来，先把最担心的事说清楚。",
                "我陪着你呢，有什么想法都可以跟我说。"
            ]
        },
        "frustrated": {
            "accept": [
                "换谁遇到这事都会难过的，别憋着。",
                "付出那么多却没结果，确实太让人失落了。",
                "这种感受我懂，就像一拳打在棉花上。"
            ],
            "understand": [
                "我知道你已经很努力了，真的。",
                "你不是不够好，只是这次运气差了点。",
                "你已经做得很好了，别对自己太苛刻。"
            ],
            "support": [
                "想哭就哭出来，憋着更难受。",
                "先歇一歇，不用急着振作。",
                "我陪着你，想说什么都可以。"
            ]
        },
        "angry": {
            "accept": [
                "这事换谁都会生气的，太理解你了。",
                "你生气是完全合理的，别憋着。",
                "确实太过分了，难怪你会这么火大。"
            ],
            "understand": [
                "我知道你不是无缘无故发火的。",
                "一直被这样对待，谁都会炸的。",
                "你的愤怒是在保护自己，这没错。"
            ],
            "support": [
                "先消消气，咱们一起想想怎么办。",
                "生气归生气，别气坏了自己。",
                "我站你这边，有什么我可以帮你的？"
            ]
        },
        "tired": {
            "accept": [
                "忙到现在确实太累了，换谁都扛不住。",
                "你已经连轴转多久了？真的该歇歇了。",
                "这种累不是睡一觉就能好的，我懂。"
            ],
            "understand": [
                "我知道你很想再坚持一下，但身体在报警了。",
                "你不是懒，是真的透支了。",
                "你已经撑了很久了，很不容易。"
            ],
            "support": [
                "现在就放下手头的事，去休息会儿吧。",
                "不用有负罪感，休息是应该的。",
                "天塌不下来，先照顾好自己。"
            ]
        },
        "overwhelmed": {
            "accept": [
                "这么多事堆在一起，换谁都得崩溃。",
                "压力大到喘不过气，这种感觉太难受了。",
                "你不是矫情，是真的被压得太久了。"
            ],
            "understand": [
                "我知道你想把所有事都做好，但这真的太难了。",
                "你不是不够强，是担子太重了。",
                "你已经扛了很久了，很不容易。"
            ],
            "support": [
                "咱们先把事情理一理，一件一件来。",
                "不用什么都自己扛，可以找人帮忙的。",
                "现在最重要的是让你自己缓一缓。"
            ]
        },
        "happy": {
            "share": [
                "太为你开心了！这感觉一定超棒！",
                "哇！这真的值得好好庆祝一下！",
                "听到这个我也跟着开心起来了！"
            ],
            "affirm": [
                "这都是你一步步努力换来的，真的不容易。",
                "你值得拥有这份开心，是你应得的。",
                "看看，我就知道你可以的！"
            ],
            "celebrate": [
                "必须好好犒劳一下自己！想吃点啥？",
                "这不得发个朋友圈嘚瑟一下？",
                "记住这种感觉，以后累了就拿出来想想。"
            ]
        },
        "proud": {
            "share": [
                "太牛了！你真的做到了！",
                "这成就感一定爆棚吧！太为你骄傲了！",
                "哇！这可是实打实的成就啊！"
            ],
            "affirm": [
                "看看，所有的坚持都是值得的。",
                "你比自己想象的更厉害。",
                "这就是你实力的证明！"
            ],
            "reinforce": [
                "记住这种感觉，下次遇到困难就想想今天。",
                "你已经有能力做到这么多事了，还有什么好怕的。",
                "这只是一个开始，后面还有更多可能在等你。"
            ]
        },
        "lonely": {
            "accept": [
                "一个人的时候确实容易觉得孤单，这很正常。",
                "想有人陪着说话，这种感受我懂。",
                "孤单的时候看什么都觉得冷清。"
            ],
            "understand": [
                "我知道你不是真的想一个人待着。",
                "你不是没人要，只是还没遇到懂你的人。",
                "这种空落落的感觉，确实不好受。"
            ],
            "support": [
                "我陪着你呢，想聊什么都可以。",
                "你不是一个人，至少还有我在听你说。",
                "要不要找朋友聊聊？有时候主动一点会有惊喜。"
            ]
        }
    }
    
    def __init__(self, memory_path: str = "data/emotion_memory.json"):
        self.memory_path = Path(memory_path)
        self.memory_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.current_emotion: Optional[str] = None
        self.intensity: int = 1  # 1-5
        self.emotion_history: List[Dict] = []
        self.emotion_intensity_level = "medium"  # weak/medium/strong
        
        self._load_memory()
    
    def _load_memory(self):
        """加载情感记忆"""
        if self.memory_path.exists():
            with open(self.memory_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.emotion_history = data.get('history', [])
                self.emotion_intensity_level = data.get('intensity_level', 'medium')
        
        # 清理 7 天前的记忆
        self._cleanup_old_memory()
    
    def _save_memory(self):
        """保存情感记忆"""
        data = {
            'history': self.emotion_history[-50:],  # 只保留最近 50 条
            'intensity_level': self.emotion_intensity_level,
            'last_updated': datetime.now().isoformat()
        }
        with open(self.memory_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def _cleanup_old_memory(self):
        """清理 7 天前的记忆"""
        cutoff = datetime.now() - timedelta(days=7)
        self.emotion_history = [
            e for e in self.emotion_history
            if datetime.fromisoformat(e['timestamp']) >= cutoff
        ]
        self._save_memory()
    
    def recognize(self, text: str, context: Optional[Dict] = None) -> Dict:
        """
        识别情感
        
        Args:
            text: 用户输入
            context: 上下文信息
            
        Returns:
            情感识别结果
        """
        # 1. 关键词匹配
        emotion_scores = {}
        
        for emotion, info in self.EMOTION_CATEGORIES.items():
            score = 0
            for keyword in info["keywords"]:
                if keyword in text:
                    score += 2
                for intensity_word in info["intensity_words"]:
                    if keyword in text and intensity_word in text:
                        # 强度词在关键词附近
                        idx = text.find(keyword)
                        if abs(text.find(intensity_word) - idx) < 5:
                            score += 1
            
            if score > 0:
                emotion_scores[emotion] = score
        
        # 2. 结合上下文
        if context and context.get("recent_emotions"):
            for recent in context["recent_emotions"][:3]:
                if recent["emotion"] in emotion_scores:
                    emotion_scores[recent["emotion"]] += 1
        
        # 3. 确定主导情感
        if emotion_scores:
            self.current_emotion = max(emotion_scores, key=emotion_scores.get)
            self.intensity = min(5, emotion_scores[self.current_emotion])
        else:
            self.current_emotion = "neutral"
            self.intensity = 1
        
        # 4. 记录到历史
        self.emotion_history.append({
            "emotion": self.current_emotion,
            "intensity": self.intensity,
            "text": text[:100],
            "timestamp": datetime.now().isoformat()
        })
        self._save_memory()
        
        return {
            "emotion": self.current_emotion,
            "intensity": self.intensity,
            "category": self.EMOTION_CATEGORIES.get(self.current_emotion, {}),
            "all_scores": emotion_scores
        }
    
    def respond(self, emotion: str, original_query: str, 
                base_response: str = "") -> str:
        """
        生成共情回复
        
        Args:
            emotion: 情感类型
            original_query: 原始输入
            base_response: 基础回复（可选）
            
        Returns:
            共情回复
        """
        if emotion not in self.EMPATHY_RESPONSES:
            return base_response if base_response else "我理解你的感受。"
        
        templates = self.EMPATHY_RESPONSES[emotion]
        
        # 根据情感强度选择回复长度
        if self.intensity >= 4:
            # 高强度：先充分共情
            parts = []
            if "accept" in templates:
                parts.append(random.choice(templates["accept"]))
            if "understand" in templates:
                parts.append(random.choice(templates["understand"]))
            if "support" in templates:
                parts.append(random.choice(templates["support"]))
            return "\n\n".join(parts)
        
        elif self.intensity >= 2:
            # 中等强度：共情 + 轻量建议
            parts = []
            if "accept" in templates:
                parts.append(random.choice(templates["accept"]))
            if "support" in templates:
                parts.append(random.choice(templates["support"]))
            return "\n\n".join(parts)
        
        else:
            # 低强度：简单共情
            if "accept" in templates:
                return random.choice(templates["accept"])
            return "我懂你的感受。"
    
    def get_recent_emotions(self, days: int = 3) -> List[Dict]:
        """获取最近的情感记录"""
        cutoff = datetime.now() - timedelta(days=days)
        return [
            e for e in self.emotion_history
            if datetime.fromisoformat(e['timestamp']) >= cutoff
        ]
    
    def clear_memory(self):
        """清除情感记忆"""
        self.emotion_history = []
        self._save_memory()
        return "已经帮你清掉近期的情绪记忆啦，要是想聊聊随时都在～"
    
    def set_intensity_level(self, level: str) -> bool:
        """设置情感强度等级"""
        if level in ["weak", "medium", "strong"]:
            self.emotion_intensity_level = level
            self._save_memory()
            return True
        return False
    
    def get_emotion_summary(self) -> str:
        """获取情感状态摘要"""
        recent = self.get_recent_emotions(1)
        if not recent:
            return "今天还没有情绪记录哦～"
        
        # 统计主导情绪
        emotion_counts = {}
        for e in recent:
            emotion_counts[e["emotion"]] = emotion_counts.get(e["emotion"], 0) + 1
        
        dominant = max(emotion_counts, key=emotion_counts.get)
        emotion_name = self._get_emotion_name(dominant)
        
        return f"你今天的情绪主要是{emotion_name}，共出现{emotion_counts[dominant]}次。"
    
    def _get_emotion_name(self, emotion: str) -> str:
        """获取情感中文名"""
        names = {
            "anxiety": "焦虑",
            "frustrated": "失落",
            "angry": "生气",
            "tired": "疲惫",
            "overwhelmed": "压力大",
            "happy": "开心",
            "proud": "自豪",
            "lonely": "孤单",
            "neutral": "平静"
        }
        return names.get(emotion, "未知")
    
    def should_adjust_response(self, base_response: str) -> bool:
        """判断是否需要调整回复（根据情感强度）"""
        if self.emotion_intensity_level == "weak":
            return False
        if self.emotion_intensity_level == "strong":
            return True
        # medium: 中等强度以上才调整
        return self.intensity >= 3
