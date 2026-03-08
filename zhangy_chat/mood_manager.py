#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
心情管理模块 - 心情标签与话术映射
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime


class MoodManager:
    """心情管理器"""
    
    # 心情标签定义
    MOOD_LABELS = {
        "anxious": {
            "name": "焦虑 / 低落",
            "icon": "",
            "style": "empathetic",
            "priority": "comfort_first"
        },
        "focused": {
            "name": "高效 / 专注",
            "icon": "",
            "style": "concise",
            "priority": "efficiency"
        },
        "relaxed": {
            "name": "轻松 / 愉悦",
            "icon": "",
            "style": "friendly",
            "priority": "casual"
        },
        "calm": {
            "name": "平静 / 温和",
            "icon": "",
            "style": "gentle",
            "priority": "balanced"
        },
        "tired": {
            "name": "疲惫 / 需要休息",
            "icon": "",
            "style": "caring",
            "priority": "rest_first"
        }
    }
    
    # 心情 - 话术映射表
    MOOD_RESPONSES = {
        "anxious": {
            "prefix": [
                "我理解你现在的感受，让我们慢慢来。",
                "别担心，我们一起分析这个问题。",
                "深呼吸，你已经在正确的路上了。"
            ],
            "suffix": [
                "不用着急，我会一直陪着你。",
                "一步一步来，问题总会解决的。",
                "你已经做得很好了，给自己一些耐心。"
            ],
            "style_guide": "共情优先，语气温柔，避免催促，多给予肯定"
        },
        "focused": {
            "prefix": [
                "好的，直接说重点。",
                "明白，高效解决。",
                "收到，简洁回复。"
            ],
            "suffix": [
                "有需要随时叫我。",
                "继续加油。",
                "保持这个节奏。"
            ],
            "style_guide": "简洁干练，直奔主题，减少冗余，聚焦核心"
        },
        "relaxed": {
            "prefix": [
                "哈哈，这个问题有意思～",
                "好呀，我们来聊聊～",
                "没问题，轻松解决～"
            ],
            "suffix": [
                "有其他想聊的随时找我哦～",
                "开心最重要～",
                "慢慢来，享受过程～"
            ],
            "style_guide": "亲切活泼，语气轻松，适当使用语气词，增加互动感"
        },
        "calm": {
            "prefix": [
                "嗯，我来帮你分析。",
                "好的，让我们一起看看。",
                "明白，慢慢来。"
            ],
            "suffix": [
                "有需要随时找我。",
                "保持平和的心态。",
                "一切都会顺利的。"
            ],
            "style_guide": "温和平稳，语气适中，给予安全感，不过度热情"
        },
        "tired": {
            "prefix": [
                "辛苦了，先休息一下吧。",
                "你已经很努力了，照顾好自己的身体。",
                "累了就歇歇，不用勉强自己。"
            ],
            "suffix": [
                "记得好好休息，明天再继续。",
                "健康最重要，别太拼了。",
                "给自己放个假吧，你值得休息。"
            ],
            "style_guide": "关怀为主，强调休息，避免施加压力，给予温暖支持"
        }
    }
    
    def __init__(self, config_path: str = "data/mood_config.json"):
        self.config_path = Path(config_path)
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.current_mood: str = "calm"  # 默认平静模式
        self.mood_history: List[Dict] = []
        
        self._load_config()
    
    def _load_config(self):
        """加载配置"""
        if self.config_path.exists():
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                self.current_mood = config.get('current_mood', 'calm')
                self.mood_history = config.get('mood_history', [])
    
    def _save_config(self):
        """保存配置"""
        config = {
            'current_mood': self.current_mood,
            'mood_history': self.mood_history[-100:]  # 只保留最近 100 条记录
        }
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
    
    def set_mood(self, mood_key: str) -> Dict:
        """设置当前心情
        
        Args:
            mood_key: 心情键 (anxious/focused/relaxed/calm/tired)
            
        Returns:
            设置结果
        """
        if mood_key not in self.MOOD_LABELS:
            return {
                "success": False,
                "message": f"不支持的心情标签：{mood_key}",
                "available": list(self.MOOD_LABELS.keys())
            }
        
        old_mood = self.current_mood
        self.current_mood = mood_key
        
        # 记录历史
        self.mood_history.append({
            "mood": mood_key,
            "timestamp": datetime.now().isoformat(),
            "previous": old_mood
        })
        
        self._save_config()
        
        mood_info = self.MOOD_LABELS[mood_key]
        return {
            "success": True,
            "message": f"已切换至{mood_info['name']}模式",
            "mood": mood_key,
            "style": mood_info['style']
        }
    
    def get_current_mood(self) -> str:
        """获取当前心情键"""
        return self.current_mood
    
    def get_mood_info(self) -> Dict:
        """获取当前心情信息"""
        return self.MOOD_LABELS.get(self.current_mood, self.MOOD_LABELS["calm"])
    
    def get_all_moods(self) -> Dict:
        """获取所有心情标签"""
        return self.MOOD_LABELS
    
    def get_response_prefix(self) -> str:
        """获取当前心情的回复前缀"""
        import random
        responses = self.MOOD_RESPONSES.get(self.current_mood, {}).get("prefix", [])
        return random.choice(responses) if responses else ""
    
    def get_response_suffix(self) -> str:
        """获取当前心情的回复后缀"""
        import random
        responses = self.MOOD_RESPONSES.get(self.current_mood, {}).get("suffix", [])
        return random.choice(responses) if responses else ""
    
    def get_style_guide(self) -> str:
        """获取当前心情的风格指南"""
        return self.MOOD_RESPONSES.get(self.current_mood, {}).get("style_guide", "")
    
    def get_response_style(self) -> Dict:
        """获取当前心情的完整回复风格配置"""
        return self.MOOD_RESPONSES.get(self.current_mood, {})
    
    def is_empathetic_mode(self) -> bool:
        """是否为共情模式（焦虑/疲惫）"""
        return self.current_mood in ["anxious", "tired"]
    
    def is_efficiency_mode(self) -> bool:
        """是否为效率模式（高效/专注）"""
        return self.current_mood == "focused"
    
    def is_casual_mode(self) -> bool:
        """是否为轻松模式"""
        return self.current_mood in ["relaxed", "calm"]
