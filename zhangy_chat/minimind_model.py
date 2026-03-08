#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MiniMind 模型加载器
使用 MiniMind 源码中的模型定义
"""

import sys
import os

# 添加模型目录到路径
model_dir = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "models", "zhangy-chat"
)
if os.path.exists(model_dir):
    sys.path.insert(0, model_dir)


def load_model(model_path, device='cpu'):
    """加载 MiniMind 模型"""
    import torch
    
    try:
        # 从源码导入 MiniMind 模型
        from model_minimind import MiniMindForCausalLM, MiniMindConfig
        
        # 首先加载权重来获取实际配置
        print(f"[MiniMind] 正在加载权重：{model_path}")
        state_dict = torch.load(model_path, map_location=device, weights_only=False)
        
        # 从权重推断配置
        embed_weight = None
        for k in state_dict.keys():
            if 'embed_tokens.weight' in k:
                embed_weight = state_dict[k]
                break
        
        if embed_weight is not None:
            vocab_size, hidden_size = embed_weight.shape
        else:
            hidden_size = 768
            vocab_size = 6400
        
        # 计算层数
        layer_keys = [k for k in state_dict.keys() if 'layers.' in k and '.weight' in k]
        layer_nums = set()
        for k in layer_keys:
            parts = k.split('.')
            if len(parts) > 1:
                try:
                    layer_nums.add(int(parts[1]))
                except:
                    pass
        num_layers = max(layer_nums) + 1 if layer_nums else 16
        
        # 推断 head 数
        q_proj_weight = None
        k_proj_weight = None
        for k in state_dict.keys():
            if 'self_attn.q_proj.weight' in k:
                q_proj_weight = state_dict[k]
            if 'self_attn.k_proj.weight' in k:
                k_proj_weight = state_dict[k]
        
        if q_proj_weight is not None:
            num_attention_heads = q_proj_weight.shape[0] // (hidden_size // 64)
        else:
            num_attention_heads = 12
        
        if k_proj_weight is not None:
            num_key_value_heads = k_proj_weight.shape[0] // (hidden_size // 64)
        else:
            num_key_value_heads = 3
        
        print(f"[MiniMind] 模型配置：vocab={vocab_size}, hidden={hidden_size}, layers={num_layers}")
        print(f"[MiniMind] num_heads={num_attention_heads}, num_kv_heads={num_key_value_heads}")
        
        # 创建配置
        config = MiniMindConfig(
            vocab_size=vocab_size,
            hidden_size=hidden_size,
            num_hidden_layers=num_layers,
            num_attention_heads=num_attention_heads,
            num_key_value_heads=num_key_value_heads,
            intermediate_size=hidden_size * 8 // 3,
            max_position_embeddings=32768,
            rms_norm_eps=1e-5,
            rope_theta=1000000.0,
            dropout=0.0
        )
        
        # 创建模型
        model = MiniMindForCausalLM(config)
        
        # 加载权重
        model.load_state_dict(state_dict, strict=False)
        model.to(device)
        model.eval()
        
        print(f"[MiniMind] 模型加载成功！")
        return model
        
    except ImportError as e:
        print(f"[MiniMind] 导入失败：{e}")
        return None
    except Exception as e:
        print(f"[MiniMind] 加载失败：{e}")
        import traceback
        traceback.print_exc()
        return None
