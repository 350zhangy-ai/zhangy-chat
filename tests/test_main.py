#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
zhangy chat - 测试文件
"""

import unittest
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from main import ZhangyChat


class TestZhangyChat(unittest.TestCase):
    """测试zhangy chat主类"""

    def setUp(self):
        """测试前准备"""
        self.chat = ZhangyChat()

    def test_initialization(self):
        """测试初始化"""
        self.assertEqual(self.chat.name, "zhangy chat")
        self.assertIsNotNone(self.chat.config)

    def test_process_query(self):
        """测试查询处理"""
        query = "测试查询"
        response = self.chat.process_query(query)
        self.assertIsNotNone(response)
        self.assertIn("zhangy chat", response)

    def test_format_response(self):
        """测试响应格式化"""
        response = self.chat._format_response("测试内容")
        self.assertIsNotNone(response)


if __name__ == "__main__":
    unittest.main()