"""
zhangy chat - 高效、专业的本地 AI 助手 (R3 MiniMind 集成版)

核心模块:
- ZhangyChat: 主类
- TaskManager: 任务/目标/习惯管理
- DataManager: 数据存储/备份/导出
- Assistant: AI 助手核心（MiniMind 模型 + 思考式响应）
- CMDInterface: CMD 命令行界面
- MemoryManager: 内存配置管理
- MoodManager: 心情标签管理
- PresetManager: 场景预设管理
- ThinkingEngine: 思考决策引擎
- ZhangyChatModel: zhangy-chat 模型（基于 MiniMind）
"""

__version__ = "3.0.0"
__author__ = "zhangy"
__license__ = "MIT License"

from .main import ZhangyChat
from .task_manager import TaskManager, Task, Goal, Habit
from .data_manager import DataManager
from .assistant import Assistant
from .cmd_interface import CMDInterface
from .memory_manager import MemoryManager
from .mood_manager import MoodManager
from .preset_manager import PresetManager
from .thinking_engine import ThinkingEngine
from .model import ZhangyChatModel

__all__ = [
    "ZhangyChat",
    "TaskManager",
    "Task",
    "Goal",
    "Habit",
    "DataManager",
    "Assistant",
    "CMDInterface",
    "MemoryManager",
    "MoodManager",
    "PresetManager",
    "ThinkingEngine",
    "ZhangyChatModel"
]
