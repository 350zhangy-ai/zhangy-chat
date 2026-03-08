#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MiniMind 官方 Tokenizer 模拟
由于无法下载官方 tokenizer，这里创建一个兼容层
"""

import json
import os
import re


class MiniMindTokenizer:
    """MiniMind Tokenizer（模拟官方行为）"""
    
    def __init__(self, vocab_size=6400):
        self.vocab_size = vocab_size
        self.pad_token_id = 0
        self.bos_token_id = 1
        self.eos_token_id = 2
        self.unk_token_id = 3
        
        # 尝试加载词表
        self.token_to_id = {}
        self.id_to_token = {}
        self._load_vocab()
        
    def _load_vocab(self):
        """加载词表"""
        # 检查是否有词表文件
        vocab_paths = [
            'minimind/vocab.json',
            'models/zhangy-chat/vocab.json',
        ]
        
        for vocab_path in vocab_paths:
            if os.path.exists(vocab_path):
                with open(vocab_path, 'r', encoding='utf-8') as f:
                    self.token_to_id = json.load(f)
                    self.id_to_token = {v: k for k, v in self.token_to_id.items()}
                print(f"[Tokenizer] 已加载词表：{vocab_path}")
                return
        
        # 没有词表，使用字符级映射
        print("[Tokenizer] 未找到词表，使用字符级映射")
        self._build_char_vocab()
        
    def _build_char_vocab(self):
        """构建字符级词表"""
        # 常用中文字符
        token_id = 10
        # 基本汉字：0x4E00-0x9FFF
        for code in range(0x4E00, min(0x9FFF + 1, 0x4E00 + 6390)):
            char = chr(code)
            self.token_to_id[char] = token_id
            self.id_to_token[token_id] = char
            token_id += 1
            
    def encode(self, text, return_tensors="pt"):
        """编码"""
        import torch
        
        ids = [self.bos_token_id]
        
        # 尝试逐字符编码
        for char in text:
            if char in self.token_to_id:
                ids.append(self.token_to_id[char])
            else:
                ids.append(self.unk_token_id)
                
        if return_tensors == "pt":
            return torch.tensor([ids])
        return ids
    
    def decode(self, ids, skip_special_tokens=True):
        """解码"""
        if hasattr(ids, 'tolist'):
            ids = ids.tolist()
        if isinstance(ids[0], list):
            ids = ids[0]
        
        tokens = []
        for i in ids:
            if skip_special_tokens and i in [self.pad_token_id, self.bos_token_id, self.eos_token_id]:
                continue
            if i in self.id_to_token:
                tokens.append(self.id_to_token[i])
            elif i < self.vocab_size and i >= 10:
                # 尝试还原为汉字
                code = 0x4E00 + (i - 10)
                if 0x4E00 <= code <= 0x9FFF:
                    tokens.append(chr(code))
        
        return ''.join(tokens)
    
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
