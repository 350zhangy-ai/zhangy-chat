#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
预设管理模块 - 多场景预设配置与切换
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime


class PresetManager:
    """预设管理器"""
    
    # 内置预设配置
    BUILTIN_PRESETS = {
        "office": {
            "name": "高效办公",
            "icon": "💼",
            "description": "侧重任务拆解、时间管理、简洁回应",
            "config": {
                # 功能开关
                "enable_task_priority": True,
                "enable_procrastination_reminder": True,
                "enable_emotional_comfort": False,
                "enable_casual_chat": False,
                "enable_learning_plan": False,
                "enable_review_report": True,
                
                # 界面设置
                "hide_redundant_hints": True,
                "show_quick_actions": True,
                "focus_mode": True,
                
                # 回应风格
                "response_style": "concise",
                "max_response_length": "medium",
                "show_emoji": False,
                
                # 任务优先级规则
                "priority_rules": {
                    "deadline_weight": 0.4,
                    "importance_weight": 0.4,
                    "complexity_weight": 0.2
                }
            }
        },
        "exam": {
            "name": "备考冲刺",
            "icon": "📚",
            "description": "侧重学习计划、知识点梳理、打卡提醒",
            "config": {
                "enable_task_priority": True,
                "enable_procrastination_reminder": True,
                "enable_emotional_comfort": True,
                "enable_casual_chat": False,
                "enable_learning_plan": True,
                "enable_review_report": True,
                "enable_habit_checkin": True,
                
                "hide_redundant_hints": False,
                "show_quick_actions": True,
                "focus_mode": True,
                
                "response_style": "structured",
                "max_response_length": "long",
                "show_emoji": True,
                
                "priority_rules": {
                    "deadline_weight": 0.5,
                    "importance_weight": 0.3,
                    "complexity_weight": 0.2
                },
                
                # 学习特定设置
                "study_settings": {
                    "enable_knowledge_map": True,
                    "enable_daily_review": True,
                    "enable_mock_exam_reminder": True
                }
            }
        },
        "casual": {
            "name": "休闲陪伴",
            "icon": "🍵",
            "description": "侧重轻松聊天、生活建议、兴趣话题",
            "config": {
                "enable_task_priority": False,
                "enable_procrastination_reminder": False,
                "enable_emotional_comfort": True,
                "enable_casual_chat": True,
                "enable_learning_plan": False,
                "enable_review_report": False,
                "enable_habit_checkin": False,
                
                "hide_redundant_hints": False,
                "show_quick_actions": False,
                "focus_mode": False,
                
                "response_style": "friendly",
                "max_response_length": "medium",
                "show_emoji": True,
                
                "priority_rules": {
                    "deadline_weight": 0.2,
                    "importance_weight": 0.3,
                    "complexity_weight": 0.1
                }
            }
        },
        "emotional": {
            "name": "情绪疏导",
            "icon": "💚",
            "description": "侧重共情倾听、压力缓解、心理调节",
            "config": {
                "enable_task_priority": False,
                "enable_procrastination_reminder": False,
                "enable_emotional_comfort": True,
                "enable_casual_chat": True,
                "enable_learning_plan": False,
                "enable_review_report": False,
                "enable_habit_checkin": False,
                
                "hide_redundant_hints": True,
                "show_quick_actions": False,
                "focus_mode": False,
                
                "response_style": "empathetic",
                "max_response_length": "medium",
                "show_emoji": True,
                
                "priority_rules": {
                    "deadline_weight": 0.1,
                    "importance_weight": 0.2,
                    "complexity_weight": 0.1
                },
                
                # 情绪疏导特定设置
                "emotional_settings": {
                    "enable_active_listening": True,
                    "enable_validation": True,
                    "enable_relaxation_tips": True,
                    "enable_breathing_exercise": True
                }
            }
        }
    }
    
    def __init__(self, 
                 presets_path: str = "data/presets.json",
                 user_presets_path: str = "data/user_presets.json"):
        self.presets_path = Path(presets_path)
        self.user_presets_path = Path(user_presets_path)
        
        self.presets_path.parent.mkdir(parents=True, exist_ok=True)
        self.user_presets_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.current_preset: str = "office"  # 默认高效办公
        self.user_presets: Dict[str, Dict] = {}
        
        self._load_presets()
        self._load_user_presets()
    
    def _load_presets(self):
        """加载内置预设"""
        if self.presets_path.exists():
            with open(self.presets_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.current_preset = data.get('current_preset', 'office')
    
    def _save_presets(self):
        """保存内置预设配置"""
        data = {
            'current_preset': self.current_preset
        }
        with open(self.presets_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def _load_user_presets(self):
        """加载用户自定义预设"""
        if self.user_presets_path.exists():
            with open(self.user_presets_path, 'r', encoding='utf-8') as f:
                self.user_presets = json.load(f)
    
    def _save_user_presets(self):
        """保存用户自定义预设"""
        with open(self.user_presets_path, 'w', encoding='utf-8') as f:
            json.dump(self.user_presets, f, ensure_ascii=False, indent=2)
    
    def set_preset(self, preset_key: str) -> Dict:
        """设置当前预设
        
        Args:
            preset_key: 预设键 (office/exam/casual/emotional 或自定义名称)
            
        Returns:
            设置结果
        """
        # 检查是否是用户自定义预设
        if preset_key in self.user_presets:
            self.current_preset = preset_key
            self._save_presets()
            return {
                "success": True,
                "message": f"已加载预设「{self.user_presets[preset_key]['name']}」",
                "preset": preset_key,
                "is_custom": True
            }
        
        # 检查是否是内置预设
        if preset_key not in self.BUILTIN_PRESETS:
            return {
                "success": False,
                "message": f"不支持的预设：{preset_key}",
                "available": list(self.BUILTIN_PRESETS.keys()) + list(self.user_presets.keys())
            }
        
        self.current_preset = preset_key
        self._save_presets()
        
        preset_info = self.BUILTIN_PRESETS[preset_key]
        return {
            "success": True,
            "message": f"已加载{preset_info['name']}预设",
            "preset": preset_key,
            "is_custom": False
        }
    
    def get_current_preset(self) -> str:
        """获取当前预设键"""
        return self.current_preset
    
    def get_preset_config(self, preset_key: Optional[str] = None) -> Dict:
        """获取预设配置
        
        Args:
            preset_key: 预设键，不传则使用当前预设
            
        Returns:
            预设配置字典
        """
        key = preset_key or self.current_preset
        
        if key in self.user_presets:
            return self.user_presets[key].get('config', {})
        
        return self.BUILTIN_PRESETS.get(key, self.BUILTIN_PRESETS["office"]).get('config', {})
    
    def get_all_presets(self) -> List[Dict]:
        """获取所有预设列表"""
        presets = []
        
        # 添加内置预设
        for key, preset in self.BUILTIN_PRESETS.items():
            presets.append({
                "key": key,
                "name": preset["name"],
                "icon": preset["icon"],
                "description": preset["description"],
                "is_custom": False,
                "is_active": key == self.current_preset
            })
        
        # 添加用户自定义预设
        for key, preset in self.user_presets.items():
            presets.append({
                "key": key,
                "name": preset["name"],
                "icon": preset.get("icon", "📁"),
                "description": preset.get("description", "自定义预设"),
                "is_custom": True,
                "is_active": key == self.current_preset
            })
        
        return presets
    
    def add_custom_preset(self, name: str, config: Dict, 
                          icon: str = "📁", 
                          description: str = "自定义预设",
                          preset_key: Optional[str] = None) -> Dict:
        """添加自定义预设
        
        Args:
            name: 预设名称
            config: 预设配置
            icon: 图标
            description: 描述
            preset_key: 预设键（不传则自动生成）
            
        Returns:
            添加结果
        """
        if preset_key is None:
            # 自动生成键名
            import re
            key_base = re.sub(r'[^\w]', '', name.lower())
            preset_key = key_base
            counter = 1
            while preset_key in self.user_presets:
                preset_key = f"{key_base}_{counter}"
                counter += 1
        
        if preset_key in self.BUILTIN_PRESETS:
            return {
                "success": False,
                "message": f"预设名称「{preset_key}」与内置预设冲突，请更换名称"
            }
        
        self.user_presets[preset_key] = {
            "name": name,
            "icon": icon,
            "description": description,
            "config": config,
            "created_at": datetime.now().isoformat()
        }
        
        self._save_user_presets()
        
        return {
            "success": True,
            "message": f"已添加自定义预设「{name}」",
            "preset_key": preset_key
        }
    
    def delete_custom_preset(self, preset_key: str) -> Dict:
        """删除自定义预设"""
        if preset_key in self.BUILTIN_PRESETS:
            return {
                "success": False,
                "message": "不能删除内置预设"
            }
        
        if preset_key not in self.user_presets:
            return {
                "success": False,
                "message": f"预设不存在：{preset_key}"
            }
        
        del self.user_presets[preset_key]
        self._save_user_presets()
        
        # 如果删除的是当前预设，切换回默认预设
        if self.current_preset == preset_key:
            self.current_preset = "office"
            self._save_presets()
        
        return {
            "success": True,
            "message": f"已删除预设「{preset_key}」"
        }
    
    def get_feature_status(self, feature: str) -> bool:
        """获取功能开关状态"""
        config = self.get_current_preset_config()
        return config.get(feature, False)
    
    def is_focus_mode(self) -> bool:
        """是否为专注模式"""
        config = self.get_preset_config()
        return config.get('focus_mode', False)
    
    def is_empathetic_mode(self) -> bool:
        """是否为共情模式"""
        config = self.get_preset_config()
        return config.get('enable_emotional_comfort', False)
