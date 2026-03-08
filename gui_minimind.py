#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
zhangy chat - MiniMind 模型版本
"""

import tkinter as tk
from tkinter import scrolledtext
import threading
from zhangy_chat.minimind_assistant import MiniMindAssistant


class MiniMindGUI:
    """MiniMind GUI"""

    def __init__(self, root):
        self.root = root
        self.root.title("zhangy chat - MiniMind 版")
        self.root.geometry("900x650")

        # 初始化助手
        self.assistant = MiniMindAssistant()

        # 创建界面
        self._create_widgets()

    def _create_widgets(self):
        """创建界面"""
        # 标题
        title = tk.Label(
            self.root,
            text="zhangy chat",
            font=("Microsoft YaHei", 14, "bold"),
            bg="#1a1a2e",
            fg="white"
        )
        title.pack(fill=tk.X)
        title.pack_propagate(False)

        # 主内容区
        main = tk.Frame(self.root, bg="#0f0f23")
        main.pack(fill=tk.BOTH, expand=True)

        # 左侧思考区
        thought_frame = tk.LabelFrame(main, text="思考过程", font=("Microsoft YaHei", 10), bg="#0f0f23", fg="#00ff00")
        thought_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.thought_text = scrolledtext.ScrolledText(
            thought_frame, wrap=tk.WORD, font=("Consolas", 9),
            bg="#0d1117", fg="#00ff00", padx=10, pady=10
        )
        self.thought_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 右侧对话区
        chat_frame = tk.Frame(main, bg="#0f0f23")
        chat_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.chat_display = scrolledtext.ScrolledText(
            chat_frame, wrap=tk.WORD, font=("Microsoft YaHei", 10),
            bg="#161b22", fg="#c9d1d9", padx=10, pady=10
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        self.chat_display.config(state=tk.DISABLED)

        # 输入区
        input_frame = tk.Frame(chat_frame, bg="#0f0f23")
        input_frame.pack(fill=tk.X)

        tk.Label(input_frame, text="输入:", font=("Microsoft YaHei", 10), bg="#0f0f23", fg="#c9d1d9").pack(anchor=tk.W)

        self.input_text = tk.Text(input_frame, height=4, font=("Microsoft YaHei", 10), bg="#161b22", fg="#c9d1d9", padx=5, pady=5)
        self.input_text.pack(fill=tk.X, pady=5)
        self.input_text.bind("<Return>", lambda e: self.send_message())

        # 按钮
        btn_frame = tk.Frame(input_frame, bg="#0f0f23")
        btn_frame.pack(fill=tk.X)

        tk.Button(btn_frame, text="发送", command=self.send_message, bg="#238636", fg="white", padx=20, pady=5).pack(side=tk.RIGHT)
        tk.Button(btn_frame, text="清空", command=self.clear_chat, bg="#da3633", fg="white", padx=20, pady=5).pack(side=tk.RIGHT, padx=5)

        self.show_thought_var = tk.BooleanVar(value=True)
        tk.Checkbutton(btn_frame, text="显示思考", variable=self.show_thought_var, bg="#0f0f23", fg="#c9d1d9").pack(side=tk.LEFT, padx=10)

        # 状态栏
        status = tk.Frame(self.root, bg="#1a1a2e", height=30)
        status.pack(fill=tk.X)
        self.status_label = tk.Label(status, text="就绪", font=("Microsoft YaHei", 9), bg="#1a1a2e", fg="#8b949e")
        self.status_label.pack(side=tk.LEFT, padx=10)

    def send_message(self):
        """发送消息"""
        user_input = self.input_text.get("1.0", tk.END).strip()
        if not user_input:
            return

        self.input_text.delete("1.0", tk.END)
        self._add_chat("用户", user_input, "#58a6ff")
        self.thought_text.delete("1.0", tk.END)
        self.status_label.config(text="思考中...")

        show_thought = self.show_thought_var.get()
        thread = threading.Thread(target=self._process_response, args=(user_input, show_thought))
        thread.start()

    def _process_response(self, user_input: str, show_thought: bool):
        """处理响应"""
        try:
            response = self.assistant.chat(user_input, show_thought=show_thought)
            if show_thought and self.assistant.thought_process:
                self.root.after(0, self._update_thought, self.assistant.thought_process)
            self.root.after(0, lambda: self._add_chat(self.assistant.__class__.__name__, response, "#7ee787"))
        except Exception as e:
            self.root.after(0, lambda: self._add_chat("系统", f"错误：{e}", "#f85149"))
        finally:
            self.root.after(0, lambda: self.status_label.config(text="就绪"))

    def _update_thought(self, thoughts):
        """更新思考"""
        self.thought_text.delete("1.0", tk.END)
        for line in thoughts:
            tag = "tag" if line in ["<think>", "</think>"] else ""
            self.thought_text.insert(tk.END, line + "\n", tag)
        self.thought_text.tag_config("tag", foreground="#ff7b72", font=("Consolas", 9, "bold"))
        self.thought_text.see(tk.END)

    def _add_chat(self, sender: str, message: str, color: str):
        """添加聊天"""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"\n{sender}:\n", ("sender",))
        self.chat_display.insert(tk.END, f"{message}\n\n", ("message",))
        self.chat_display.tag_config("sender", font=("Microsoft YaHei", 10, "bold"), foreground=color)
        self.chat_display.tag_config("message", font=("Microsoft YaHei", 10), foreground="#c9d1d9")
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)

    def clear_chat(self):
        """清空"""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete("1.0", tk.END)
        self.chat_display.config(state=tk.DISABLED)
        self.thought_text.delete("1.0", tk.END)


def main():
    root = tk.Tk()
    app = MiniMindGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
