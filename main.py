#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Zhangy Chat - 主程序入口
支持 GUI 和 CMD 双模式
"""

import argparse
import sys
import yaml
from pathlib import Path

from zhangy_chat import ZhangyChat, TaskManager, DataManager, Assistant


def load_config(config_path="config.yaml"):
    """加载配置文件"""
    config_file = Path(config_path)
    if config_file.exists():
        with open(config_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    return {}


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="Zhangy Chat - 专业 AI 助手")
    parser.add_argument('-cmd', '--cmd', action='store_true', help='启动 CMD 模式')
    parser.add_argument('-c', '--config', type=str, default='config.yaml', help='配置文件路径')
    args = parser.parse_args()
    
    config = load_config(args.config)
    default_mode = config.get('ui', {}).get('default_mode', 'gui')
    
    if args.cmd or default_mode == 'cmd':
        # 启动 CMD 模式
        from zhangy_chat.cmd_interface import CMDInterface
        print("=" * 50)
        print("  Zhangy Chat - CMD 模式")
        print("  输入 /help 查看指令，/gui 切换图形界面，exit 退出")
        print("=" * 50)
        
        interface = CMDInterface()
        interface.run()
    else:
        # 启动 GUI 模式
        import subprocess
        subprocess.Popen([sys.executable, "gui.py"])


if __name__ == "__main__":
    main()
