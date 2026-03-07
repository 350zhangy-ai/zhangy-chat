#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Zhangy Chat R4 - 深度智能版测试脚本
测试逻辑推理和情感计算功能
"""

import sys
import os

project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from zhangy_chat.logic_engine import LogicEngine
from zhangy_chat.emotion_engine import EmotionEngine
from zhangy_chat.assistant import Assistant


def test_logic_engine():
    """测试逻辑推理引擎"""
    print("\n=== 测试逻辑推理引擎 ===")
    
    engine = LogicEngine()
    
    test_queries = [
        "为什么加班越久效率越低",
        "为什么坚持很难",
        "为什么努力没回报",
        "怎么才能提高工作效率",
        "要不要辞职",
        "考研和工作哪个更好"
    ]
    
    for query in test_queries:
        print(f"\n问题：{query}")
        result = engine.analyze(query)
        print(f"类型：{result.get('type', 'unknown')}")
        print(f"回答：{result.get('content', '')[:100]}...")
    
    print("\n[OK] 逻辑推理引擎测试完成")


def test_emotion_engine():
    """测试情感计算引擎"""
    print("\n=== 测试情感计算引擎 ===")
    
    engine = EmotionEngine(memory_path="test_data/emotion_memory.json")
    
    test_texts = [
        "今天加班好烦啊",
        "终于完成项目了！",
        "我好累，快撑不住了",
        "这件事让我很生气",
        "一个人好孤单"
    ]
    
    for text in test_texts:
        print(f"\n输入：{text}")
        result = engine.recognize(text)
        print(f"识别情感：{result['emotion']} (强度：{result['intensity']})")
        
        response = engine.respond(result['emotion'], text)
        print(f"共情回复：{response[:80]}...")
    
    # 测试情感记忆
    print(f"\n情感摘要：{engine.get_emotion_summary()}")
    
    # 清理测试数据
    import shutil
    if os.path.exists("test_data"):
        shutil.rmtree("test_data")
    
    print("\n[OK] 情感计算引擎测试完成")


def test_assistant_integration():
    """测试 AI 助手集成"""
    print("\n=== 测试 AI 助手集成 ===")
    
    assistant = Assistant()
    
    test_queries = [
        ("我饿了", "实用回复"),
        ("为什么努力没回报", "逻辑推理"),
        ("今天加班好烦", "情感 + 逻辑"),
        ("终于完成项目了！", "正面情感"),
        ("你好", "简单对话")
    ]
    
    for query, expected_type in test_queries:
        print(f"\n问题：{query} (期望：{expected_type})")
        response = assistant.chat(query)
        print(f"回复：{response[:100]}...")
    
    # 测试逻辑推理模式
    print("\n--- 测试 /logic 模式 ---")
    response = assistant.logic_chat("为什么坚持很难")
    print(f"逻辑推理：{response[:100]}...")
    
    # 测试情感管理
    print("\n--- 测试情感管理 ---")
    print(f"情感状态：{assistant.get_emotion_status()}")
    print(f"清除记忆：{assistant.clear_emotion_memory()}")
    
    print("\n[OK] AI 助手集成测试完成")


def main():
    """主函数"""
    print("=" * 50)
    print("  Zhangy Chat R4 - 深度智能版测试")
    print("=" * 50)
    
    try:
        test_logic_engine()
        test_emotion_engine()
        test_assistant_integration()
        
        print("\n" + "=" * 50)
        print("  所有测试通过！")
        print("=" * 50)
    except Exception as e:
        print(f"\n测试失败：{e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
