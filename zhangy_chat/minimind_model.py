#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MiniMind 模型定义
参考：https://github.com/jingyaogong/minimind
"""

import math
import torch
from torch import nn
from torch.nn import functional as F


class RMSNorm(nn.Module):
    def __init__(self, hidden_size, eps=1e-6):
        super().__init__()
        self.weight = nn.Parameter(torch.ones(hidden_size))
        self.eps = eps

    def forward(self, hidden_states):
        input_dtype = hidden_states.dtype
        hidden_states = hidden_states.to(torch.float32)
        variance = hidden_states.pow(2).mean(-1, keepdim=True)
        hidden_states = hidden_states * torch.rsqrt(variance + self.eps)
        return self.weight * hidden_states.to(input_dtype)


class SiLU(nn.Module):
    def forward(self, x):
        return x * torch.sigmoid(x)


class MLP(nn.Module):
    def __init__(self, hidden_size, intermediate_size):
        super().__init__()
        self.gate_proj = nn.Linear(hidden_size, intermediate_size, bias=False)
        self.down_proj = nn.Linear(intermediate_size, hidden_size, bias=False)
        self.up_proj = nn.Linear(hidden_size, intermediate_size, bias=False)
        self.act_fn = SiLU()

    def forward(self, x):
        return self.down_proj(self.act_fn(self.gate_proj(x)) * self.up_proj(x))


class Attention(nn.Module):
    def __init__(self, hidden_size, num_heads, num_kv_heads, max_seq_len=512):
        super().__init__()
        self.hidden_size = hidden_size
        self.num_heads = num_heads
        self.num_kv_heads = num_kv_heads
        self.head_dim = hidden_size // num_heads
        self.max_seq_len = max_seq_len
        
        self.q_proj = nn.Linear(hidden_size, hidden_size, bias=False)
        self.k_proj = nn.Linear(hidden_size, num_kv_heads * self.head_dim, bias=False)
        self.v_proj = nn.Linear(hidden_size, num_kv_heads * self.head_dim, bias=False)
        self.o_proj = nn.Linear(hidden_size, hidden_size, bias=False)
        
        # 注册位置编码缓冲区
        self.register_buffer(
            "rotary_emb",
            self._build_rotary_emb(max_seq_len),
            persistent=False
        )
        
        # GQA 重复因子
        self.num_q_per_kv = num_heads // num_kv_heads

    def _build_rotary_emb(self, max_seq_len):
        inv_freq = 1.0 / (
            10000 ** (torch.arange(0, self.head_dim, 2).float() / self.head_dim)
        )
        t = torch.arange(max_seq_len).float().unsqueeze(1)
        freqs = t @ inv_freq.unsqueeze(0)
        freqs = torch.cat((freqs, freqs), dim=-1)
        return torch.stack([freqs.sin(), freqs.cos()], dim=-1)

    def _apply_rotary(self, x, start_pos):
        seqlen = x.shape[1]
        rotary_emb = self.rotary_emb[start_pos : start_pos + seqlen, :, :]
        rotary_emb = rotary_emb.to(x.device)
        x_ = x.reshape(x.shape[0], seqlen, -1, self.head_dim)
        x_rot = x_.reshape_as(rotary_emb[..., 0])
        x1, x2 = x_rot[..., 0], x_rot[..., 1]
        c1, c2 = rotary_emb[..., 0], rotary_emb[..., 1]
        y1 = x1 * c1 - x2 * c2
        y2 = x1 * c2 + x2 * c1
        y = torch.stack((y1, y2), dim=-1).flatten(-2)
        return y.reshape_as(x)

    def forward(self, x, start_pos=0):
        bsz, seq_len, _ = x.shape
        
        q = self.q_proj(x)
        k = self.k_proj(x)
        v = self.v_proj(x)
        
        q = self._apply_rotary(q, start_pos)
        k = self._apply_rotary(k, start_pos)
        
        # GQA: reshape q and k/v
        q = q.view(bsz, seq_len, self.num_heads, self.head_dim).transpose(1, 2)
        k = k.view(bsz, seq_len, self.num_kv_heads, self.head_dim).transpose(1, 2)
        v = v.view(bsz, seq_len, self.num_kv_heads, self.head_dim).transpose(1, 2)
        
        # 重复 k/v 以匹配 q 的 heads
        if self.num_q_per_kv > 1:
            k = k.repeat_interleave(self.num_q_per_kv, dim=1)
            v = v.repeat_interleave(self.num_q_per_kv, dim=1)
        
        # 简化注意力
        scores = torch.matmul(q, k.transpose(-2, -1)) / math.sqrt(self.head_dim)
        attn = F.softmax(scores, dim=-1)
        output = torch.matmul(attn, v)
        
        output = output.transpose(1, 2).reshape(bsz, seq_len, self.hidden_size)
        return self.o_proj(output)


class TransformerBlock(nn.Module):
    def __init__(self, hidden_size, num_heads, num_kv_heads, intermediate_size):
        super().__init__()
        self.self_attn = Attention(hidden_size, num_heads, num_kv_heads)
        self.input_layernorm = RMSNorm(hidden_size)
        self.post_attention_layernorm = RMSNorm(hidden_size)
        self.mlp = MLP(hidden_size, intermediate_size)

    def forward(self, x, start_pos=0):
        h = x + self.self_attn(self.input_layernorm(x), start_pos)
        out = h + self.mlp(self.post_attention_layernorm(h))
        return out


class MiniMindLM(nn.Module):
    """MiniMind 语言模型"""
    
    def __init__(self, vocab_size=6400, hidden_size=768, num_layers=8,
                 num_heads=12, num_kv_heads=3, intermediate_size=2048, max_seq_len=512):
        super().__init__()
        self.vocab_size = vocab_size
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        
        self.embed_tokens = nn.Embedding(vocab_size, hidden_size)
        
        self.layers = nn.ModuleList([
            TransformerBlock(hidden_size, num_heads, num_kv_heads, intermediate_size)
            for _ in range(num_layers)
        ])
        
        self.norm = RMSNorm(hidden_size)
        self.lm_head = nn.Linear(hidden_size, vocab_size, bias=False)
        
        self.max_seq_len = max_seq_len

    def forward(self, input_ids):
        x = self.embed_tokens(input_ids)
        
        for i, layer in enumerate(self.layers):
            x = layer(x, start_pos=0)
        
        x = self.norm(x)
        logits = self.lm_head(x)
        
        return logits
    
    @torch.no_grad()
    def generate(self, input_ids, max_new_tokens=512, temperature=0.7, do_sample=True):
        """生成文本"""
        self.eval()
        
        generated = input_ids.clone()
        
        for _ in range(max_new_tokens):
            # 截断到最大长度
            if generated.shape[1] > self.max_seq_len:
                generated = generated[:, -self.max_seq_len:]
            
            # 前向传播
            outputs = self(generated)
            next_token_logits = outputs[:, -1, :]
            
            # 采样
            if temperature > 0.0:
                probs = F.softmax(next_token_logits / temperature, dim=-1)
                if do_sample:
                    next_token = torch.multinomial(probs, num_samples=1)
                else:
                    next_token = torch.argmax(probs, dim=-1, keepdim=True)
            else:
                next_token = torch.argmax(next_token_logits, dim=-1, keepdim=True)
            
            generated = torch.cat((generated, next_token), dim=1)
            
            # 检查是否生成 EOS
            if next_token.item() == 2:  # EOS token
                break
        
        return generated


def load_model(model_path, device='cpu'):
    """加载 MiniMind 模型"""
    import torch
    
    # 加载 checkpoint
    checkpoint = torch.load(model_path, map_location=device, weights_only=False)
    
    # 检测模型配置
    if 'model.embed_tokens.weight' in checkpoint:
        # 提取配置
        embed_weight = checkpoint['model.embed_tokens.weight']
        vocab_size, hidden_size = embed_weight.shape
        
        # 推断层数 - 找最大层号
        layer_nums = set()
        for k in checkpoint.keys():
            if 'model.layers.' in k:
                parts = k.split('.')
                if len(parts) > 2:
                    try:
                        layer_nums.add(int(parts[2]))
                    except:
                        pass
        num_layers = max(layer_nums) + 1 if layer_nums else 16
        
        # 推断 num_heads 和 num_kv_heads
        q_proj_weight = checkpoint['model.layers.0.self_attn.q_proj.weight']
        k_proj_weight = checkpoint['model.layers.0.self_attn.k_proj.weight']
        
        head_dim = q_proj_weight.shape[0] // 12  # 假设 num_heads=12
        num_heads = hidden_size // head_dim
        num_kv_heads = k_proj_weight.shape[0] // head_dim
        
        print(f"[MiniMind] 模型配置：vocab={vocab_size}, hidden={hidden_size}, layers={num_layers}")
        print(f"[MiniMind] num_heads={num_heads}, num_kv_heads={num_kv_heads}, head_dim={head_dim}")
        
        # 创建模型
        model = MiniMindLM(
            vocab_size=vocab_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            num_heads=num_heads,
            num_kv_heads=num_kv_heads,
            intermediate_size=hidden_size * 8 // 3,
            max_seq_len=512
        )
        
        # 移除 'model.' 前缀并加载权重
        new_state_dict = {}
        for k, v in checkpoint.items():
            if k.startswith('model.'):
                new_state_dict[k[6:]] = v
            else:
                new_state_dict[k] = v
        
        # 加载权重
        model.load_state_dict(new_state_dict)
        model.to(device)
        model.eval()
        
        return model
    else:
        print("[MiniMind] 未知的模型格式")
        return None


class MiniMindTokenizer:
    """MiniMind 简单 tokenizer"""
    
    def __init__(self, vocab_size=6400):
        self.vocab_size = vocab_size
        self.pad_token_id = 0
        self.bos_token_id = 1
        self.eos_token_id = 2
    
    def encode(self, text, return_tensors="pt"):
        """字符级编码"""
        import torch
        ids = [self.bos_token_id] + [ord(c) % (self.vocab_size - 10) + 10 for c in text]
        if return_tensors == "pt":
            return torch.tensor([ids])
        return ids
    
    def decode(self, ids, skip_special_tokens=True):
        """字符级解码"""
        if hasattr(ids, 'tolist'):
            ids = ids.tolist()
        if isinstance(ids[0], list):
            ids = ids[0]
        
        text = ''
        for i in ids:
            if skip_special_tokens and i in [self.pad_token_id, self.bos_token_id, self.eos_token_id]:
                continue
            if i >= 10:
                text += chr((i - 10) % 10000)
        return text
    
    def apply_chat_template(self, messages, tokenize=False, add_generation_prompt=True):
        """对话模板"""
        prompt = ""
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if role == "user":
                prompt += f"Human: {content}\n\n"
            elif role == "assistant":
                prompt += f"Assistant: {content}\n\n"
        
        if add_generation_prompt:
            prompt += "Assistant:"
        
        return prompt
