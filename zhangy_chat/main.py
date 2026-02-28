#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
zhangy chat - 主程序
"""

import yaml
from pathlib import Path


class ZhangyChat:
    """zhangy chat 主类"""

    def __init__(self, config_path="config.yaml"):
        """初始化zhangy chat"""
        self.config = self._load_config(config_path)
        self.name = self.config.get('name', 'zhangy chat')
        self.personality = self.config.get('personality', {})
        self.functions = self.config.get('functions', {})
        self.response_rules = self.config.get('response_rules', {})

    def _load_config(self, config_path):
        """加载配置文件"""
        config_file = Path(config_path)
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        return {}

    def process_query(self, query):
        """处理用户查询"""
        response = self._generate_response(query)
        return self._format_response(response)

    def _generate_response(self, query):
        """生成回答"""
        # 核心处理逻辑
        personality_name = self.personality.get('name', 'zhangy')
        personality_traits = ', '.join(self.personality.get('性格', ['专业', '高效']))

        return f"""## {personality_name} 分析

**问题**: {query}

### 解决方案

针对您的问题，建议如下：

1. **诊断分析**: 识别问题的关键因素
2. **执行方案**: 提供具体可操作的步骤
3. **验证方法**: 确保方案有效性

### 实施建议

请根据上述方案执行，如需进一步协助，请提供更多细节。

---
*{personality_traits} AI助手*
"""

    def _format_response(self, response):
        """格式化回答"""
        return response


def main():
    """主函数"""
    print("=" * 50)
    print("  zhangy chat - 专业AI助手")
    print("  输入 'exit' 退出")
    print("=" * 50)

    chat = ZhangyChat()

    while True:
        try:
            query = input("\n> ").strip()

            if query.lower() in ['exit', 'quit', '退出']:
                print("再见！")
                break

            if not query:
                continue

            response = chat.process_query(query)
            print(response)

        except KeyboardInterrupt:
            print("\n再见！")
            break
        except Exception as e:
            print(f"错误: {e}")


if __name__ == "__main__":
    main()