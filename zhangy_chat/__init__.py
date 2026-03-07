"""
zhangy chat - 高效、专业的本地 AI 助手

核心模块:
- ZhangyChat: 主类
- TaskManager: 任务/目标/习惯管理
- DataManager: 数据存储/备份/导出
- Assistant: AI 助手核心
- CMDInterface: CMD 命令行界面
"""

__version__ = "2.0.0"
__author__ = "zhangy"
__license__ = "MIT License"

from .main import ZhangyChat
from .task_manager import TaskManager, Task, Goal, Habit
from .data_manager import DataManager
from .assistant import Assistant
from .cmd_interface import CMDInterface

__all__ = [
    "ZhangyChat",
    "TaskManager",
    "Task",
    "Goal", 
    "Habit",
    "DataManager",
    "Assistant",
    "CMDInterface"
]
