#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MiniMind 模型定义
来自：https://github.com/jingyaogong/minimind
"""

import sys
import os

# 添加 MiniMind 模型目录到路径
minimind_model_dir = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "models", "zhangy-chat"
)
if os.path.exists(minimind_model_dir):
    sys.path.insert(0, minimind_model_dir)

try:
    from model_minimind import MiniMindForCausalLM, MiniMindConfig
    from transformers import AutoTokenizer
    
    def load_model(model_path, device='cpu'):
        """加载 MiniMind 模型"""
        import torch
        
        # 加载配置
        config = MiniMindConfig.from_pretrained(os.path.dirname(model_path))
        
        # 加载模型
        model = MiniMindForCausalLM.from_pretrained(
            os.path.dirname(model_path),
            config=config,
            torch_dtype=torch.float32
        )
        model.to(device)
        model.eval()
        
        print(f"[MiniMind] 模型加载成功：{model_path}")
        return model
        
except ImportError as e:
    print(f"[MiniMind] 导入失败：{e}")
    
    def load_model(model_path, device='cpu'):
        """加载 MiniMind 模型（降级版本）"""
        print("[MiniMind] 使用降级加载方案")
        return None
