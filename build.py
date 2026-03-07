#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Zhangy Chat R2 - 打包脚本
支持 GUI 和 CMD 双模式打包
"""

import sys
import os
import shutil

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

try:
    import PyInstaller
    pyinstaller_available = True
except ImportError:
    pyinstaller_available = False


def build_all():
    """打包所有版本"""
    if not pyinstaller_available:
        print("PyInstaller 未安装，正在安装...")
        os.system("pip install pyinstaller")
    
    print("=" * 50)
    print("  Zhangy Chat R2 - 打包工具")
    print("=" * 50)
    
    # 清理旧的 build 目录
    if os.path.exists("build"):
        shutil.rmtree("build")
    
    # 打包 GUI 版本
    print("\n[1/2] 打包 GUI 版本...")
    build_gui()
    
    # 打包 CMD 版本
    print("\n[2/2] 打包 CMD 版本...")
    build_cmd()
    
    print("\n" + "=" * 50)
    print("打包完成！")
    print("GUI 版本：dist/zhangy_chat_gui.exe")
    print("CMD 版本：dist/zhangy_chat_cmd.exe")
    print("=" * 50)


def build_gui():
    """打包 GUI 版本"""
    cmd = [
        "pyinstaller",
        "--name=zhangy_chat_gui",
        "--onefile",
        "--windowed",
        "--add-data=config.yaml;.",
        "--hidden-import=yaml",
        "--hidden-import=tkinter",
        "--hidden-import=zhangy_chat",
        "--hidden-import=zhangy_chat.task_manager",
        "--hidden-import=zhangy_chat.data_manager",
        "--hidden-import=zhangy_chat.assistant",
        "gui.py"
    ]
    os.system(" ".join(cmd))


def build_cmd():
    """打包 CMD 版本"""
    cmd = [
        "pyinstaller",
        "--name=zhangy_chat_cmd",
        "--onefile",
        "--console",
        "--add-data=config.yaml;.",
        "--hidden-import=yaml",
        "--hidden-import=zhangy_chat",
        "--hidden-import=zhangy_chat.task_manager",
        "--hidden-import=zhangy_chat.data_manager",
        "--hidden-import=zhangy_chat.assistant",
        "--hidden-import=zhangy_chat.cmd_interface",
        "main.py"
    ]
    os.system(" ".join(cmd))


if __name__ == "__main__":
    build_all()
