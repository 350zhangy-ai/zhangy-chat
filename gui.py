#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
zhangy chat - 图形界面版本 (R3 美化版)
现代、简洁、优雅的 UI 设计，类似豆包/微信风格
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import yaml
from pathlib import Path
import threading
import subprocess
import sys
import json
from datetime import datetime

# 导入核心模块
from zhangy_chat.task_manager import TaskManager
from zhangy_chat.data_manager import DataManager
from zhangy_chat.assistant import Assistant
from zhangy_chat.memory_manager import MemoryManager
from zhangy_chat.mood_manager import MoodManager
from zhangy_chat.preset_manager import PresetManager
from zhangy_chat.external_ai import ExternalAI, AI_PROVIDERS


# ==================== 豆包风格配色 ====================
class Colors:
    """配色方案"""
    # 主色调
    PRIMARY = "#5B8FF9"        # 豆包蓝
    PRIMARY_LIGHT = "#E8F3FF"  # 浅蓝背景
    PRIMARY_DARK = "#3A78E8"   # 深蓝
    
    # 背景色
    BG_MAIN = "#FFFFFF"        # 主背景
    BG_SECONDARY = "#F5F7FA"   # 次级背景
    BG_CHAT = "#F5F7FA"        # 聊天背景
    BG_SIDEBAR = "#F7F7F7"     # 侧边栏背景
    BG_HOVER = "#EBF5FF"       # 悬停背景
    
    # 文字色
    TEXT_PRIMARY = "#1F2329"   # 主文字
    TEXT_SECONDARY = "#646A73" # 次级文字
    TEXT_HINT = "#9DA5AE"      # 提示文字
    
    # 功能色
    SUCCESS = "#00B365"        # 成功绿
    WARNING = "#FF7D00"        # 警告橙
    ERROR = "#F53F3F"          # 错误红
    INFO = "#5B8FF9"           # 信息蓝
    
    # 边框色
    BORDER = "#DEE3EA"         # 边框灰
    BORDER_LIGHT = "#EFF1F5"   # 浅边框
    
    # 用户消息
    USER_BG = "#5B8FF9"        # 用户消息背景
    USER_TEXT = "#FFFFFF"      # 用户消息文字
    
    # AI 消息
    AI_BG = "#FFFFFF"          # AI 消息背景
    AI_TEXT = "#1F2329"        # AI 消息文字


