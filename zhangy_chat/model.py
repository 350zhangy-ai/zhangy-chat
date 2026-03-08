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
                # 尝试加载 HuggingFace tokenizer
                try:
                    from transformers import AutoTokenizer
                    
                    # 加载 tokenizer
                    self.tokenizer = AutoTokenizer.from_pretrained(
                        self.model_dir,
                        trust_remote_code=True
                    )
                    print("[zhangy-chat] HuggingFace Tokenizer 已加载")
                    
                    # 加载模型
                    from .minimind_model import load_model
                    self.model = load_model(model_path, self.device)
                    
                    if self.model:
                        print("[zhangy-chat] 模型已加载")
                        print("[zhangy-chat] 但由于模型权重与 tokenizer 可能不匹配，将使用知识库模式")
                        print("[zhangy-chat] 如需使用模型推理，请确保模型权重与 tokenizer 来自同一版本")
                        self.model = None  # 禁用模型推理
                        return False
                    else:
                        print("[zhangy-chat] 模型加载失败")
                        return False
                        
                except Exception as e:
                    print(f"[zhangy-chat] Tokenizer 加载失败：{e}")
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
        # 由于模型权重与 tokenizer 可能不匹配，推理输出可能为乱码
        # 直接返回 None，使用知识库模式
        print("[zhangy-chat] 模型推理已禁用，使用知识库模式")
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
