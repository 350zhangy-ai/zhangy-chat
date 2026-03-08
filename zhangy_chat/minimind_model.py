#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MiniMind 模型加载器
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


def load_model(model_path, device='cpu'):
    """加载 MiniMind 模型"""
    import torch
    
    try:
        from model_minimind import MiniMindForCausalLM, MiniMindConfig
        
        # 首先加载权重来获取实际配置
        print(f"[MiniMind] 正在加载权重：{model_path}")
        state_dict = torch.load(model_path, map_location=device, weights_only=False)
        
        # 从权重推断配置
        embed_weight = state_dict.get('embed_tokens.weight', state_dict.get('model.embed_tokens.weight'))
        if embed_weight is not None:
            vocab_size, hidden_size = embed_weight.shape
        else:
            hidden_size = 768  # 默认值
            vocab_size = 6400
        
        # 计算层数
        layer_keys = [k for k in state_dict.keys() if 'layers.' in k and '.weight' in k]
        num_layers = len(set(k.split('.')[1] for k in layer_keys))
        
        print(f"[MiniMind] 推断配置：vocab={vocab_size}, hidden={hidden_size}, layers={num_layers}")
        
        # 创建配置
        config = MiniMindConfig(
            vocab_size=vocab_size,
            hidden_size=hidden_size,
            num_hidden_layers=num_layers,
            num_attention_heads=hidden_size // 64,  # head_dim=64
            num_key_value_heads=hidden_size // 256 if hidden_size == 768 else 2,  # GQA
            intermediate_size=hidden_size * 8 // 3,
            max_position_embeddings=32768,
            rms_norm_eps=1e-5,
            rope_theta=1000000.0
        )
        
        # 创建模型
        model = MiniMindForCausalLM(config)
        
        # 直接加载权重（不修改 key）
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