class ZhangyChatGUI:
    """zhangy chat 图形界面类 (R3 美化版)"""

    def __init__(self, root):
        """初始化 GUI"""
        self.root = root
        self.root.title("zhangy-chat R3")
        self.root.geometry("1280x800")
        self.root.minsize(1000, 700)

        # 加载配置
        self.config = self._load_config()
        self.name = "zhangy-chat"

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
        
        # 初始化外部 AI
        self.external_ai = ExternalAI()
        self.use_external_ai = False

        # 聊天记录
        self.chat_history = []
        self.current_chat_id = "default"
        self.chats = {}  # 存储多个对话
        
        # 深度思考开关
        self.deep_thinking_var = tk.BooleanVar(value=False)

        # 创建界面
        self._create_widgets()
        self._load_initial_data()

    def _load_config(self):
        """加载配置文件"""
        config_file = Path("config.yaml")
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        return {}

    def _create_widgets(self):
        """创建界面组件 - 现代风格"""
        self.root.configure(bg=Colors.BG_SECONDARY)
        
        # ==================== 主容器（左右布局）====================
        main_container = tk.PanedWindow(self.root, orient=tk.HORIZONTAL, bg=Colors.BORDER)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # ===== 左侧边栏 - 对话列表 =====
        sidebar_frame = tk.Frame(main_container, bg=Colors.BG_SIDEBAR, width=280)
        main_container.add(sidebar_frame)
        self._create_sidebar(sidebar_frame)
        
        # ===== 右侧主聊天区 =====
        chat_main_frame = tk.Frame(main_container, bg=Colors.BG_MAIN)
        main_container.add(chat_main_frame)
        self._create_chat_area(chat_main_frame)

    def _create_sidebar(self, parent):
        """创建左侧边栏"""
        # 顶部标题栏
        header_frame = tk.Frame(parent, bg=Colors.PRIMARY, height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        # Logo
        logo_label = tk.Label(
            header_frame,
            text="💬 zhangy-chat",
            font=("Microsoft YaHei", 16, "bold"),
            bg=Colors.PRIMARY,
            fg="white"
        )
        logo_label.pack(side=tk.LEFT, padx=15, pady=15)
        
        # 新建对话按钮
        new_chat_btn = tk.Button(
            header_frame,
            text="➕",
            command=self._new_chat,
            font=("Microsoft YaHei", 14),
            bg=Colors.PRIMARY,
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            padx=10
        )
        new_chat_btn.pack(side=tk.RIGHT, padx=10, pady=15)
        
        # 对话列表
        list_container = tk.Frame(parent, bg=Colors.BG_SIDEBAR)
        list_container.pack(fill=tk.BOTH, expand=True)
        
        # 对话列表标题
        tk.Label(
            list_container,
            text="最近对话",
            font=("Microsoft YaHei", 9, "bold"),
            bg=Colors.BG_SIDEBAR,
            fg=Colors.TEXT_SECONDARY
        ).pack(anchor=tk.W, padx=15, pady=10)
        
        # 对话列表框
        self.chat_list_frame = tk.Frame(list_container, bg=Colors.BG_SIDEBAR)
        self.chat_list_frame.pack(fill=tk.BOTH, expand=True)
        
        # 底部功能按钮
        bottom_frame = tk.Frame(parent, bg=Colors.BG_SIDEBAR, height=50)
        bottom_frame.pack(fill=tk.X)
        bottom_frame.pack_propagate(False)
        
        # CMD 模式按钮
        cmd_btn = tk.Button(
            bottom_frame,
            text="⌨️ CMD 模式",
            command=self._switch_to_cmd,
            font=("Microsoft YaHei", 9),
            bg=Colors.BG_SIDEBAR,
            fg=Colors.TEXT_PRIMARY,
            relief=tk.FLAT,
            cursor="hand2"
        )
        cmd_btn.pack(side=tk.LEFT, padx=15, pady=10)
        
        # 设置按钮
        settings_btn = tk.Button(
            bottom_frame,
            text="⚙️ 设置",
            command=self._open_settings,
            font=("Microsoft YaHei", 9),
            bg=Colors.BG_SIDEBAR,
            fg=Colors.TEXT_PRIMARY,
            relief=tk.FLAT,
            cursor="hand2"
        )
        settings_btn.pack(side=tk.RIGHT, padx=15, pady=10)

    def _create_chat_area(self, parent):
        """创建聊天区域"""
        # 顶部标题栏
        top_frame = tk.Frame(parent, bg=Colors.BG_MAIN, height=60)
        top_frame.pack(fill=tk.X)
        top_frame.pack_propagate(False)
        
        # 当前对话标题
        self.chat_title_label = tk.Label(
            top_frame,
            text="新对话",
            font=("Microsoft YaHei", 14, "bold"),
            bg=Colors.BG_MAIN,
            fg=Colors.TEXT_PRIMARY
        )
        self.chat_title_label.pack(side=tk.LEFT, padx=20, pady=15)
        
        # 深度思考开关
        think_frame = tk.Frame(top_frame, bg=Colors.BG_MAIN)
        think_frame.pack(side=tk.LEFT, padx=20, pady=15)
        
        self.deep_thinking_btn = tk.Checkbutton(
            think_frame,
            text="🧠 深度思考",
            variable=self.deep_thinking_var,
            font=("Microsoft YaHei", 9),
            bg=Colors.BG_MAIN,
            fg=Colors.TEXT_PRIMARY,
            selectcolor=Colors.PRIMARY_LIGHT
        )
        self.deep_thinking_btn.pack(side=tk.LEFT)
        
        # 清空对话按钮
        clear_btn = tk.Button(
            top_frame,
            text="🗑️ 清空",
            command=self.clear_chat,
            font=("Microsoft YaHei", 9),
            bg=Colors.BG_MAIN,
            fg=Colors.TEXT_SECONDARY,
            relief=tk.FLAT,
            cursor="hand2"
        )
        clear_btn.pack(side=tk.RIGHT, padx=15, pady=15)
        
        # 聊天内容显示区
        chat_container = tk.Frame(parent, bg=Colors.BG_CHAT)
        chat_container.pack(fill=tk.BOTH, expand=True)
        
        # 聊天记录
        self.chat_display = scrolledtext.ScrolledText(
            chat_container,
            wrap=tk.WORD,
            font=("Microsoft YaHei", 10),
            bg=Colors.BG_CHAT,
            fg=Colors.TEXT_PRIMARY,
            padx=0,
            pady=0,
            relief=tk.FLAT,
            borderwidth=0,
            highlightthickness=0
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        self.chat_display.config(state=tk.DISABLED)
        
        # 输入区域
        input_frame = tk.Frame(parent, bg=Colors.BG_MAIN, height=100)
        input_frame.pack(fill=tk.X)
        input_frame.pack_propagate(False)
        
        # 输入框容器
        input_container = tk.Frame(input_frame, bg=Colors.BG_MAIN)
        input_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        # 输入框
        self.input_text = tk.Text(
            input_container,
            height=3,
            font=("Microsoft YaHei", 10),
            bg=Colors.BG_SECONDARY,
            fg=Colors.TEXT_PRIMARY,
            padx=15,
            pady=12,
            relief=tk.FLAT,
            borderwidth=0,
            highlightthickness=1,
            highlightbackground=Colors.BORDER,
            insertbackground=Colors.PRIMARY
        )
        self.input_text.pack(fill=tk.BOTH, expand=True)
        self.input_text.bind("<Return>", lambda e: self._on_enter_key(e))
        
        # 发送按钮
        send_btn = tk.Button(
            input_container,
            text="📤 发送  Enter",
            command=self.send_message,
            font=("Microsoft YaHei", 9, "bold"),
            bg=Colors.PRIMARY,
            fg="white",
            relief=tk.FLAT,
            padx=20,
            pady=8,
            cursor="hand2"
        )
        send_btn.pack(anchor=tk.E, pady=(8, 0))
        
        # 底部状态栏
        status_frame = tk.Frame(parent, bg=Colors.BG_MAIN, height=30)
        status_frame.pack(fill=tk.X)
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(
            status_frame,
            text="✓ 就绪",
            font=("Microsoft YaHei", 8),
            bg=Colors.BG_MAIN,
            fg=Colors.TEXT_HINT
        )
        self.status_label.pack(side=tk.LEFT, padx=20)
        
        # 每日小贴士
        self.tip_label = tk.Label(
            status_frame,
            text=self.assistant.get_daily_tip(),
            font=("Microsoft YaHei", 8),
            bg=Colors.BG_MAIN,
            fg=Colors.SUCCESS
        )
        self.tip_label.pack(side=tk.RIGHT, padx=20)

    def _load_initial_data(self):
        """加载初始数据"""
        # 创建默认对话
        self._new_chat()
        
        # 显示欢迎消息
        self._add_welcome_message()

    def _new_chat(self):
        """新建对话"""
        import uuid
        chat_id = str(uuid.uuid4())[:8]
        self.chats[chat_id] = {
            "id": chat_id,
            "title": "新对话",
            "messages": [],
            "created_at": datetime.now().isoformat()
        }
        self.current_chat_id = chat_id
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete("1.0", tk.END)
        self.chat_display.config(state=tk.DISABLED)
        self.chat_title_label.config(text="新对话")
        self._refresh_chat_list()

    def _refresh_chat_list(self):
        """刷新对话列表"""
        # 清空列表
        for widget in self.chat_list_frame.winfo_children():
            widget.destroy()
        
        # 显示对话列表
        for chat_id, chat in sorted(self.chats.items(), key=lambda x: x[1]["created_at"], reverse=True)[:20]:
            self._add_chat_item(chat_id, chat)

    def _add_chat_item(self, chat_id, chat):
        """添加对话项到列表"""
        item_frame = tk.Frame(self.chat_list_frame, bg=Colors.BG_SIDEBAR)
        item_frame.pack(fill=tk.X, padx=10, pady=2)
        
        # 对话标题
        title = chat["title"][:20] + "..." if len(chat["title"]) > 20 else chat["title"]
        is_current = chat_id == self.current_chat_id
        
        bg_color = Colors.BG_HOVER if is_current else Colors.BG_SIDEBAR
        fg_color = Colors.PRIMARY if is_current else Colors.TEXT_PRIMARY
        
        item_btn = tk.Button(
            item_frame,
            text=f"💬 {title}",
            command=lambda cid=chat_id: self._select_chat(cid),
            font=("Microsoft YaHei", 9),
            bg=bg_color,
            fg=fg_color,
            relief=tk.FLAT,
            anchor=tk.W,
            padx=10,
            pady=8,
            cursor="hand2"
        )
        item_btn.pack(fill=tk.X)
        
        # 悬停效果
        item_btn.bind("<Enter>", lambda e, f=item_frame: f.config(bg=Colors.BG_HOVER))
        item_btn.bind("<Leave>", lambda e, f=item_frame, cid=chat_id: f.config(bg=Colors.BG_SIDEBAR if cid != self.current_chat_id else Colors.BG_HOVER))

    def _select_chat(self, chat_id):
        """选择对话"""
        if chat_id in self.chats:
            self.current_chat_id = chat_id
            chat = self.chats[chat_id]
            self.chat_title_label.config(text=chat["title"])
            
            # 加载聊天记录
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.delete("1.0", tk.END)
            for msg in chat["messages"]:
                self._add_message_to_display(msg["sender"], msg["content"], msg["color"], log=False)
            self.chat_display.config(state=tk.DISABLED)
            
            self._refresh_chat_list()

    def _add_welcome_message(self):
        """添加欢迎消息"""
        welcome = """欢迎使用 zhangy-chat R3！

我是你的专属 AI 助手，可以帮你：
• 解答各种问题
• 管理任务和 goal
• 深度思考复杂问题
• 聊天解闷

💡 提示：勾选"🧠 深度思考"可以分析复杂问题的多个维度哦～"""
        self._add_message("ai", welcome)

    def send_message(self):
        """发送消息"""
        user_input = self.input_text.get("1.0", tk.END).strip()
        if not user_input:
            return

        self.input_text.delete("1.0", tk.END)
        self._add_message("user", user_input)
        
        # 更新对话标题
        if len(self.chats[self.current_chat_id]["messages"]) <= 1:
            self.chats[self.current_chat_id]["title"] = user_input[:20]
            self.chat_title_label.config(text=self.chats[self.current_chat_id]["title"])
        
        # 检查是否启用深度思考
        deep_thinking = self.deep_thinking_var.get()
        if deep_thinking:
            self.status_label.config(text="🧠 深度思考中...")
        else:
            self.status_label.config(text="⏳ 正在思考...")

        thread = threading.Thread(target=self._process_response, args=(user_input, deep_thinking))
        thread.daemon = True
        thread.start()

    def _process_response(self, user_input, deep_thinking=False):
        """处理响应"""
        try:
            # 如果启用了外部 AI，优先使用外部 AI
            if self.use_external_ai and self.external_ai.provider != "none":
                response = self.external_ai.chat(user_input)
                if response:
                    self.root.after(0, lambda: self._add_message("ai", response))
                    return

            # 使用本地 AI 助手（支持深度思考）
            response = self.assistant.chat(user_input, deep_thinking=deep_thinking)
            # 移除 "zhangy-chat:" 前缀（如果有）
            if response.startswith("zhangy-chat:"):
                response = response.replace("zhangy-chat:", "").strip()
            self.root.after(0, lambda: self._add_message("ai", response))
        except Exception as e:
            self.root.after(0, lambda: self._add_message("system", f"错误：{str(e)}"))
        finally:
            self.root.after(0, lambda: self.status_label.config(text="✓ 就绪"))

    def _add_message(self, sender, content):
        """添加消息"""
        if sender == "user":
            color = Colors.USER_BG
        elif sender == "system":
            color = Colors.ERROR
        else:
            color = Colors.AI_TEXT
        
        # 添加到显示
        self._add_message_to_display(sender, content, color)
        
        # 保存到聊天记录
        self.chats[self.current_chat_id]["messages"].append({
            "sender": sender,
            "content": content,
            "color": color,
            "timestamp": datetime.now().isoformat()
        })
        self.chats[self.current_chat_id]["updated_at"] = datetime.now().isoformat()

    def _add_message_to_display(self, sender, content, color, log=True):
        """添加消息到显示区域"""
        self.chat_display.config(state=tk.NORMAL)
        
        if sender == "user":
            # 用户消息 - 右侧蓝色气泡
            self.chat_display.insert(tk.END, "\n")
            self.chat_display.insert(tk.END, f"  {content}\n\n", "user_bubble")
            self.chat_display.tag_config("user_bubble", 
                                         font=("Microsoft YaHei", 10), 
                                         foreground=Colors.USER_TEXT,
                                         background=Colors.USER_BG,
                                         lmargin1=400,
                                         lmargin2=400,
                                         rmargin=20,
                                         spacing1=10,
                                         spacing3=10)
        elif sender == "ai":
            # AI 消息 - 左侧白色气泡
            self.chat_display.insert(tk.END, "\n")
            self.chat_display.insert(tk.END, f"zhangy-chat\n", "ai_sender")
            self.chat_display.insert(tk.END, f"{content}\n\n", "ai_message")
            self.chat_display.tag_config("ai_sender", 
                                         font=("Microsoft YaHei", 9, "bold"), 
                                         foreground=Colors.PRIMARY,
                                         lmargin1=20,
                                         rmargin=400)
            self.chat_display.tag_config("ai_message", 
                                         font=("Microsoft YaHei", 10), 
                                         foreground=Colors.AI_TEXT,
                                         lmargin1=20,
                                         rmargin=400,
                                         spacing1=5,
                                         spacing3=5)
        elif sender == "system":
            # 系统消息 - 居中红色
            self.chat_display.insert(tk.END, "\n")
            self.chat_display.insert(tk.END, f"  {content}  \n\n", "system_bubble")
            self.chat_display.tag_config("system_bubble", 
                                         font=("Microsoft YaHei", 9), 
                                         foreground=Colors.ERROR,
                                         justify=tk.CENTER,
                                         lmargin1=200,
                                         rmargin=200)
        
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)

    def clear_chat(self):
        """清空聊天记录"""
        if messagebox.askyesno("确认", "确定要清空当前对话吗？"):
            self.chats[self.current_chat_id]["messages"] = []
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.delete("1.0", tk.END)
            self.chat_display.config(state=tk.DISABLED)
            self._add_welcome_message()

    def _switch_to_cmd(self):
        """切换到 CMD 模式"""
        if messagebox.askyesno("切换模式", "确定要切换到 CMD 模式吗？"):
            self.root.quit()
            subprocess.Popen([sys.executable, "main.py", "-cmd"])

    def _on_enter_key(self, event):
        """处理回车键发送"""
        if not event.state & 0x1:  # 没有按 Shift
            self.send_message()
            return "break"

    def _open_settings(self):
        """打开设置窗口"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("设置")
        settings_window.geometry("500x600")
        settings_window.configure(bg=Colors.BG_MAIN)
        
        # 设置内容
        self._create_settings_content(settings_window)

    def _create_settings_content(self, parent):
        """创建设置内容"""
        # 内存配置
        mem_frame = tk.LabelFrame(parent, text="内存配置", font=("Microsoft YaHei", 10, "bold"), bg=Colors.BG_MAIN)
        mem_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(mem_frame, text="内存大小:", bg=Colors.BG_MAIN).grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        self.mem_var = tk.StringVar(value=str(self.memory_manager.selected_memory))
        mem_combo = ttk.Combobox(mem_frame, textvariable=self.mem_var, values=["8", "16", "32", "64"], width=10)
        mem_combo.grid(row=0, column=1, padx=10, pady=10)
        mem_combo.bind("<<ComboboxSelected>>", lambda e: self._set_memory())
        
        # 心情配置
        mood_frame = tk.LabelFrame(parent, text="心情配置", font=("Microsoft YaHei", 10, "bold"), bg=Colors.BG_MAIN)
        mood_frame.pack(fill=tk.X, padx=20, pady=10)
        
        for key, info in self.mood_manager.get_all_moods().items():
            tk.Button(
                mood_frame,
                text=f"{info['icon']} {info['name']}",
                command=lambda k=key: self._select_mood(k),
                bg=Colors.BG_SECONDARY
            ).pack(side=tk.LEFT, padx=5, pady=5)
        
        # 关于
        about_frame = tk.LabelFrame(parent, text="关于", font=("Microsoft YaHei", 10, "bold"), bg=Colors.BG_MAIN)
        about_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(about_frame, text="zhangy-chat R3\n版本：3.0.0\n作者：zhangy", bg=Colors.BG_MAIN).pack(pady=10)

    def _set_memory(self):
        """设置内存"""
        try:
            mem_gib = int(self.mem_var.get())
            result = self.memory_manager.set_memory(mem_gib)
            if result['success']:
                messagebox.showinfo("内存配置", result['message'])
        except:
            messagebox.showerror("错误", "无效的内存配置")

    def _select_mood(self, mood_key):
        """选择心情"""
        result = self.mood_manager.set_mood(mood_key)
        if result['success']:
            messagebox.showinfo("心情切换", result['message'])


def main():
    """主函数"""
    root = tk.Tk()
    app = ZhangyChatGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
