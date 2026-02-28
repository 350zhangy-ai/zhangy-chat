#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
zhangy chat - 图形界面版本
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox
import yaml
from pathlib import Path
import threading


class ZhangyChatGUI:
    """zhangy chat 图形界面类"""

    def __init__(self, root):
        """初始化GUI"""
        self.root = root
        self.root.title("zhangy chat - 专业AI助手")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)

        # 加载配置
        self.config = self._load_config()
        self.name = self.config.get('name', 'zhangy chat')

        # 创建界面
        self._create_widgets()

    def _load_config(self):
        """加载配置文件"""
        config_file = Path("config.yaml")
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        return {}

    def _create_widgets(self):
        """创建界面组件"""
        # 顶部标题栏
        title_frame = tk.Frame(self.root, bg="#2c3e50", height=50)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)

        title_label = tk.Label(
            title_frame,
            text=f"  {self.name}",
            font=("Microsoft YaHei", 16, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title_label.pack(side=tk.LEFT, padx=10, pady=10)

        # 主内容区域
        main_frame = tk.Frame(self.root, bg="#ecf0f1")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 聊天记录显示区域
        chat_frame = tk.Frame(main_frame, bg="#ecf0f1")
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            font=("Microsoft YaHei", 10),
            bg="white",
            fg="#2c3e50",
            padx=10,
            pady=10
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        self.chat_display.config(state=tk.DISABLED)

        # 输入区域
        input_frame = tk.Frame(main_frame, bg="#ecf0f1")
        input_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        tk.Label(
            input_frame,
            text="输入问题:",
            font=("Microsoft YaHei", 10),
            bg="#ecf0f1",
            fg="#2c3e50"
        ).pack(anchor=tk.W)

        self.input_text = tk.Text(
            input_frame,
            height=4,
            font=("Microsoft YaHei", 10),
            bg="white",
            fg="#2c3e50",
            padx=5,
            pady=5
        )
        self.input_text.pack(fill=tk.X, pady=5)
        self.input_text.bind("<Return>", lambda e: self.send_message())

        # 按钮区域
        button_frame = tk.Frame(main_frame, bg="#ecf0f1")
        button_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        send_btn = tk.Button(
            button_frame,
            text="发送",
            command=self.send_message,
            font=("Microsoft YaHei", 10),
            bg="#3498db",
            fg="white",
            activebackground="#2980b9",
            activeforeground="white",
            relief=tk.FLAT,
            padx=20,
            pady=8
        )
        send_btn.pack(side=tk.RIGHT)

        clear_btn = tk.Button(
            button_frame,
            text="清空",
            command=self.clear_chat,
            font=("Microsoft YaHei", 10),
            bg="#e74c3c",
            fg="white",
            activebackground="#c0392b",
            activeforeground="white",
            relief=tk.FLAT,
            padx=20,
            pady=8
        )
        clear_btn.pack(side=tk.RIGHT, padx=5)

        # 底部状态栏
        status_frame = tk.Frame(self.root, bg="#2c3e50", height=30)
        status_frame.pack(fill=tk.X)
        status_frame.pack_propagate(False)

        self.status_label = tk.Label(
            status_frame,
            text="就绪",
            font=("Microsoft YaHei", 9),
            bg="#2c3e50",
            fg="#bdc3c7"
        )
        self.status_label.pack(side=tk.LEFT, padx=10)

    def send_message(self):
        """发送消息"""
        user_input = self.input_text.get("1.0", tk.END).strip()
        if not user_input:
            return

        # 清空输入框
        self.input_text.delete("1.0", tk.END)

        # 显示用户消息
        self._add_message("用户", user_input, "#3498db")

        # 更新状态
        self.status_label.config(text="正在思考...")

        # 在新线程中处理响应
        thread = threading.Thread(target=self._process_response, args=(user_input,))
        thread.start()

    def _process_response(self, user_input):
        """处理响应"""
        try:
            response = self._generate_response(user_input)
            self.root.after(0, lambda: self._add_message(self.name, response, "#2c3e50"))
        except Exception as e:
            self.root.after(0, lambda: self._add_message("系统", f"错误: {str(e)}", "#e74c3c"))
        finally:
            self.root.after(0, lambda: self.status_label.config(text="就绪"))

    def _generate_response(self, query):
        """生成回答"""
        personality_name = self.config.get('personality', {}).get('name', 'zhangy')
        personality_traits = ', '.join(self.config.get('personality', {}).get('性格', ['专业', '高效']))

        return f"""## {personality_name} 分析

**问题**: {query}

### 解决方案

针对您的问题，建议如下：

1. **诊断分析**: 识别问题的关键因素
2. **执行方案**: 提供具体可操作的步骤
3. **验证方法**: 确保方案有效性

### 实施建议

请根据上述方案执行，如需进一步协助，请提供更多细节。

---
*{personality_traits} AI助手*
"""

    def _add_message(self, sender, message, color):
        """添加消息到聊天记录"""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"\n{sender}:\n", ("sender",))
        self.chat_display.insert(tk.END, f"{message}\n\n", ("message",))

        # 配置标签样式
        self.chat_display.tag_config("sender", font=("Microsoft YaHei", 10, "bold"), foreground=color)
        self.chat_display.tag_config("message", font=("Microsoft YaHei", 10), foreground="#2c3e50")

        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)

    def clear_chat(self):
        """清空聊天记录"""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete("1.0", tk.END)
        self.chat_display.config(state=tk.DISABLED)


def main():
    """主函数"""
    root = tk.Tk()
    app = ZhangyChatGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()