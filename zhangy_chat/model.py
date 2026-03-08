#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
zhangy-chat 模型加载器
基于 MiniMind 架构，支持本地部署
"""

import os
import sys


class ZhangyChatModel:
    """zhangy-chat 模型类（基于 MiniMind）"""
    
    def __init__(self, model_dir: str = None):
        if model_dir is None:
            model_dir = os.path.join(
                os.path.dirname(os.path.dirname(__file__)), 
                "models", "zhangy-chat"
            )
        self.model_dir = model_dir
        self.model = None
        self.tokenizer = None
        self.device = "cpu"
        
    def load(self):
        """加载模型"""
        try:
            import torch
            
            # 创建模型目录
            os.makedirs(self.model_dir, exist_ok=True)
            
            # 查找模型文件
            model_files = [
                "full_sft_768.pth",
                "full_sft_512.pth", 
                "grpo_768.pth",
                "model.pth"
            ]
            
            model_path = None
            for f in model_files:
                path = os.path.join(self.model_dir, f)
                if os.path.exists(path):
                    model_path = path
                    print(f"[zhangy-chat] 找到模型文件：{f}")
                    break
            
            if model_path:
                # 加载模型
                try:
                    # PyTorch 2.6+ 需要 weights_only=False
                    self.model = torch.load(
                        model_path,
                        map_location=self.device,
                        weights_only=False
                    )
                    print("[zhangy-chat] 模型加载成功！")
                    return True
                except Exception as e:
                    print(f"[zhangy-chat] 模型加载失败：{e}")
                    print("[zhangy-chat] 将使用知识库模式")
                    return False
            else:
                print(f"[zhangy-chat] 未在 {self.model_dir} 找到模型文件")
                print("[zhangy-chat] 将使用知识库模式")
                return False
                
        except Exception as e:
            print(f"[zhangy-chat] 模型加载失败：{e}")
            print("[zhangy-chat] 将使用知识库模式")
            return False
    
    def generate(self, text: str, max_length: int = 512) -> str:
        """生成回复"""
        if self.model is None:
            return None
            
        try:
            import torch
            
            # 如果有 tokenizer
            if self.tokenizer:
                messages = [{"role": "user", "content": text}]
                prompt = self.tokenizer.apply_chat_template(
                    messages,
                    tokenize=False,
                    add_generation_prompt=True
                )
                inputs = self.tokenizer.encode(
                    prompt,
                    return_tensors="pt"
                ).to(self.device)
                
                with torch.no_grad():
                    outputs = self.model.generate(
                        inputs,
                        max_new_tokens=max_length,
                        temperature=0.7,
                        do_sample=True
                    )
                
                response = self.tokenizer.decode(
                    outputs[0],
                    skip_special_tokens=True
                )
                return response
            
            # 没有 tokenizer 时返回 None，使用知识库
            return None
            
        except Exception as e:
            print(f"[zhangy-chat] 生成失败：{e}")
            return None
    
    def download_model(self, repo: str = "jingyaogong/minimind"):
        """从 HuggingFace 下载模型"""
        print(f"[zhangy-chat] 正在从 {repo} 下载模型...")
        
        try:
            from huggingface_hub import snapshot_download
            
            # 下载到模型目录
            snapshot_download(
                repo_id=repo,
                local_dir=self.model_dir,
                local_dir_use_symlinks=False
            )
            
            print(f"[zhangy-chat] 模型下载完成：{self.model_dir}")
            return True
            
        except ImportError:
            print("[zhangy-chat] 需要安装 huggingface_hub:")
            print("  pip install huggingface_hub")
            return False
        except Exception as e:
            print(f"[zhangy-chat] 下载失败：{e}")
            print("[zhangy-chat] 请手动下载模型到:", self.model_dir)
            return False


def main():
    """主函数"""
    print("=" * 50)
    print("  zhangy-chat 模型加载器")
    print("=" * 50)
    
    model = ZhangyChatModel()
    
    # 尝试加载模型
    if model.load():
        print("\n模型已就绪，可以开始对话！")
    else:
        print("\n使用知识库模式，无需模型文件")
    
    # 简单测试
    print("\n输入 'exit' 退出")
    while True:
        try:
            user_input = input("\n你：").strip()
            if user_input.lower() in ['exit', 'quit', '退出']:
                print("再见！")
                break
            if not user_input:
                continue
            
            # 这里只是测试，实际使用通过 Assistant 类
            print("zhangy-chat：这是一个测试回复")
            
        except KeyboardInterrupt:
            print("\n再见！")
            break


if __name__ == "__main__":
    main()
