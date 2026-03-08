#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AI 助手 - 基于 MiniMind 模型 (简化版)
"""

from typing import Optional, Dict
from datetime import datetime


class MiniMindAssistant:
    """AI 助手 (基于 MiniMind 模型)"""

    def __init__(self, model_path: Optional[str] = None):
        # 默认使用 models/zhangy-chat 目录
        if model_path is None:
            import os
            default_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models", "zhangy-chat")
            if os.path.exists(default_path):
                model_path = default_path
        self.model_path = model_path
        self.model = None
        self.tokenizer = None
        self.thought_process = []
        self._load_model()
    
    def _load_model(self):
        """加载模型"""
        if self.model_path:
            try:
                import os
                # 查找模型文件
                model_files = ["full_sft_768.pth", "full_sft_512.pth", "grpo_768.pth"]
                model_file = None
                for f in model_files:
                    path = os.path.join(self.model_path, f)
                    if os.path.exists(path):
                        model_file = path
                        break
                
                if model_file:
                    print(f"加载模型：{model_file}")
                    # 使用 PyTorch 加载
                    import torch
                    checkpoint = torch.load(model_file, map_location='cpu', weights_only=True)
                    self.model = checkpoint
                    print("模型加载成功！")
                else:
                    print("未找到模型文件，使用备用回复")
            except Exception as e:
                print(f"模型加载失败：{e}，使用备用回复")
                self.model = None
    
    def chat(self, query: str, show_thought: bool = True) -> str:
        """对话"""
        self.thought_process = []
        if show_thought:
            self.thought_process.append("<think>")
        
        if self.model:
            return self._model_chat(query, show_thought)
        return self._fallback_chat(query, show_thought)
    
    def _model_chat(self, query: str, show_thought: bool) -> str:
        """模型推理"""
        try:
            import torch
            messages = [{"role": "user", "content": query}]
            text = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
            inputs = self.tokenizer.encode(text, return_tensors="pt")
            with torch.no_grad():
                outputs = self.model.generate(inputs, max_new_tokens=512, temperature=0.7, do_sample=True)
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            if show_thought:
                self.thought_process.append("</think>")
            return "\n".join(self.thought_process) + "\n\n" + response
        except Exception as e:
            return self._fallback_chat(query, show_thought)
    
    def _fallback_chat(self, query: str, show_thought: bool) -> str:
        """备用回复"""
        responses = {
            "你好": "你好！有什么可以帮你的？",
            "饿": "去吃点东西吧，别饿坏了～",
            "累": "辛苦了，休息一下吧",
            "工作": "工作加油，但也别太累了",
            "学习": "学习进步中，继续加油！",
        }
        for key, val in responses.items():
            if key in query:
                if show_thought:
                    self.thought_process.append(f"匹配关键词：{key}")
                    self.thought_process.append("</think>")
                return "\n".join(self.thought_process) + "\n\n" + val
        if show_thought:
            self.thought_process.append("未匹配预设回复")
            self.thought_process.append("</think>")
        return "\n".join(self.thought_process) + "\n\n" + "这是一个有趣的问题，能再多说点细节吗？"
    
    def get_daily_tip(self) -> str:
        tips = ["今天也要加油哦～", "注意休息，别太累了", "保持好心情！"]
        return tips[datetime.now().weekday() % len(tips)]
