#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
zhangy-chat 模型加载器
使用 Qwen2.5-0.5B 开源模型
"""

import os


class ZhangyChatModel:
    """zhangy-chat 模型类（使用 Qwen2.5-0.5B）"""
    
    def __init__(self, model_name: str = None):
        self.model_name = model_name or "Qwen/Qwen2.5-0.5B-Instruct"
        self.model = None
        self.tokenizer = None
        self.device = "cuda" if self._check_gpu() else "cpu"
        
    def _check_gpu(self):
        """检查 GPU"""
        try:
            import torch
            return torch.cuda.is_available()
        except:
            return False
        
    def load(self):
        """加载模型"""
        try:
            import torch
            from transformers import AutoModelForCausalLM, AutoTokenizer
            
            # 使用 ModelScope 国内镜像
            print(f"[zhangy-chat] 加载 zhangy-chat 模型...")
            print(f"[zhangy-chat] 设备：{self.device}")
            print("[zhangy-chat] 首次加载需要下载模型（约 1GB），请耐心等待...")
            
            # 设置使用 ModelScope
            os.environ['TRANSFORMERS_OFFLINE'] = '0'
            
            # 尝试从 ModelScope 加载
            try:
                from modelscope import snapshot_download
                # 下载 Qwen2.5-0.5B 作为 zhangy-chat 模型
                print("[zhangy-chat] 正在从 ModelScope 下载 zhangy-chat 模型...")
                model_dir = snapshot_download('qwen/Qwen2.5-0.5B-Instruct')
                
                self.tokenizer = AutoTokenizer.from_pretrained(
                    model_dir,
                    trust_remote_code=True
                )
                
                self.model = AutoModelForCausalLM.from_pretrained(
                    model_dir,
                    trust_remote_code=True,
                    torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                    device_map="auto" if self.device == "cuda" else None
                )
            except ImportError:
                print("[zhangy-chat] 未安装 modelscope，尝试从 HuggingFace 加载...")
                # 备用方案：使用 HuggingFace 镜像
                self.tokenizer = AutoTokenizer.from_pretrained(
                    "Qwen/Qwen2.5-0.5B-Instruct",
                    trust_remote_code=True,
                    mirror='modelscope'
                )
                
                self.model = AutoModelForCausalLM.from_pretrained(
                    "Qwen/Qwen2.5-0.5B-Instruct",
                    trust_remote_code=True,
                    torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                    device_map="auto" if self.device == "cuda" else None
                )
            
            print("[zhangy-chat] zhangy-chat 模型加载成功！")
            return True
            
        except Exception as e:
            print(f"[zhangy-chat] 加载失败：{e}")
            print("[zhangy-chat] 将使用知识库模式")
            return False
    
    def generate(self, text: str, max_length: int = 512) -> str:
        """生成回复"""
        if not self.model or not self.tokenizer:
            return None
        
        try:
            import torch
            
            messages = [
                {"role": "system", "content": "你是 zhangy-chat，AI 助手。"},
                {"role": "user", "content": text}
            ]
            
            prompt = self.tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True
            )
            
            inputs = self.tokenizer(prompt, return_tensors="pt")
            if self.device == "cuda":
                inputs = {k: v.to("cuda") for k, v in inputs.items()}
            
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_length,
                temperature=0.7,
                do_sample=True
            )
            
            response = self.tokenizer.decode(
                outputs[0][inputs['input_ids'].shape[1]:],
                skip_special_tokens=True
            )
            
            return response.strip()
            
        except Exception as e:
            print(f"[zhangy-chat] 生成失败：{e}")
            return None
