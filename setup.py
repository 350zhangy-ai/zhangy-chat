#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
zhangy chat - 安装脚本
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="zhangy-chat",
    version="1.0.0",
    author="zhangy",
    author_email="contact@zhangy.chat",
    description="高效、专业的本地AI助手",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zhangy/zhangy-chat",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "torch>=2.0.0",
        "transformers>=4.30.0",
        "accelerate>=0.20.0",
        "fastapi>=0.100.0",
        "uvicorn>=0.22.0",
        "pyyaml>=6.0",
    ],
    entry_points={
        "console_scripts": [
            "zhangy-chat=zhangy_chat.main:main",
        ],
    },
)