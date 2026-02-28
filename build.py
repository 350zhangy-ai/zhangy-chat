#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
zhangy chat - 打包脚本
"""

import sys
import os

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

try:
    import PyInstaller
    pyinstaller_available = True
except ImportError:
    pyinstaller_available = False

def build_exe():
    """打包为EXE文件"""
    if not pyinstaller_available:
        print("PyInstaller未安装，正在安装...")
        os.system("pip install pyinstaller")

    print("开始打包...")
    
    cmd = [
        "pyinstaller",
        "--name=zhangy_chat",
        "--onefile",
        "--windowed",
        "--icon=NONE",
        "--add-data=config.yaml;.",
        "--add-data=prompt_template.txt;.",
        "--hidden-import=yaml",
        "--hidden-import=transformers",
        "main.py"
    ]
    
    os.system(" ".join(cmd))
    print("打包完成！EXE文件位于 dist/zhangy_chat.exe")

if __name__ == "__main__":
    build_exe()