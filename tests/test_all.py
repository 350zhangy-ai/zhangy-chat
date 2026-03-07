#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Zhangy Chat R2 - 测试脚本
验证核心功能
"""

import sys
import os

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from zhangy_chat.task_manager import TaskManager
from zhangy_chat.data_manager import DataManager
from zhangy_chat.assistant import Assistant


def test_task_manager():
    """测试任务管理器"""
    print("\n=== 测试任务管理器 ===")
    
    tm = TaskManager(data_dir="test_data")
    
    # 测试添加任务
    task = tm.add_task("测试任务", "这是一个测试任务", priority=5)
    print(f"✓ 添加任务：{task.title} [ID: {task.id}]")
    
    # 测试获取任务
    tasks = tm.get_tasks()
    print(f"✓ 获取任务列表：共 {len(tasks)} 个任务")
    
    # 测试更新状态
    tm.update_task_status(task.id, "completed")
    print(f"✓ 更新任务状态为 completed")
    
    # 测试添加目标
    goal = tm.add_goal("测试目标", "这是一个测试目标")
    print(f"✓ 添加目标：{goal.title} [ID: {goal.id}]")
    
    # 测试添加里程碑
    tm.add_milestone(goal.id, "里程碑 1")
    tm.add_milestone(goal.id, "里程碑 2")
    print(f"✓ 添加 2 个里程碑")
    
    # 测试完成里程碑
    tm.complete_milestone(goal.id, 0)
    print(f"✓ 完成第 1 个里程碑")
    
    # 测试获取进度
    progress = tm.get_goal_progress(goal.id)
    print(f"✓ 目标进度：{progress}%")
    
    # 测试添加习惯
    habit = tm.add_habit("测试习惯", "daily")
    print(f"✓ 添加习惯：{habit.title} [ID: {habit.id}]")
    
    # 测试打卡
    tm.habit_check_in(habit.id)
    print(f"✓ 习惯打卡成功")
    
    # 测试生成复盘
    review = tm.generate_review(7)
    print(f"✓ 生成复盘报告：{review['period']}")
    
    # 清理测试数据
    import shutil
    if os.path.exists("test_data"):
        shutil.rmtree("test_data")
    
    print("✓ 任务管理器测试通过")


def test_data_manager():
    """测试数据管理器"""
    print("\n=== 测试数据管理器 ===")
    
    dm = DataManager(data_dir="test_data", backup_dir="test_backups")
    
    # 测试配置管理
    dm.set_config("test_key", "test_value")
    value = dm.get_config("test_key")
    print(f"✓ 配置读写：{value}")
    
    # 测试收藏
    fav = dm.add_favorite("测试问题", "测试回答", ["测试"])
    print(f"✓ 添加收藏：{fav['question']}")
    
    # 测试获取收藏
    favs = dm.get_favorites()
    print(f"✓ 获取收藏列表：共 {len(favs)} 个")
    
    # 测试备份
    backup_path = dm.create_backup("test_backup")
    print(f"✓ 创建备份：{backup_path}")
    
    # 测试列出备份
    backups = dm.list_backups()
    print(f"✓ 列出备份：共 {len(backups)} 个")
    
    # 清理测试数据
    import shutil
    if os.path.exists("test_data"):
        shutil.rmtree("test_data")
    if os.path.exists("test_backups"):
        shutil.rmtree("test_backups")
    
    print("✓ 数据管理器测试通过")


def test_assistant():
    """测试 AI 助手"""
    print("\n=== 测试 AI 助手 ===")
    
    assistant = Assistant()
    
    # 测试情绪检测
    responses = [
        ("我感到很焦虑", "情绪疏导"),
        ("今天好累啊", "情绪疏导"),
        ("帮我润色一下这段话", "内容辅助"),
        ("如何管理时间？", "任务建议"),
        ("今天天气不错", "默认问答")
    ]
    
    for query, expected_type in responses:
        response = assistant.chat(query)
        print(f"✓ 测试 {expected_type}: {query[:20]}...")
    
    # 测试每日小贴士
    tip = assistant.get_daily_tip()
    print(f"✓ 每日小贴士：{tip}")
    
    print("✓ AI 助手测试通过")


def main():
    """主函数"""
    print("=" * 50)
    print("  Zhangy Chat R2 - 功能测试")
    print("=" * 50)
    
    try:
        test_task_manager()
        test_data_manager()
        test_assistant()
        
        print("\n" + "=" * 50)
        print("  所有测试通过！✓")
        print("=" * 50)
    except Exception as e:
        print(f"\n测试失败：{e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
