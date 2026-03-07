#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
内存管理模块 - 8/16/32/64GiB 内存配置与适配
"""

import json
from pathlib import Path
from typing import Dict, Optional
import psutil


class MemoryManager:
    """内存管理器"""
    
    # 内存配置预设值
    MEMORY_PRESETS = {
        8: {
            "cache_size": 64,        # MB
            "max_concurrent": 2,
            "batch_size": 16,
            "data_loading": "chunked"  # chunked / full
        },
        16: {
            "cache_size": 256,
            "max_concurrent": 4,
            "batch_size": 32,
            "data_loading": "chunked"
        },
        32: {
            "cache_size": 512,
            "max_concurrent": 8,
            "batch_size": 64,
            "data_loading": "mixed"
        },
        64: {
            "cache_size": 1024,
            "max_concurrent": 16,
            "batch_size": 128,
            "data_loading": "full"
        }
    }
    
    def __init__(self, config_path: str = "data/memory_config.json"):
        self.config_path = Path(config_path)
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.selected_memory: int = 16  # 默认 16GiB
        self.actual_memory: int = 16    # 实际物理内存
        self.current_config: Dict = {}
        
        self._load_config()
        self._detect_actual_memory()
        
        # 如果选择的内存超出实际内存，自动降级
        if self.selected_memory > self.actual_memory:
            self.selected_memory = self.actual_memory
            self._save_config()
        
        self.current_config = self.get_memory_config()
    
    def _load_config(self):
        """加载配置"""
        if self.config_path.exists():
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                self.selected_memory = config.get('selected_memory', 16)
    
    def _save_config(self):
        """保存配置"""
        config = {
            'selected_memory': self.selected_memory,
            'actual_memory': self.actual_memory
        }
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
    
    def _detect_actual_memory(self):
        """检测实际物理内存"""
        try:
            # 获取系统内存（字节）
            total_memory = psutil.virtual_memory().total
            # 转换为 GiB
            self.actual_memory = int(total_memory / (1024 ** 3))
            
            # 向下取整到最近的预设值
            presets = sorted(self.MEMORY_PRESETS.keys())
            for preset in reversed(presets):
                if self.actual_memory >= preset:
                    self.actual_memory = preset
                    break
            else:
                self.actual_memory = presets[0]
        except Exception:
            self.actual_memory = 16  # 默认值
    
    def set_memory(self, memory_gib: int) -> Dict:
        """设置内存配置
        
        Args:
            memory_gib: 内存大小 (8/16/32/64)
            
        Returns:
            配置结果
        """
        if memory_gib not in self.MEMORY_PRESETS:
            return {
                "success": False,
                "message": f"不支持的内存配置：{memory_gib}GiB",
                "available": list(self.MEMORY_PRESETS.keys())
            }
        
        # 检查是否超出实际内存
        if memory_gib > self.actual_memory:
            self.selected_memory = self.actual_memory
            self._save_config()
            return {
                "success": False,
                "message": f"选择的内存配置 ({memory_gib}GiB) 超出实际物理内存 ({self.actual_memory}GiB)，已自动降级",
                "current": self.actual_memory
            }
        
        self.selected_memory = memory_gib
        self._save_config()
        self.current_config = self.get_memory_config()
        
        return {
            "success": True,
            "message": f"内存配置已设置为 {memory_gib}GiB",
            "config": self.current_config
        }
    
    def get_memory_config(self) -> Dict:
        """获取当前内存配置参数"""
        return self.MEMORY_PRESETS.get(self.selected_memory, self.MEMORY_PRESETS[16])
    
    def get_memory_info(self) -> Dict:
        """获取内存信息"""
        return {
            "selected": self.selected_memory,
            "actual": self.actual_memory,
            "config": self.get_memory_config(),
            "usage": f"{psutil.virtual_memory().percent}%"
        }
    
    def get_cache_size(self) -> int:
        """获取缓存大小（MB）"""
        return self.current_config.get('cache_size', 256)
    
    def get_max_concurrent(self) -> int:
        """获取最大并发数"""
        return self.current_config.get('max_concurrent', 4)
    
    def get_batch_size(self) -> int:
        """获取批次大小"""
        return self.current_config.get('batch_size', 32)
    
    def get_data_loading_mode(self) -> str:
        """获取数据加载模式"""
        return self.current_config.get('data_loading', 'chunked')
    
    def is_low_memory_mode(self) -> bool:
        """是否为低内存模式（8GiB）"""
        return self.selected_memory <= 8
    
    def is_high_memory_mode(self) -> bool:
        """是否为高内存模式（32GiB+）"""
        return self.selected_memory >= 32
