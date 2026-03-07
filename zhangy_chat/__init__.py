"""
zhangy chat - 高效、专业的本地 AI 助手 (R4 深度智能版)

核心模块:
- ZhangyChat: 主类
- TaskManager: 任务/目标/习惯管理
- DataManager: 数据存储/备份/导出
- Assistant: AI 助手核心（逻辑推理 + 情感计算）
- CMDInterface: CMD 命令行界面
- MemoryManager: 内存配置管理
- MoodManager: 心情标签管理
- PresetManager: 场景预设管理
- LogicEngine: 逻辑推理引擎 (R4 新增)
- EmotionEngine: 情感计算引擎 (R4 新增)
"""

__version__ = "4.0.0"
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
from .logic_engine import LogicEngine
from .emotion_engine import EmotionEngine

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
    "LogicEngine",
    "EmotionEngine"
]
