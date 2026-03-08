#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
外部 AI 调用模块
支持调用 DeepSeek、文心一言、通义千问等在线 AI 服务
"""

import json
import urllib.request
import urllib.error


class ExternalAI:
    """外部 AI 调用类"""
    
    def __init__(self):
        self.api_key = ""
        self.api_url = ""
        self.provider = "none"  # none, deepseek, wenxin, qwen
        
    def set_provider(self, provider: str, api_key: str = ""):
        """设置 AI 提供商"""
        self.provider = provider
        self.api_key = api_key
        
        # 设置 API URL
        if provider == "deepseek":
            self.api_url = "https://api.deepseek.com/v1/chat/completions"
        elif provider == "wenxin":
            self.api_url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions"
        elif provider == "qwen":
            self.api_url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
    
    def chat(self, message: str) -> str:
        """发送消息并获取回复"""
        if self.provider == "none":
            return None
            
        try:
            if self.provider == "deepseek":
                return self._call_deepseek(message)
            elif self.provider == "wenxin":
                return self._call_wenxin(message)
            elif self.provider == "qwen":
                return self._call_qwen(message)
        except Exception as e:
            return f"调用失败：{str(e)}"
        
        return None
    
    def _call_deepseek(self, message: str) -> str:
        """调用 DeepSeek"""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        data = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "user", "content": message}
            ],
            "temperature": 0.7
        }
        
        req = urllib.request.Request(
            self.api_url,
            data=json.dumps(data).encode('utf-8'),
            headers=headers,
            method='POST'
        )
        
        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result['choices'][0]['message']['content']
    
    def _call_wenxin(self, message: str) -> str:
        """调用文心一言"""
        # 需要先获取 access_token
        access_token = self._get_wenxin_token()
        
        url = f"{self.api_url}?access_token={access_token}"
        headers = {"Content-Type": "application/json"}
        
        data = {
            "messages": [
                {"role": "user", "content": message}
            ]
        }
        
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode('utf-8'),
            headers=headers,
            method='POST'
        )
        
        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result['result']
    
    def _get_wenxin_token(self) -> str:
        """获取文心一言 access_token"""
        # 需要 API Key 和 Secret Key
        return self.api_key  # 简化处理
    
    def _call_qwen(self, message: str) -> str:
        """调用通义千问"""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        data = {
            "model": "qwen-turbo",
            "input": {
                "messages": [
                    {"role": "user", "content": message}
                ]
            }
        }
        
        req = urllib.request.Request(
            self.api_url,
            data=json.dumps(data).encode('utf-8'),
            headers=headers,
            method='POST'
        )
        
        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result['output']['text']


# 预设的 AI 服务
AI_PROVIDERS = {
    "none": "不使用外部 AI",
    "deepseek": "DeepSeek（深度求索）",
    "wenxin": "文心一言（百度）",
    "qwen": "通义千问（阿里）",
}
