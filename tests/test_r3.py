#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Zhangy Chat R3 - 功能测试脚本
测试新增功能：内存配置、心情选择、预设管理
"""

import sys
import os

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from zhangy_chat.memory_manager import MemoryManager
from zhangy_chat.mood_manager import MoodManager
from zhangy_chat.preset_manager import PresetManager
from zhangy_chat.assistant import Assistant


def test_memory_manager():
    """测试内存管理器"""
    print("\n=== 测试内存管理器 ===")
    
    mm = MemoryManager(config_path="test_data/memory_config.json")
    
    # 测试获取内存信息
    info = mm.get_memory_info()
    print(f"✓ 实际内存：{info['actual']}GiB")
    print(f"✓ 已选内存：{info['selected']}GiB")
    
    # 测试设置内存
    for mem in [8, 16, 32, 64]:
        result = mm.set_memory(mem)
        if result['success']:
            print(f"✓ 设置 {mem}GiB: 成功")
            print(f"  缓存：{result['config']['cache_size']}MB")
            print(f"  并发：{result['config']['max_concurrent']}")
        else:
            print(f"⚠ 设置 {mem}GiB: {result['message']}")
    
    # 测试低内存模式
    mm.set_memory(8)
    print(f"✓ 低内存模式：{mm.is_low_memory_mode()}")
    
    # 测试高内存模式
    mm.set_memory(32)
    print(f"✓ 高内存模式：{mm.is_high_memory_mode()}")
    
    # 清理测试数据
    import shutil
    if os.path.exists("test_data"):
        shutil.rmtree("test_data")
    
    print("✓ 内存管理器测试通过")


def test_mood_manager():
    """测试心情管理器"""
    print("\n=== 测试心情管理器 ===")
    
    mood = MoodManager(config_path="test_data/mood_config.json")
    
    # 测试获取所有心情
    moods = mood.get_all_moods()
    print(f"✓ 心情标签数量：{len(moods)}")
    for key, info in moods.items():
        print(f"  {info['icon']} {info['name']} - {info['style']}")
    
    # 测试设置心情
    test_moods = ["anxious", "focused", "relaxed", "calm", "tired"]
    for m in test_moods:
        result = mood.set_mood(m)
        if result['success']:
            print(f"✓ 设置心情 {m}: {result['message']}")
    
    # 测试心情回复
    mood.set_mood("anxious")
    prefix = mood.get_response_prefix()
    suffix = mood.get_response_suffix()
    print(f"✓ 焦虑模式前缀：{prefix}")
    print(f"✓ 焦虑模式后缀：{suffix}")
    
    # 测试模式判断
    mood.set_mood("focused")
    print(f"✓ 效率模式：{mood.is_efficiency_mode()}")
    
    mood.set_mood("tired")
    print(f"✓ 共情模式：{mood.is_empathetic_mode()}")
    
    # 清理测试数据
    import shutil
    if os.path.exists("test_data"):
        shutil.rmtree("test_data")
    
    print("✓ 心情管理器测试通过")


def test_preset_manager():
    """测试预设管理器"""
    print("\n=== 测试预设管理器 ===")
    
    pm = PresetManager(
        presets_path="test_data/presets.json",
        user_presets_path="test_data/user_presets.json"
    )
    
    # 测试获取所有预设
    presets = pm.get_all_presets()
    print(f"✓ 预设数量：{len(presets)}")
    for p in presets:
        print(f"  {p['icon']} {p['name']} - {p['description']}")
    
    # 测试切换预设
    test_presets = ["office", "exam", "casual", "emotional"]
    for p in test_presets:
        result = pm.set_preset(p)
        if result['success']:
            print(f"✓ 切换预设 {p}: {result['message']}")
    
    # 测试获取配置
    config = pm.get_preset_config("office")
    print(f"✓ 办公预设专注模式：{config.get('focus_mode')}")
    
    # 测试自定义预设
    result = pm.add_custom_preset(
        name="测试预设",
        config={"focus_mode": True},
        icon="🧪"
    )
    if result['success']:
        print(f"✓ 添加自定义预设：{result['message']}")
        preset_key = result['preset_key']
        
        # 测试删除自定义预设
        del_result = pm.delete_custom_preset(preset_key)
        print(f"✓ 删除自定义预设：{del_result['message']}")
    
    # 清理测试数据
    import shutil
    if os.path.exists("test_data"):
        shutil.rmtree("test_data")
    
    print("✓ 预设管理器测试通过")


def test_assistant_with_managers():
    """测试 AI 助手与管理器集成"""
    print("\n=== 测试 AI 助手集成 ===")
    
    mood = MoodManager(config_path="test_data/mood_config.json")
    pm = PresetManager(
        presets_path="test_data/presets.json",
        user_presets_path="test_data/user_presets.json"
    )
    
    assistant = Assistant(mood_manager=mood, preset_manager=pm)
    
    # 测试不同心情下的回复
    test_queries = [
        ("我感到很焦虑", "anxious"),
        ("今天好累啊", "tired"),
        ("如何管理时间？", "calm"),
        ("帮我制定学习计划", "focused")
    ]
    
    for query, set_mood in test_queries:
        mood.set_mood(set_mood)
        response = assistant.chat(query)
        print(f"✓ 心情 {set_mood}: {query[:10]}... -> {len(response)} 字")
    
    # 测试不同预设下的回复
    pm.set_preset("office")
    response = assistant.chat("如何提高工作效率？")
    print(f"✓ 办公预设回复长度：{len(response)} 字")
    
    pm.set_preset("casual")
    response = assistant.chat("今天有什么好玩的？")
    print(f"✓ 休闲预设回复长度：{len(response)} 字")
    
    # 测试每日小贴士
    mood.set_mood("relaxed")
    tip = assistant.get_daily_tip()
    print(f"✓ 每日小贴士：{tip}")
    
    # 清理测试数据
    import shutil
    if os.path.exists("test_data"):
        shutil.rmtree("test_data")
    
    print("✓ AI 助手集成测试通过")


def test_cmd_interface_r3():
    """测试 CMD 界面 R3 指令"""
    print("\n=== 测试 CMD 界面 R3 指令 ===")
    
    from zhangy_chat.cmd_interface import CMDInterface
    
    ci = CMDInterface()
    
    # 测试内存指令
    print("\n测试 /mem 指令:")
    ci._cmd_mem("16")
    ci._cmd_mem("")  # 查看当前配置
    
    # 测试心情指令
    print("\n测试 /mood 指令:")
    ci._cmd_mood("高效")
    ci._cmd_mood("")  # 查看当前心情
    
    # 测试预设指令
    print("\n测试 /preset 指令:")
    ci._cmd_preset("办公")
    ci._cmd_preset("")  # 查看所有预设
    
    # 测试状态指令
    print("\n测试 /status 指令:")
    ci._cmd_status("")
    
    print("\n✓ CMD 界面 R3 指令测试通过")


def main():
    """主函数"""
    print("=" * 50)
    print("  Zhangy Chat R3 - 功能测试")
    print("=" * 50)
    
    try:
        test_memory_manager()
        test_mood_manager()
        test_preset_manager()
        test_assistant_with_managers()
        test_cmd_interface_r3()
        
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
