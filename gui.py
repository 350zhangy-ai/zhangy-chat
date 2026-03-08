#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
zhangy chat - 图形界面版本 (R3 豆包风格美化版)
现代、简洁、优雅的 UI 设计
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
    """zhangy chat 图形界面类 (R3 豆包风格)"""

    def __init__(self, root):
        """初始化 GUI"""
        self.root = root
        self.root.title("zhangy-chat R3")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # 设置窗口图标（如果有）
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass

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

        # 当前标签页
        self.current_tab = "chat"
        
        # 聊天记录
        self.chat_history = []

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
        """创建界面组件 - 豆包风格"""
        self.root.configure(bg=Colors.BG_SECONDARY)
        
        # ==================== 顶部导航栏 ====================
        nav_frame = tk.Frame(self.root, bg=Colors.BG_MAIN, height=60)
        nav_frame.pack(fill=tk.X)
        nav_frame.pack_propagate(False)

        # Logo 和标题
        logo_frame = tk.Frame(nav_frame, bg=Colors.BG_MAIN)
        logo_frame.pack(side=tk.LEFT, padx=20)
        
        logo_label = tk.Label(
            logo_frame,
            text="💬 zhangy-chat",
            font=("Microsoft YaHei", 18, "bold"),
            bg=Colors.BG_MAIN,
            fg=Colors.PRIMARY
        )
        logo_label.pack(side=tk.LEFT)
        
        version_label = tk.Label(
            logo_frame,
            text="R3",
            font=("Microsoft YaHei", 10),
            bg=Colors.BG_MAIN,
            fg=Colors.TEXT_HINT
        )
        version_label.pack(side=tk.LEFT, padx=10, pady=5)

        # 右侧按钮
        btn_frame = tk.Frame(nav_frame, bg=Colors.BG_MAIN)
        btn_frame.pack(side=tk.RIGHT, padx=20)

        # CMD 模式按钮
        cmd_btn = tk.Button(
            btn_frame,
            text="⌨️ CMD 模式",
            command=self._switch_to_cmd,
            font=("Microsoft YaHei", 10),
            bg=Colors.BG_SECONDARY,
            fg=Colors.TEXT_PRIMARY,
            relief=tk.FLAT,
            padx=15,
            pady=8,
            cursor="hand2"
        )
        cmd_btn.pack(side=tk.RIGHT, padx=5)
        cmd_btn.bind("<Enter>", lambda e: cmd_btn.config(bg=Colors.BORDER))
        cmd_btn.bind("<Leave>", lambda e: cmd_btn.config(bg=Colors.BG_SECONDARY))

        # 设置按钮
        settings_btn = tk.Button(
            btn_frame,
            text="⚙️ 设置",
            command=lambda: self.notebook.select(4),
            font=("Microsoft YaHei", 10),
            bg=Colors.BG_SECONDARY,
            fg=Colors.TEXT_PRIMARY,
            relief=tk.FLAT,
            padx=15,
            pady=8,
            cursor="hand2"
        )
        settings_btn.pack(side=tk.RIGHT, padx=5)
        settings_btn.bind("<Enter>", lambda e: settings_btn.config(bg=Colors.BORDER))
        settings_btn.bind("<Leave>", lambda e: settings_btn.config(bg=Colors.BG_SECONDARY))

        # ==================== 主内容区域 ====================
        main_frame = tk.Frame(self.root, bg=Colors.BG_SECONDARY)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)

        # 使用 Notebook 实现标签页
        self.notebook = ttk.Notebook(main_frame, style="Custom.TNotebook")
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # 自定义 Notebook 样式
        style = ttk.Style()
        style.configure("Custom.TNotebook", background=Colors.BG_SECONDARY, borderwidth=0)
        style.configure("Custom.TNotebook.Tab", 
                       padding=(20, 10), 
                       font=("Microsoft YaHei", 10),
                       background=Colors.BG_SECONDARY,
                       foreground=Colors.TEXT_SECONDARY)
        style.map("Custom.TNotebook.Tab",
                 background=[("selected", Colors.BG_MAIN)],
                 foreground=[("selected", Colors.PRIMARY)])

        # 创建各功能标签页
        self._create_chat_tab()
        self._create_task_tab()
        self._create_goal_tab()
        self._create_habit_tab()
        self._create_settings_tab()

        # ==================== 底部状态栏 ====================
        status_frame = tk.Frame(self.root, bg=Colors.BG_MAIN, height=40)
        status_frame.pack(fill=tk.X)
        status_frame.pack_propagate(False)

        # 状态文字
        self.status_label = tk.Label(
            status_frame,
            text="✓ 就绪",
            font=("Microsoft YaHei", 9),
            bg=Colors.BG_MAIN,
            fg=Colors.TEXT_HINT
        )
        self.status_label.pack(side=tk.LEFT, padx=20)

        # 每日小贴士
        self.tip_label = tk.Label(
            status_frame,
            text=self.assistant.get_daily_tip(),
            font=("Microsoft YaHei", 9),
            bg=Colors.BG_MAIN,
            fg=Colors.SUCCESS
        )
        self.tip_label.pack(side=tk.RIGHT, padx=20)

    def _create_chat_tab(self):
        """创建聊天标签页 - 豆包风格"""
        chat_frame = tk.Frame(self.notebook, bg=Colors.BG_CHAT)
        self.notebook.add(chat_frame, text="💬 对话")

        # ==================== 心情选择区 ====================
        mood_frame = tk.LabelFrame(
            chat_frame, 
            text="💚 当前心情", 
            font=("Microsoft YaHei", 9, "bold"), 
            bg=Colors.BG_MAIN,
            fg=Colors.TEXT_PRIMARY,
            relief=tk.FLAT,
            bd=1
        )
        mood_frame.pack(fill=tk.X, padx=15, pady=10)

        self.mood_buttons = {}
        mood_layout = tk.Frame(mood_frame, bg=Colors.BG_MAIN)
        mood_layout.pack(padx=15, pady=10)

        for key, info in self.mood_manager.get_all_moods().items():
            btn = tk.Button(
                mood_layout,
                text=f"{info['icon']} {info['name']}",
                command=lambda k=key: self._select_mood(k),
                font=("Microsoft YaHei", 9),
                bg=Colors.BG_SECONDARY,
                fg=Colors.TEXT_PRIMARY,
                relief=tk.FLAT,
                padx=12,
                pady=6,
                cursor="hand2",
                borderwidth=1,
                highlightthickness=1,
                highlightbackground=Colors.BORDER
            )
            btn.pack(side=tk.LEFT, padx=5)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=Colors.PRIMARY_LIGHT))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=Colors.BG_SECONDARY))
            self.mood_buttons[key] = btn

        self._update_mood_buttons()

        # ==================== 聊天显示区 ====================
        chat_container = tk.Frame(chat_frame, bg=Colors.BG_CHAT)
        chat_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        # 聊天记录显示区域
        self.chat_display = scrolledtext.ScrolledText(
            chat_container,
            wrap=tk.WORD,
            font=("Microsoft YaHei", 10),
            bg=Colors.BG_CHAT,
            fg=Colors.TEXT_PRIMARY,
            padx=10,
            pady=10,
            relief=tk.FLAT,
            borderwidth=0,
            highlightthickness=0
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        self.chat_display.config(state=tk.DISABLED)

        # ==================== 输入区域 ====================
        input_frame = tk.Frame(chat_frame, bg=Colors.BG_MAIN)
        input_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        input_frame.pack_propagate(False)
        input_frame.config(height=120)

        # 输入框
        input_container = tk.Frame(input_frame, bg=Colors.BG_MAIN)
        input_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        tk.Label(
            input_container,
            text="输入问题:",
            font=("Microsoft YaHei", 9, "bold"),
            bg=Colors.BG_MAIN,
            fg=Colors.TEXT_PRIMARY
        ).pack(anchor=tk.W, pady=(0, 8))

        self.input_text = tk.Text(
            input_container,
            height=3,
            font=("Microsoft YaHei", 10),
            bg=Colors.BG_SECONDARY,
            fg=Colors.TEXT_PRIMARY,
            padx=12,
            pady=10,
            relief=tk.FLAT,
            borderwidth=0,
            highlightthickness=1,
            highlightbackground=Colors.BORDER,
            insertbackground=Colors.PRIMARY
        )
        self.input_text.pack(fill=tk.X, pady=5)
        self.input_text.bind("<Return>", lambda e: self._on_enter_key(e))
        self.input_text.bind("<Shift-Return>", lambda e: None)  # 允许换行

        # 按钮区域
        button_frame = tk.Frame(input_container, bg=Colors.BG_MAIN)
        button_frame.pack(fill=tk.X, pady=(10, 0))

        # 清空按钮
        clear_btn = tk.Button(
            button_frame,
            text="🗑️ 清空",
            command=self.clear_chat,
            font=("Microsoft YaHei", 9),
            bg=Colors.BG_SECONDARY,
            fg=Colors.TEXT_SECONDARY,
            relief=tk.FLAT,
            padx=15,
            pady=8,
            cursor="hand2"
        )
        clear_btn.pack(side=tk.LEFT)
        clear_btn.bind("<Enter>", lambda e: clear_btn.config(bg=Colors.BORDER))
        clear_btn.bind("<Leave>", lambda e: clear_btn.config(bg=Colors.BG_SECONDARY))

        # 发送按钮
        send_btn = tk.Button(
            button_frame,
            text="📤 发送",
            command=self.send_message,
            font=("Microsoft YaHei", 10, "bold"),
            bg=Colors.PRIMARY,
            fg=Colors.USER_TEXT,
            relief=tk.FLAT,
            padx=25,
            pady=10,
            cursor="hand2"
        )
        send_btn.pack(side=tk.RIGHT)
        send_btn.bind("<Enter>", lambda e: send_btn.config(bg=Colors.PRIMARY_DARK))
        send_btn.bind("<Leave>", lambda e: send_btn.config(bg=Colors.PRIMARY))

    def _create_task_tab(self):
        """创建任务标签页 - 豆包风格"""
        task_frame = tk.Frame(self.notebook, bg=Colors.BG_CHAT)
        self.notebook.add(task_frame, text="📋 任务")

        # 任务输入区
        input_frame = tk.LabelFrame(
            task_frame, 
            text="➕ 添加任务", 
            font=("Microsoft YaHei", 9, "bold"), 
            bg=Colors.BG_MAIN,
            fg=Colors.TEXT_PRIMARY,
            relief=tk.FLAT,
            bd=1
        )
        input_frame.pack(fill=tk.X, padx=15, pady=10)

        tk.Label(input_frame, text="任务标题:", bg=Colors.BG_MAIN, fg=Colors.TEXT_PRIMARY).grid(row=0, column=0, sticky=tk.W, padx=15, pady=10)
        self.task_title = tk.Entry(input_frame, font=("Microsoft YaHei", 10), width=40, bg=Colors.BG_SECONDARY, fg=Colors.TEXT_PRIMARY, relief=tk.FLAT, highlightthickness=1, highlightbackground=Colors.BORDER)
        self.task_title.grid(row=0, column=1, padx=15, pady=10)

        tk.Label(input_frame, text="描述:", bg=Colors.BG_MAIN, fg=Colors.TEXT_PRIMARY).grid(row=1, column=0, sticky=tk.W, padx=15, pady=10)
        self.task_desc = tk.Entry(input_frame, font=("Microsoft YaHei", 10), width=40, bg=Colors.BG_SECONDARY, fg=Colors.TEXT_PRIMARY, relief=tk.FLAT, highlightthickness=1, highlightbackground=Colors.BORDER)
        self.task_desc.grid(row=1, column=1, padx=15, pady=10)

        tk.Label(input_frame, text="优先级 (1-5):", bg=Colors.BG_MAIN, fg=Colors.TEXT_PRIMARY).grid(row=2, column=0, sticky=tk.W, padx=15, pady=10)
        self.task_priority = ttk.Spinbox(input_frame, from_=1, to=5, width=10, font=("Microsoft YaHei", 10))
        self.task_priority.set(3)
        self.task_priority.grid(row=2, column=1, sticky=tk.W, padx=15, pady=10)

        add_btn = tk.Button(
            input_frame,
            text="✓ 添加任务",
            command=self._add_task,
            font=("Microsoft YaHei", 10, "bold"),
            bg=Colors.PRIMARY,
            fg=Colors.USER_TEXT,
            relief=tk.FLAT,
            padx=20,
            pady=8
        )
        add_btn.grid(row=3, column=1, sticky=tk.E, padx=15, pady=15)

        # 任务列表区
        list_frame = tk.LabelFrame(
            task_frame, 
            text="📝 任务列表", 
            font=("Microsoft YaHei", 9, "bold"), 
            bg=Colors.BG_MAIN,
            fg=Colors.TEXT_PRIMARY,
            relief=tk.FLAT,
            bd=1
        )
        list_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        # 筛选按钮
        filter_frame = tk.Frame(list_frame, bg=Colors.BG_MAIN)
        filter_frame.pack(fill=tk.X, padx=15, pady=10)

        tk.Label(filter_frame, text="筛选:", bg=Colors.BG_MAIN, fg=Colors.TEXT_SECONDARY).pack(side=tk.LEFT)
        self.task_filter = tk.StringVar(value="pending")
        for status, label in [("pending", "待完成"), ("in_progress", "进行中"), ("completed", "已完成"), ("all", "全部")]:
            rb = tk.Radiobutton(
                filter_frame,
                text=label,
                variable=self.task_filter,
                value=status,
                bg=Colors.BG_MAIN,
                fg=Colors.TEXT_PRIMARY,
                selectcolor=Colors.PRIMARY_LIGHT,
                activebackground=Colors.BG_MAIN,
                activeforeground=Colors.PRIMARY
            )
            rb.pack(side=tk.LEFT, padx=10)

        # 任务列表
        columns = ("ID", "标题", "优先级", "状态", "截止")
        self.task_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=10)
        for col in columns:
            self.task_tree.heading(col, text=col)
            self.task_tree.column(col, width=100, anchor=tk.CENTER)
        self.task_tree.column("标题", width=300, anchor=tk.W)
        self.task_tree.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        # 操作按钮
        op_frame = tk.Frame(list_frame, bg=Colors.BG_MAIN)
        op_frame.pack(fill=tk.X, padx=15, pady=10)

        tk.Button(op_frame, text="🔄 刷新", command=self._refresh_task_list, bg=Colors.BG_SECONDARY, fg=Colors.TEXT_PRIMARY, relief=tk.FLAT, padx=15, pady=6).pack(side=tk.LEFT, padx=5)
        tk.Button(op_frame, text="✓ 完成", command=self._complete_task, bg=Colors.SUCCESS, fg=Colors.USER_TEXT, relief=tk.FLAT, padx=15, pady=6).pack(side=tk.LEFT, padx=5)
        tk.Button(op_frame, text="🗑️ 删除", command=self._delete_task, bg=Colors.ERROR, fg=Colors.USER_TEXT, relief=tk.FLAT, padx=15, pady=6).pack(side=tk.LEFT, padx=5)

    def _create_goal_tab(self):
        """创建目标标签页 - 豆包风格"""
        goal_frame = tk.Frame(self.notebook, bg=Colors.BG_CHAT)
        self.notebook.add(goal_frame, text="🎯 目标")

        # 目标输入区
        input_frame = tk.LabelFrame(
            goal_frame, 
            text="🎯 添加目标", 
            font=("Microsoft YaHei", 9, "bold"), 
            bg=Colors.BG_MAIN,
            fg=Colors.TEXT_PRIMARY,
            relief=tk.FLAT,
            bd=1
        )
        input_frame.pack(fill=tk.X, padx=15, pady=10)

        tk.Label(input_frame, text="目标标题:", bg=Colors.BG_MAIN, fg=Colors.TEXT_PRIMARY).grid(row=0, column=0, sticky=tk.W, padx=15, pady=10)
        self.goal_title = tk.Entry(input_frame, font=("Microsoft YaHei", 10), width=40, bg=Colors.BG_SECONDARY, fg=Colors.TEXT_PRIMARY, relief=tk.FLAT, highlightthickness=1, highlightbackground=Colors.BORDER)
        self.goal_title.grid(row=0, column=1, padx=15, pady=10)

        tk.Label(input_frame, text="描述:", bg=Colors.BG_MAIN, fg=Colors.TEXT_PRIMARY).grid(row=1, column=0, sticky=tk.W, padx=15, pady=10)
        self.goal_desc = tk.Entry(input_frame, font=("Microsoft YaHei", 10), width=40, bg=Colors.BG_SECONDARY, fg=Colors.TEXT_PRIMARY, relief=tk.FLAT, highlightthickness=1, highlightbackground=Colors.BORDER)
        self.goal_desc.grid(row=1, column=1, padx=15, pady=10)

        add_btn = tk.Button(
            input_frame,
            text="✓ 添加目标",
            command=self._add_goal,
            font=("Microsoft YaHei", 10, "bold"),
            bg=Colors.PRIMARY,
            fg=Colors.USER_TEXT,
            relief=tk.FLAT,
            padx=20,
            pady=8
        )
        add_btn.grid(row=2, column=1, sticky=tk.E, padx=15, pady=15)

        # 目标列表区
        list_frame = tk.LabelFrame(
            goal_frame, 
            text="📊 目标列表", 
            font=("Microsoft YaHei", 9, "bold"), 
            bg=Colors.BG_MAIN,
            fg=Colors.TEXT_PRIMARY,
            relief=tk.FLAT,
            bd=1
        )
        list_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        columns = ("ID", "标题", "状态", "进度")
        self.goal_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=8)
        for col in columns:
            self.goal_tree.heading(col, text=col)
            self.goal_tree.column(col, width=150, anchor=tk.CENTER)
        self.goal_tree.column("标题", width=400, anchor=tk.W)
        self.goal_tree.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        # 操作按钮
        op_frame = tk.Frame(list_frame, bg=Colors.BG_MAIN)
        op_frame.pack(fill=tk.X, padx=15, pady=10)

        tk.Button(op_frame, text="🔄 刷新", command=self._refresh_goal_list, bg=Colors.BG_SECONDARY, fg=Colors.TEXT_PRIMARY, relief=tk.FLAT, padx=15, pady=6).pack(side=tk.LEFT, padx=5)
        tk.Button(op_frame, text="📈 生成复盘", command=self._generate_review, bg=Colors.WARNING, fg=Colors.USER_TEXT, relief=tk.FLAT, padx=15, pady=6).pack(side=tk.LEFT, padx=5)

    def _create_habit_tab(self):
        """创建习惯标签页 - 豆包风格"""
        habit_frame = tk.Frame(self.notebook, bg=Colors.BG_CHAT)
        self.notebook.add(habit_frame, text="✅ 习惯")

        # 习惯输入区
        input_frame = tk.LabelFrame(
            habit_frame, 
            text="✅ 添加习惯", 
            font=("Microsoft YaHei", 9, "bold"), 
            bg=Colors.BG_MAIN,
            fg=Colors.TEXT_PRIMARY,
            relief=tk.FLAT,
            bd=1
        )
        input_frame.pack(fill=tk.X, padx=15, pady=10)

        tk.Label(input_frame, text="习惯名称:", bg=Colors.BG_MAIN, fg=Colors.TEXT_PRIMARY).grid(row=0, column=0, sticky=tk.W, padx=15, pady=10)
        self.habit_name = tk.Entry(input_frame, font=("Microsoft YaHei", 10), width=30, bg=Colors.BG_SECONDARY, fg=Colors.TEXT_PRIMARY, relief=tk.FLAT, highlightthickness=1, highlightbackground=Colors.BORDER)
        self.habit_name.grid(row=0, column=1, padx=15, pady=10)

        tk.Label(input_frame, text="频率:", bg=Colors.BG_MAIN, fg=Colors.TEXT_PRIMARY).grid(row=0, column=2, sticky=tk.W, padx=15, pady=10)
        self.habit_freq = ttk.Combobox(input_frame, values=["daily", "weekly"], width=10, font=("Microsoft YaHei", 10))
        self.habit_freq.set("daily")
        self.habit_freq.grid(row=0, column=3, padx=15, pady=10)

        add_btn = tk.Button(
            input_frame,
            text="✓ 添加习惯",
            command=self._add_habit,
            font=("Microsoft YaHei", 10, "bold"),
            bg=Colors.PRIMARY,
            fg=Colors.USER_TEXT,
            relief=tk.FLAT,
            padx=20,
            pady=8
        )
        add_btn.grid(row=1, column=3, sticky=tk.E, padx=15, pady=15)

        # 习惯列表区
        list_frame = tk.LabelFrame(
            habit_frame, 
            text="📅 习惯列表", 
            font=("Microsoft YaHei", 9, "bold"), 
            bg=Colors.BG_MAIN,
            fg=Colors.TEXT_PRIMARY,
            relief=tk.FLAT,
            bd=1
        )
        list_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        columns = ("名称", "频率", "连续天数", "总次数")
        self.habit_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=8)
        for col in columns:
            self.habit_tree.heading(col, text=col)
            self.habit_tree.column(col, width=150, anchor=tk.CENTER)
        self.habit_tree.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        # 操作按钮
        op_frame = tk.Frame(list_frame, bg=Colors.BG_MAIN)
        op_frame.pack(fill=tk.X, padx=15, pady=10)

        tk.Button(op_frame, text="🔄 刷新", command=self._refresh_habit_list, bg=Colors.BG_SECONDARY, fg=Colors.TEXT_PRIMARY, relief=tk.FLAT, padx=15, pady=6).pack(side=tk.LEFT, padx=5)
        tk.Button(op_frame, text="✓ 打卡", command=self._habit_checkin, bg=Colors.SUCCESS, fg=Colors.USER_TEXT, relief=tk.FLAT, padx=15, pady=6).pack(side=tk.LEFT, padx=5)
        tk.Button(op_frame, text="🗑️ 删除", command=self._delete_habit, bg=Colors.ERROR, fg=Colors.USER_TEXT, relief=tk.FLAT, padx=15, pady=6).pack(side=tk.LEFT, padx=5)

    def _create_settings_tab(self):
        """创建设置标签页 - 豆包风格"""
        settings_frame = tk.Frame(self.notebook, bg=Colors.BG_CHAT)
        self.notebook.add(settings_frame, text="⚙️ 设置")

        # 系统配置区
        sys_frame = tk.LabelFrame(
            settings_frame, 
            text="🔧 系统配置", 
            font=("Microsoft YaHei", 9, "bold"), 
            bg=Colors.BG_MAIN,
            fg=Colors.TEXT_PRIMARY,
            relief=tk.FLAT,
            bd=1
        )
        sys_frame.pack(fill=tk.X, padx=15, pady=10)

        # 内存配置
        mem_frame = tk.Frame(sys_frame, bg=Colors.BG_MAIN)
        mem_frame.pack(fill=tk.X, padx=15, pady=15)

        tk.Label(mem_frame, text="内存配置:", bg=Colors.BG_MAIN, font=("Microsoft YaHei", 10)).grid(row=0, column=0, padx=15, pady=10, sticky=tk.W)
        self.mem_var = tk.StringVar(value=str(self.memory_manager.selected_memory))
        mem_combo = ttk.Combobox(
            mem_frame,
            textvariable=self.mem_var,
            values=["8", "16", "32", "64"],
            width=10,
            font=("Microsoft YaHei", 10),
            state="readonly"
        )
        mem_combo.grid(row=0, column=1, padx=10, pady=10)
        mem_combo.bind("<<ComboboxSelected>>", lambda e: self._set_memory())

        tk.Label(mem_frame, text="GiB", bg=Colors.BG_MAIN, font=("Microsoft YaHei", 10)).grid(row=0, column=2, padx=5, pady=10, sticky=tk.W)

        # 预设选择
        preset_frame = tk.Frame(sys_frame, bg=Colors.BG_MAIN)
        preset_frame.pack(fill=tk.X, padx=15, pady=15)

        tk.Label(preset_frame, text="场景预设:", bg=Colors.BG_MAIN, font=("Microsoft YaHei", 10)).grid(row=0, column=0, padx=15, pady=10, sticky=tk.W)

        self.preset_var = tk.StringVar(value=self.preset_manager.get_current_preset())
        preset_choices = [
            ("office", "💼 高效办公"),
            ("exam", "📚 备考冲刺"),
            ("casual", "🍵 休闲陪伴"),
            ("emotional", "💚 情绪疏导")
        ]
        for i, (key, label) in enumerate(preset_choices):
            rb = tk.Radiobutton(
                preset_frame,
                text=label,
                variable=self.preset_var,
                value=key,
                bg=Colors.BG_MAIN,
                font=("Microsoft YaHei", 10),
                command=lambda k=key: self._set_preset(k)
            )
            rb.grid(row=0, column=i+1, padx=10, pady=10, sticky=tk.W)

        # 数据管理区
        data_frame = tk.LabelFrame(
            settings_frame, 
            text="💾 数据管理", 
            font=("Microsoft YaHei", 9, "bold"), 
            bg=Colors.BG_MAIN,
            fg=Colors.TEXT_PRIMARY,
            relief=tk.FLAT,
            bd=1
        )
        data_frame.pack(fill=tk.X, padx=15, pady=10)

        btn_frame = tk.Frame(data_frame, bg=Colors.BG_MAIN)
        btn_frame.pack(padx=15, pady=15)

        tk.Button(btn_frame, text="📦 备份数据", command=self._backup_data, bg=Colors.PRIMARY, fg=Colors.USER_TEXT, relief=tk.FLAT, width=15, padx=15, pady=8).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="📄 导出 TXT", command=lambda: self._export_data("txt"), bg=Colors.BG_SECONDARY, fg=Colors.TEXT_PRIMARY, relief=tk.FLAT, width=15, padx=15, pady=8).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="📊 导出 Excel", command=lambda: self._export_data("excel"), bg=Colors.BG_SECONDARY, fg=Colors.TEXT_PRIMARY, relief=tk.FLAT, width=15, padx=15, pady=8).pack(side=tk.LEFT, padx=5)

        # 关于区
        about_frame = tk.LabelFrame(
            settings_frame, 
            text="ℹ️ 关于", 
            font=("Microsoft YaHei", 9, "bold"), 
            bg=Colors.BG_MAIN,
            fg=Colors.TEXT_PRIMARY,
            relief=tk.FLAT,
            bd=1
        )
        about_frame.pack(fill=tk.X, padx=15, pady=10)

        about_text = """
zhangy-chat R3 - 高效、专业的本地 AI 助手

版本：3.0.0
作者：zhangy
协议：MIT License

R3 新功能:
• 8/16/32/64GiB 内存配置
• 5 种心情标签选择
• 4 类场景预设切换
• 双界面无缝切换
"""
        tk.Label(about_frame, text=about_text, bg=Colors.BG_MAIN, justify=tk.LEFT, font=("Microsoft YaHei", 9), fg=Colors.TEXT_SECONDARY).pack(padx=15, pady=15)

    def _load_initial_data(self):
        """加载初始数据"""
        self._refresh_task_list()
        self._refresh_goal_list()
        self._refresh_habit_list()
        self._update_mood_buttons()
        self._update_preset_display()

        # 显示欢迎消息
        self._add_message("system", f"欢迎使用 zhangy-chat R3！我是你的专属 AI 助手，有任何问题都可以问我。", "#00B365")

    def _switch_to_cmd(self):
        """切换到 CMD 模式"""
        if messagebox.askyesno("切换模式", "确定要切换到 CMD 模式吗？"):
            self.root.quit()
            subprocess.Popen([sys.executable, "main.py", "-cmd"])

    def send_message(self):
        """发送消息"""
        user_input = self.input_text.get("1.0", tk.END).strip()
        if not user_input:
            return

        self.input_text.delete("1.0", tk.END)
        self._add_message("user", user_input, Colors.USER_BG)
        self.status_label.config(text="⏳ 正在思考...")

        thread = threading.Thread(target=self._process_response, args=(user_input,))
        thread.daemon = True
        thread.start()

    def _process_response(self, user_input):
        """处理响应"""
        try:
            response = self.assistant.chat(user_input)
            # 移除 "zhangy-chat:" 前缀（如果有）
            if response.startswith("zhangy-chat:"):
                response = response.replace("zhangy-chat:", "").strip()
            self.root.after(0, lambda: self._add_message("ai", response, Colors.AI_TEXT))
        except Exception as e:
            self.root.after(0, lambda: self._add_message("system", f"错误：{str(e)}", Colors.ERROR))
        finally:
            self.root.after(0, lambda: self.status_label.config(text="✓ 就绪"))

    def _on_enter_key(self, event):
        """处理回车键发送"""
        if not event.state & 0x1:  # 没有按 Shift
            self.send_message()
            return "break"

    def _add_message(self, sender, message, color):
        """添加消息到聊天记录 - 豆包风格气泡"""
        self.chat_display.config(state=tk.NORMAL)
        
        if sender == "user":
            # 用户消息 - 右侧蓝色气泡
            self.chat_display.insert(tk.END, "\n")
            self.chat_display.insert(tk.END, f"  {message}\n\n", "user_bubble")
            self.chat_display.tag_config("user_bubble", 
                                         font=("Microsoft YaHei", 10), 
                                         foreground=Colors.USER_TEXT,
                                         background=Colors.USER_BG,
                                         lmargin1=400,
                                         lmargin2=400,
                                         rmargin=20,
                                         spacing1=10,
                                         spacing3=10,
                                         borderwidth=0)
        elif sender == "ai":
            # AI 消息 - 左侧白色气泡
            self.chat_display.insert(tk.END, "\n")
            self.chat_display.insert(tk.END, f"zhangy-chat:\n", "ai_sender")
            self.chat_display.insert(tk.END, f"{message}\n\n", "ai_message")
            self.chat_display.tag_config("ai_sender", 
                                         font=("Microsoft YaHei", 10, "bold"), 
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
            # 系统消息 - 居中绿色
            self.chat_display.insert(tk.END, "\n")
            self.chat_display.insert(tk.END, f"  {message}  \n\n", "system_bubble")
            self.chat_display.tag_config("system_bubble", 
                                         font=("Microsoft YaHei", 9), 
                                         foreground=Colors.SUCCESS,
                                         justify=tk.CENTER,
                                         lmargin1=200,
                                         rmargin=200)
        
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)

    def clear_chat(self):
        """清空聊天记录"""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete("1.0", tk.END)
        self.chat_display.config(state=tk.DISABLED)
        self.chat_history = []

    # R3 方法
    def _select_mood(self, mood_key):
        """选择心情"""
        result = self.mood_manager.set_mood(mood_key)
        if result['success']:
            self._update_mood_buttons()
            self._update_tip()
            messagebox.showinfo("心情切换", result['message'])
        else:
            messagebox.showwarning("提示", result['message'])

    def _update_mood_buttons(self):
        """更新心情按钮状态"""
        current = self.mood_manager.get_current_mood()
        for key, btn in self.mood_buttons.items():
            if key == current:
                btn.config(bg=Colors.PRIMARY_LIGHT, fg=Colors.PRIMARY, relief=tk.FLAT)
            else:
                btn.config(bg=Colors.BG_SECONDARY, fg=Colors.TEXT_PRIMARY, relief=tk.FLAT)

    def _set_memory(self):
        """设置内存配置"""
        try:
            mem_gib = int(self.mem_var.get())
            result = self.memory_manager.set_memory(mem_gib)
            if result['success']:
                messagebox.showinfo("内存配置", f"{result['message']}\n缓存：{result['config']['cache_size']}MB\n并发：{result['config']['max_concurrent']}")
            else:
                messagebox.showwarning("内存配置", result['message'])
        except ValueError:
            messagebox.showerror("错误", "无效的内存配置")

    def _set_preset(self, preset_key):
        """设置预设"""
        result = self.preset_manager.set_preset(preset_key)
        if result['success']:
            self._update_preset_display()
            self._update_tip()
            messagebox.showinfo("预设切换", result['message'])
        else:
            messagebox.showwarning("预设切换", result['message'])

    def _update_preset_display(self):
        """更新预设显示"""
        current = self.preset_manager.get_current_preset()
        self.preset_var.set(current)

    def _update_tip(self):
        """更新每日小贴士"""
        self.tip_label.config(text=self.assistant.get_daily_tip())

    # 任务相关方法
    def _add_task(self):
        """添加任务"""
        title = self.task_title.get().strip()
        desc = self.task_desc.get().strip()
        priority = int(self.task_priority.get())

        if not title:
            messagebox.showwarning("提示", "请输入任务标题")
            return

        task = self.task_manager.add_task(title, desc, priority)
        messagebox.showinfo("成功", f"任务已添加 [ID: {task.id}]")
        self.task_title.delete(0, tk.END)
        self.task_desc.delete(0, tk.END)
        self._refresh_task_list()

    def _refresh_task_list(self):
        """刷新任务列表"""
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)

        status = self.task_filter.get()
        tasks = self.task_manager.get_tasks(status=None if status == "all" else status)

        status_map = {"pending": "待完成", "in_progress": "进行中", "completed": "已完成", "cancelled": "已取消"}
        for task in tasks:
            self.task_tree.insert("", tk.END, values=(
                task.id,
                task.title[:30],
                task.priority,
                status_map.get(task.status, "未知"),
                (task.deadline or "")[:10]
            ))

    def _complete_task(self):
        """完成任务"""
        selected = self.task_tree.selection()
        if not selected:
            messagebox.showwarning("提示", "请选择一个任务")
            return
        item = self.task_tree.item(selected[0])
        task_id = item["values"][0]
        if self.task_manager.update_task_status(task_id, "completed"):
            messagebox.showinfo("成功", "任务已标记为完成")
            self._refresh_task_list()

    def _delete_task(self):
        """删除任务"""
        selected = self.task_tree.selection()
        if not selected:
            messagebox.showwarning("提示", "请选择一个任务")
            return
        if messagebox.askyesno("确认", "确定要删除此任务吗？"):
            item = self.task_tree.item(selected[0])
            task_id = item["values"][0]
            if self.task_manager.delete_task(task_id):
                messagebox.showinfo("成功", "任务已删除")
                self._refresh_task_list()

    # 目标相关方法
    def _add_goal(self):
        """添加目标"""
        title = self.goal_title.get().strip()
        desc = self.goal_desc.get().strip()

        if not title:
            messagebox.showwarning("提示", "请输入目标标题")
            return

        goal = self.task_manager.add_goal(title, desc)
        messagebox.showinfo("成功", f"目标已添加 [ID: {goal.id}]")
        self.goal_title.delete(0, tk.END)
        self.goal_desc.delete(0, tk.END)
        self._refresh_goal_list()

    def _refresh_goal_list(self):
        """刷新目标列表"""
        for item in self.goal_tree.get_children():
            self.goal_tree.delete(item)

        goals = self.task_manager.get_goals()
        for goal in goals:
            progress = goal.get_progress()
            self.goal_tree.insert("", tk.END, values=(
                goal.id,
                goal.title[:40],
                goal.status,
                f"{progress:.0f}%"
            ))

    def _generate_review(self):
        """生成复盘报告"""
        review = self.task_manager.generate_review(7)

        review_window = tk.Toplevel(self.root)
        review_window.title("复盘报告")
        review_window.geometry("600x500")
        review_window.configure(bg=Colors.BG_MAIN)

        text = scrolledtext.ScrolledText(review_window, font=("Microsoft YaHei", 10), bg=Colors.BG_SECONDARY, fg=Colors.TEXT_PRIMARY, relief=tk.FLAT)
        text.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        content = f"""复盘报告：{review['period']}
{'='*40}\n\n"""
        content += f"✅ 完成任务：{review['completed_tasks']} 个\n"
        for task in review['task_details'][:5]:
            content += f"   - {task['title']}\n"

        content += f"\n🎯 进行中目标：{review['active_goals']} 个\n"
        for goal in review['goal_progress']:
            content += f"   - {goal['title']}: {goal['progress']:.0f}%\n"

        content += f"\n📊 习惯打卡:\n"
        for habit in review['habits_summary']:
            content += f"   - {habit['title']}: 连续{habit['streak']}天，总计{habit['total']}次\n"

        text.insert(tk.END, content)
        text.config(state=tk.DISABLED)

    # 习惯相关方法
    def _add_habit(self):
        """添加习惯"""
        name = self.habit_name.get().strip()
        freq = self.habit_freq.get()

        if not name:
            messagebox.showwarning("提示", "请输入习惯名称")
            return

        habit = self.task_manager.add_habit(name, freq)
        messagebox.showinfo("成功", f"习惯已添加 [ID: {habit.id}]")
        self.habit_name.delete(0, tk.END)
        self._refresh_habit_list()

    def _refresh_habit_list(self):
        """刷新习惯列表"""
        for item in self.habit_tree.get_children():
            self.habit_tree.delete(item)

        habits = self.task_manager.get_habits()
        for habit in habits:
            self.habit_tree.insert("", tk.END, values=(
                habit.title,
                habit.frequency,
                habit.streak,
                habit.total_completions
            ))

    def _habit_checkin(self):
        """习惯打卡"""
        selected = self.habit_tree.selection()
        if not selected:
            messagebox.showwarning("提示", "请选择一个习惯")
            return
        item = self.habit_tree.item(selected[0])
        habit_name = item["values"][0]

        for habit in self.task_manager.get_habits():
            if habit.title == habit_name:
                if self.task_manager.habit_check_in(habit.id):
                    messagebox.showinfo("成功", "打卡成功！")
                    self._refresh_habit_list()
                else:
                    messagebox.showwarning("提示", "今日已打卡或习惯不存在")
                return

    def _delete_habit(self):
        """删除习惯"""
        selected = self.habit_tree.selection()
        if not selected:
            messagebox.showwarning("提示", "请选择一个习惯")
            return
        if messagebox.askyesno("确认", "确定要删除此习惯吗？"):
            item = self.habit_tree.item(selected[0])
            habit_name = item["values"][0]
            for habit in self.task_manager.get_habits():
                if habit.title == habit_name:
                    if self.task_manager.delete_habit(habit.id):
                        messagebox.showinfo("成功", "习惯已删除")
                        self._refresh_habit_list()
                    return

    # 数据管理方法
    def _backup_data(self):
        """备份数据"""
        backup_path = self.data_manager.create_backup()
        messagebox.showinfo("成功", f"备份已创建:\n{backup_path}")

    def _export_data(self, fmt):
        """导出数据"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        try:
            if fmt == "txt":
                path = self.data_manager.export_to_txt(f"export_{timestamp}.txt")
            elif fmt == "excel":
                path = self.data_manager.export_to_excel(f"export_{timestamp}.xlsx")
            else:
                messagebox.showerror("错误", f"不支持的格式：{fmt}")
                return
            messagebox.showinfo("成功", f"数据已导出:\n{path}")
        except Exception as e:
            messagebox.showerror("错误", f"导出失败：{e}")


def main():
    """主函数"""
    root = tk.Tk()
    app = ZhangyChatGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
