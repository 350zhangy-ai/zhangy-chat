#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
zhangy chat - 图形界面 (R3 MiniMind 风格思考可见版)
思考过程使用 <think></think> 标签包裹，类似 MiniMind-R1
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox
import yaml
from pathlib import Path
import threading
from datetime import datetime

# 导入核心模块（R3 MiniMind 风格）
from zhangy_chat.task_manager import TaskManager
from zhangy_chat.data_manager import DataManager
from zhangy_chat.assistant_r3_minimind import Assistant
from zhangy_chat.memory_manager import MemoryManager
from zhangy_chat.mood_manager import MoodManager
from zhangy_chat.preset_manager import PresetManager


class ZhangyChatGUI:
    """zhangy chat 图形界面 (R3 MiniMind 风格思考可见版)"""

    def __init__(self, root):
        self.root = root
        self.root.title("zhangy chat R3 - MiniMind 风格思考可见")
        self.root.geometry("1100x750")

        # 加载配置
        self.config = self._load_config()
        self.name = self.config.get('name', 'zhangy chat')

        # 初始化核心模块
        self.task_manager = TaskManager()
        self.data_manager = DataManager()
        self.memory_manager = MemoryManager()
        self.mood_manager = MoodManager()
        self.preset_manager = PresetManager()

        # 初始化助手
        self.assistant = Assistant(
            mood_manager=self.mood_manager,
            preset_manager=self.preset_manager
        )

        # 创建界面
        self._create_widgets()

    def _load_config(self):
        config_file = Path("config.yaml")
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        return {}

    def _create_widgets(self):
        """创建界面组件"""
        # 顶部标题栏
        title_frame = tk.Frame(self.root, bg="#1a1a2e", height=50)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)

        tk.Label(
            title_frame,
            text=f"  {self.name}  R3 - MiniMind 思考可见版",
            font=("Microsoft YaHei", 14, "bold"),
            bg="#1a1a2e",
            fg="white"
        ).pack(side=tk.LEFT, padx=10, pady=10)

        # 主内容区 - 左右分栏
        main_frame = tk.Frame(self.root, bg="#0f0f23")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 左侧：思考过程显示区（类似终端风格）
        thought_frame = tk.LabelFrame(
            main_frame, 
            text="💭 思考过程 (CoT)", 
            font=("Microsoft YaHei", 10, "bold"), 
            bg="#0f0f23",
            fg="#00ff00"
        )
        thought_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.thought_text = scrolledtext.ScrolledText(
            thought_frame,
            wrap=tk.WORD,
            font=("Consolas", 9),
            bg="#0d1117",
            fg="#00ff00",
            padx=10,
            pady=10,
            insertbackground="#00ff00"
        )
        self.thought_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 右侧：对话区
        chat_frame = tk.Frame(main_frame, bg="#0f0f23")
        chat_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 聊天记录（深色主题）
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            font=("Microsoft YaHei", 10),
            bg="#161b22",
            fg="#c9d1d9",
            padx=10,
            pady=10,
            insertbackground="#c9d1d9"
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        self.chat_display.config(state=tk.DISABLED)

        # 输入区
        input_frame = tk.Frame(chat_frame, bg="#0f0f23")
        input_frame.pack(fill=tk.X)

        tk.Label(
            input_frame, 
            text="输入问题:", 
            font=("Microsoft YaHei", 10), 
            bg="#0f0f23",
            fg="#c9d1d9"
        ).pack(anchor=tk.W)

        self.input_text = tk.Text(
            input_frame, 
            height=4, 
            font=("Microsoft YaHei", 10),
            bg="#161b22",
            fg="#c9d1d9",
            insertbackground="#c9d1d9",
            padx=5, 
            pady=5
        )
        self.input_text.pack(fill=tk.X, pady=5)
        self.input_text.bind("<Return>", lambda e: self.send_message())

        # 按钮区
        btn_frame = tk.Frame(input_frame, bg="#0f0f23")
        btn_frame.pack(fill=tk.X)

        tk.Button(
            btn_frame, 
            text="发送", 
            command=self.send_message,
            bg="#238636", 
            fg="white", 
            padx=20, 
            pady=5,
            relief=tk.FLAT
        ).pack(side=tk.RIGHT)

        tk.Button(
            btn_frame, 
            text="清空", 
            command=self.clear_chat,
            bg="#da3633", 
            fg="white", 
            padx=20, 
            pady=5,
            relief=tk.FLAT
        ).pack(side=tk.RIGHT, padx=5)

        # 思考开关
        self.show_thought_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            btn_frame, 
            text="显示思考过程",
            variable=self.show_thought_var,
            bg="#0f0f23", 
            fg="#c9d1d9",
            font=("Microsoft YaHei", 10),
            selectcolor="#161b22",
            activebackground="#0f0f23",
            activeforeground="#c9d1d9"
        ).pack(side=tk.LEFT, padx=10)

        # 底部状态栏
        status_frame = tk.Frame(self.root, bg="#1a1a2e", height=30)
        status_frame.pack(fill=tk.X)

        self.status_label = tk.Label(
            status_frame, 
            text="就绪", 
            font=("Microsoft YaHei", 9),
            bg="#1a1a2e", 
            fg="#8b949e"
        )
        self.status_label.pack(side=tk.LEFT, padx=10)

        self.tip_label = tk.Label(
            status_frame, 
            text=self.assistant.get_daily_tip(), 
            font=("Microsoft YaHei", 9),
            bg="#1a1a2e", 
            fg="#3fb950"
        )
        self.tip_label.pack(side=tk.RIGHT, padx=10)

    def send_message(self):
        """发送消息"""
        user_input = self.input_text.get("1.0", tk.END).strip()
        if not user_input:
            return

        self.input_text.delete("1.0", tk.END)
        self._add_chat_message("用户", user_input, "#58a6ff")

        # 清空思考区
        self.thought_text.delete("1.0", tk.END)
        self.thought_text.config(state=tk.NORMAL)

        # 更新状态
        self.status_label.config(text="思考中...")

        # 在新线程处理
        show_thought = self.show_thought_var.get()
        thread = threading.Thread(target=self._process_response, args=(user_input, show_thought))
        thread.start()

    def _process_response(self, user_input: str, show_thought: bool):
        """处理响应"""
        try:
            # 获取回复（带思考过程）
            response = self.assistant.chat(user_input, show_thought=show_thought)

            # 更新思考区
            if show_thought and self.assistant.thought_process:
                self.root.after(0, self._update_thought, self.assistant.thought_process)

            # 更新聊天区
            self.root.after(0, lambda: self._add_chat_message(self.name, response, "#7ee787"))
        except Exception as e:
            self.root.after(0, lambda: self._add_chat_message("系统", f"错误：{e}", "#f85149"))
        finally:
            self.root.after(0, lambda: self.status_label.config(text="就绪"))

    def _update_thought(self, thought_process):
        """更新思考过程显示"""
        self.thought_text.delete("1.0", tk.END)
        for line in thought_process:
            # 高亮 <think> 和</think> 标签
            if line == "<think>":
                self.thought_text.insert(tk.END, line + "\n", "thought_tag")
            elif line == "</think>":
                self.thought_text.insert(tk.END, line + "\n", "thought_tag")
            else:
                self.thought_text.insert(tk.END, line + "\n")
        
        # 配置标签样式
        self.thought_text.tag_config("thought_tag", foreground="#ff7b72", font=("Consolas", 9, "bold"))
        self.thought_text.see(tk.END)

    def _add_chat_message(self, sender: str, message: str, color: str):
        """添加聊天消息"""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"\n{sender}:\n", ("sender",))
        self.chat_display.insert(tk.END, f"{message}\n\n", ("message",))

        self.chat_display.tag_config("sender", font=("Microsoft YaHei", 10, "bold"), foreground=color)
        self.chat_display.tag_config("message", font=("Microsoft YaHei", 10), foreground="#c9d1d9")

        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)

    def clear_chat(self):
        """清空聊天"""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete("1.0", tk.END)
        self.chat_display.config(state=tk.DISABLED)
        self.thought_text.delete("1.0", tk.END)


def main():
    root = tk.Tk()
    app = ZhangyChatGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
