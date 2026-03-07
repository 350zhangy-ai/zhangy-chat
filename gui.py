#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
zhangy chat - 图形界面版本 (R2 双界面版)
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


class ZhangyChatGUI:
    """zhangy chat 图形界面类"""

    def __init__(self, root):
        """初始化 GUI"""
        self.root = root
        self.root.title("zhangy chat - 专业 AI 助手")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)

        # 加载配置
        self.config = self._load_config()
        self.name = self.config.get('name', 'zhangy chat')
        
        # 初始化核心模块
        self.task_manager = TaskManager()
        self.data_manager = DataManager()
        self.assistant = Assistant(self.config)
        
        # 当前标签页
        self.current_tab = "chat"
        
        # 创建界面
        self._create_widgets()
        
        # 加载初始数据
        self._load_initial_data()

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
            text=f"  {self.name}  R2",
            font=("Microsoft YaHei", 16, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title_label.pack(side=tk.LEFT, padx=10, pady=10)
        
        # CMD 模式切换按钮
        cmd_btn = tk.Button(
            title_frame,
            text="切换 CMD 模式",
            command=self._switch_to_cmd,
            font=("Microsoft YaHei", 9),
            bg="#34495e",
            fg="white",
            relief=tk.FLAT,
            padx=10,
            pady=5
        )
        cmd_btn.pack(side=tk.RIGHT, padx=10, pady=10)

        # 主内容区域 - 使用 Notebook 实现标签页
        main_frame = tk.Frame(self.root, bg="#ecf0f1")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建各功能标签页
        self._create_chat_tab()
        self._create_task_tab()
        self._create_goal_tab()
        self._create_habit_tab()
        self._create_settings_tab()

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
        
        # 每日小贴士
        self.tip_label = tk.Label(
            status_frame,
            text=self.assistant.get_daily_tip(),
            font=("Microsoft YaHei", 9),
            bg="#2c3e50",
            fg="#2ecc71"
        )
        self.tip_label.pack(side=tk.RIGHT, padx=10)

    def _create_chat_tab(self):
        """创建聊天标签页"""
        chat_frame = tk.Frame(self.notebook, bg="#ecf0f1")
        self.notebook.add(chat_frame, text="💬 对话")
        
        # 聊天记录显示区域
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            font=("Microsoft YaHei", 10),
            bg="white",
            fg="#2c3e50",
            padx=10,
            pady=10
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.chat_display.config(state=tk.DISABLED)

        # 输入区域
        input_frame = tk.Frame(chat_frame, bg="#ecf0f1")
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
        button_frame = tk.Frame(input_frame, bg="#ecf0f1")
        button_frame.pack(fill=tk.X, pady=5)

        send_btn = tk.Button(
            button_frame,
            text="发送",
            command=self.send_message,
            font=("Microsoft YaHei", 10),
            bg="#3498db",
            fg="white",
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
            relief=tk.FLAT,
            padx=20,
            pady=8
        )
        clear_btn.pack(side=tk.RIGHT, padx=5)

    def _create_task_tab(self):
        """创建任务标签页"""
        task_frame = tk.Frame(self.notebook, bg="#ecf0f1")
        self.notebook.add(task_frame, text="📋 任务")
        
        # 任务输入区
        input_frame = tk.LabelFrame(task_frame, text="添加任务", font=("Microsoft YaHei", 10, "bold"), bg="#ecf0f1")
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(input_frame, text="任务标题:", bg="#ecf0f1").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.task_title = tk.Entry(input_frame, font=("Microsoft YaHei", 10), width=40)
        self.task_title.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(input_frame, text="描述:", bg="#ecf0f1").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.task_desc = tk.Entry(input_frame, font=("Microsoft YaHei", 10), width=40)
        self.task_desc.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(input_frame, text="优先级 (1-5):", bg="#ecf0f1").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.task_priority = ttk.Spinbox(input_frame, from_=1, to=5, width=10, font=("Microsoft YaHei", 10))
        self.task_priority.set(3)
        self.task_priority.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        
        add_btn = tk.Button(
            input_frame,
            text="添加任务",
            command=self._add_task,
            font=("Microsoft YaHei", 10),
            bg="#27ae60",
            fg="white",
            relief=tk.FLAT,
            padx=15,
            pady=5
        )
        add_btn.grid(row=3, column=1, sticky=tk.E, padx=5, pady=10)
        
        # 任务列表区
        list_frame = tk.LabelFrame(task_frame, text="任务列表", font=("Microsoft YaHei", 10, "bold"), bg="#ecf0f1")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 筛选按钮
        filter_frame = tk.Frame(list_frame, bg="#ecf0f1")
        filter_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(filter_frame, text="筛选:", bg="#ecf0f1").pack(side=tk.LEFT)
        self.task_filter = tk.StringVar(value="pending")
        for status, label in [("pending", "待完成"), ("in_progress", "进行中"), ("completed", "已完成"), ("all", "全部")]:
            tk.Radiobutton(
                filter_frame,
                text=label,
                variable=self.task_filter,
                value=status,
                bg="#ecf0f1",
                command=self._refresh_task_list
            ).pack(side=tk.LEFT, padx=5)
        
        # 任务列表
        columns = ("ID", "标题", "优先级", "状态", "截止")
        self.task_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=10)
        for col in columns:
            self.task_tree.heading(col, text=col)
            self.task_tree.column(col, width=100)
        self.task_tree.column("标题", width=300)
        self.task_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 操作按钮
        op_frame = tk.Frame(list_frame, bg="#ecf0f1")
        op_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Button(op_frame, text="刷新", command=self._refresh_task_list, bg="#3498db", fg="white").pack(side=tk.LEFT, padx=2)
        tk.Button(op_frame, text="完成", command=self._complete_task, bg="#27ae60", fg="white").pack(side=tk.LEFT, padx=2)
        tk.Button(op_frame, text="删除", command=self._delete_task, bg="#e74c3c", fg="white").pack(side=tk.LEFT, padx=2)

    def _create_goal_tab(self):
        """创建目标标签页"""
        goal_frame = tk.Frame(self.notebook, bg="#ecf0f1")
        self.notebook.add(goal_frame, text="🎯 目标")
        
        # 目标输入区
        input_frame = tk.LabelFrame(goal_frame, text="添加目标", font=("Microsoft YaHei", 10, "bold"), bg="#ecf0f1")
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(input_frame, text="目标标题:", bg="#ecf0f1").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.goal_title = tk.Entry(input_frame, font=("Microsoft YaHei", 10), width=40)
        self.goal_title.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(input_frame, text="描述:", bg="#ecf0f1").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.goal_desc = tk.Entry(input_frame, font=("Microsoft YaHei", 10), width=40)
        self.goal_desc.grid(row=1, column=1, padx=5, pady=5)
        
        add_btn = tk.Button(
            input_frame,
            text="添加目标",
            command=self._add_goal,
            font=("Microsoft YaHei", 10),
            bg="#27ae60",
            fg="white",
            relief=tk.FLAT,
            padx=15,
            pady=5
        )
        add_btn.grid(row=2, column=1, sticky=tk.E, padx=5, pady=10)
        
        # 目标列表区
        list_frame = tk.LabelFrame(goal_frame, text="目标列表", font=("Microsoft YaHei", 10, "bold"), bg="#ecf0f1")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        columns = ("ID", "标题", "状态", "进度")
        self.goal_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=8)
        for col in columns:
            self.goal_tree.heading(col, text=col)
            self.goal_tree.column(col, width=150)
        self.goal_tree.column("标题", width=400)
        self.goal_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 操作按钮
        op_frame = tk.Frame(list_frame, bg="#ecf0f1")
        op_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Button(op_frame, text="刷新", command=self._refresh_goal_list, bg="#3498db", fg="white").pack(side=tk.LEFT, padx=2)
        tk.Button(op_frame, text="生成复盘", command=self._generate_review, bg="#9b59b6", fg="white").pack(side=tk.LEFT, padx=2)

    def _create_habit_tab(self):
        """创建习惯标签页"""
        habit_frame = tk.Frame(self.notebook, bg="#ecf0f1")
        self.notebook.add(habit_frame, text="✅ 习惯")
        
        # 习惯输入区
        input_frame = tk.LabelFrame(habit_frame, text="添加习惯", font=("Microsoft YaHei", 10, "bold"), bg="#ecf0f1")
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(input_frame, text="习惯名称:", bg="#ecf0f1").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.habit_name = tk.Entry(input_frame, font=("Microsoft YaHei", 10), width=30)
        self.habit_name.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(input_frame, text="频率:", bg="#ecf0f1").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.habit_freq = ttk.Combobox(input_frame, values=["daily", "weekly"], width=10, font=("Microsoft YaHei", 10))
        self.habit_freq.set("daily")
        self.habit_freq.grid(row=0, column=3, padx=5, pady=5)
        
        add_btn = tk.Button(
            input_frame,
            text="添加习惯",
            command=self._add_habit,
            font=("Microsoft YaHei", 10),
            bg="#27ae60",
            fg="white",
            relief=tk.FLAT,
            padx=15,
            pady=5
        )
        add_btn.grid(row=1, column=3, sticky=tk.E, padx=5, pady=10)
        
        # 习惯列表区
        list_frame = tk.LabelFrame(habit_frame, text="习惯列表", font=("Microsoft YaHei", 10, "bold"), bg="#ecf0f1")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        columns = ("名称", "频率", "连续天数", "总次数")
        self.habit_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=8)
        for col in columns:
            self.habit_tree.heading(col, text=col)
            self.habit_tree.column(col, width=150)
        self.habit_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 操作按钮
        op_frame = tk.Frame(list_frame, bg="#ecf0f1")
        op_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Button(op_frame, text="刷新", command=self._refresh_habit_list, bg="#3498db", fg="white").pack(side=tk.LEFT, padx=2)
        tk.Button(op_frame, text="打卡", command=self._habit_checkin, bg="#27ae60", fg="white").pack(side=tk.LEFT, padx=2)
        tk.Button(op_frame, text="删除", command=self._delete_habit, bg="#e74c3c", fg="white").pack(side=tk.LEFT, padx=2)

    def _create_settings_tab(self):
        """创建设置标签页"""
        settings_frame = tk.Frame(self.notebook, bg="#ecf0f1")
        self.notebook.add(settings_frame, text="⚙️ 设置")
        
        # 数据管理区
        data_frame = tk.LabelFrame(settings_frame, text="数据管理", font=("Microsoft YaHei", 10, "bold"), bg="#ecf0f1")
        data_frame.pack(fill=tk.X, padx=10, pady=10)
        
        btn_frame = tk.Frame(data_frame, bg="#ecf0f1")
        btn_frame.pack(padx=10, pady=10)
        
        tk.Button(btn_frame, text="备份数据", command=self._backup_data, bg="#3498db", fg="white", width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="导出数据 (TXT)", command=lambda: self._export_data("txt"), bg="#3498db", fg="white", width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="导出数据 (Excel)", command=lambda: self._export_data("excel"), bg="#3498db", fg="white", width=15).pack(side=tk.LEFT, padx=5)
        
        # 界面设置区
        ui_frame = tk.LabelFrame(settings_frame, text="界面设置", font=("Microsoft YaHei", 10, "bold"), bg="#ecf0f1")
        ui_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(ui_frame, text="主题:", bg="#ecf0f1", font=("Microsoft YaHei", 10)).grid(row=0, column=0, padx=10, pady=10)
        self.theme_var = tk.StringVar(value="light")
        ttk.Radiobutton(ui_frame, text="浅色", variable=self.theme_var, value="light").grid(row=0, column=1, padx=5)
        ttk.Radiobutton(ui_frame, text="深色", variable=self.theme_var, value="dark").grid(row=0, column=2, padx=5)
        
        tk.Label(ui_frame, text="字体大小:", bg="#ecf0f1", font=("Microsoft YaHei", 10)).grid(row=1, column=0, padx=10, pady=10)
        self.font_size = ttk.Spinbox(ui_frame, from_=8, to=16, width=10, font=("Microsoft YaHei", 10))
        self.font_size.set(10)
        self.font_size.grid(row=1, column=1, sticky=tk.W, padx=5, pady=10)
        
        apply_btn = tk.Button(
            ui_frame,
            text="应用设置",
            command=self._apply_settings,
            font=("Microsoft YaHei", 10),
            bg="#27ae60",
            fg="white",
            relief=tk.FLAT,
            padx=15,
            pady=5
        )
        apply_btn.grid(row=2, column=1, sticky=tk.W, padx=5, pady=10)
        
        # 关于区
        about_frame = tk.LabelFrame(settings_frame, text="关于", font=("Microsoft YaHei", 10, "bold"), bg="#ecf0f1")
        about_frame.pack(fill=tk.X, padx=10, pady=10)
        
        about_text = """
Zhangy Chat R2 - 高效、专业的本地 AI 助手

版本：2.0.0
作者：zhangy
协议：MIT License

功能特点:
• 双界面切换 (GUI + CMD)
• 任务管理、目标规划、习惯打卡
• 情绪疏导、内容辅助
• 数据备份与导出
"""
        tk.Label(about_frame, text=about_text, bg="#ecf0f1", justify=tk.LEFT, font=("Microsoft YaHei", 9)).pack(padx=10, pady=10)

    def _load_initial_data(self):
        """加载初始数据"""
        self._refresh_task_list()
        self._refresh_goal_list()
        self._refresh_habit_list()
        
        # 显示欢迎消息
        self._add_message("系统", f"欢迎使用 {self.name}！我是你的专属 AI 助手，有任何问题都可以问我。", "#27ae60")

    def _switch_to_cmd(self):
        """切换到 CMD 模式"""
        if messagebox.askyesno("切换模式", "确定要切换到 CMD 模式吗？"):
            self.root.quit()
            subprocess.Popen([sys.executable, "-m", "zhangy_chat.cmd_interface", "-cmd"])

    def send_message(self):
        """发送消息"""
        user_input = self.input_text.get("1.0", tk.END).strip()
        if not user_input:
            return

        self.input_text.delete("1.0", tk.END)
        self._add_message("用户", user_input, "#3498db")
        self.status_label.config(text="正在思考...")
        
        thread = threading.Thread(target=self._process_response, args=(user_input,))
        thread.start()

    def _process_response(self, user_input):
        """处理响应"""
        try:
            response = self.assistant.chat(user_input)
            self.root.after(0, lambda: self._add_message(self.name, response, "#2c3e50"))
        except Exception as e:
            self.root.after(0, lambda: self._add_message("系统", f"错误：{str(e)}", "#e74c3c"))
        finally:
            self.root.after(0, lambda: self.status_label.config(text="就绪"))

    def _add_message(self, sender, message, color):
        """添加消息到聊天记录"""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"\n{sender}:\n", ("sender",))
        self.chat_display.insert(tk.END, f"{message}\n\n", ("message",))
        self.chat_display.tag_config("sender", font=("Microsoft YaHei", 10, "bold"), foreground=color)
        self.chat_display.tag_config("message", font=("Microsoft YaHei", 10), foreground="#2c3e50")
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)

    def clear_chat(self):
        """清空聊天记录"""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete("1.0", tk.END)
        self.chat_display.config(state=tk.DISABLED)

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
        
        text = scrolledtext.ScrolledText(review_window, font=("Microsoft YaHei", 10))
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        content = f"""复盘报告：{review['period']}
{'='*40}

✅ 完成任务：{review['completed_tasks']} 个
"""
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
        
        # 根据名称查找习惯 ID
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

    def _apply_settings(self):
        """应用设置"""
        # 主题设置
        if self.theme_var.get() == "dark":
            self.root.configure(bg="#2c3e50")
        else:
            self.root.configure(bg="#ecf0f1")
        
        # 字体大小
        font_size = int(self.font_size.get())
        self.chat_display.config(font=("Microsoft YaHei", font_size))
        
        messagebox.showinfo("成功", "设置已应用")


def main():
    """主函数"""
    root = tk.Tk()
    app = ZhangyChatGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
