# Zhangy Chat R2

<div align="center">
  <h3>高效、专业的本地 AI 助手 - 双界面版本</h3>
  <p>GUI 图形界面 + CMD 命令行 | 任务管理 | 情绪疏导 | 数据导出</p>
</div>

## 简介

Zhangy Chat R2 是一个功能全面的本地 AI 助手，支持**图形界面**和**命令行界面**双模式切换。它专为**学生、职场人、自由职业者**设计，提供任务管理、目标规划、情绪疏导、内容辅助等全方位功能，所有数据本地存储，保护隐私。

## 核心特性

### 🎯 双界面切换
- **GUI 图形界面** - 可视化操作，5 个功能标签页（对话/任务/目标/习惯/设置）
- **CMD 命令行** - 15+ 条高效指令，支持 `/add` `/goal` `/review` 等
- **无缝切换** - 一键在两种模式间切换

### 📋 任务与目标管理
- **待办事项** - 添加/删除/标记任务，优先级排序
- **目标规划** - 目标拆解、里程碑管理、进度追踪
- **习惯打卡** - 每日/每周习惯，连续打卡统计
- **复盘报告** - 周期性复盘，生成成长报告

### 💬 AI 助手功能
- **智能问答** - 学习/职场/生活问题解答
- **情绪疏导** - 检测焦虑/沮丧/疲惫情绪，提供心理支持
- **内容辅助** - 文案润色、摘要生成、大纲制定
- **每日小贴士** - 每日一句正能量

### 🔒 数据管理
- **本地存储** - 所有数据存储在本地，不上传云端
- **备份恢复** - 一键备份/恢复数据
- **多格式导出** - 支持 TXT、Excel、CSV 格式导出
- **收藏夹** - 收藏高频问题和答案

## 快速开始

### 环境要求

- Python 3.8+
- 8GB+ RAM
- Windows 10+ / macOS 12+ / Linux (Ubuntu 20.04+)

### 安装

```bash
cd zhangy_chat
pip install -r requirements.txt
```

### 运行

```bash
# GUI 图形界面模式
python gui.py

# CMD 命令行模式
python main.py -cmd

# 或统一入口（默认 GUI）
python main.py
```

## CMD 指令列表

### 任务管理
| 指令 | 说明 | 示例 |
|------|------|------|
| `/add` | 添加任务 | `/add 完成报告 明天截止` |
| `/del` | 删除任务 | `/del task_id` |
| `/list` | 查看任务 | `/list pending` (待完成/已完成/全部) |
| `/mark` | 标记状态 | `/mark task_id completed` |

### 目标规划
| 指令 | 说明 | 示例 |
|------|------|------|
| `/goal add` | 添加目标 | `/goal add 学会 Python 3 个月掌握` |
| `/goal list` | 查看目标 | `/goal list` |
| `/goal milestone` | 添加里程碑 | `/goal milestone goal_id 完成第一章` |
| `/review` | 生成复盘 | `/review 7` (默认 7 天) |
| `/progress` | 查看进度 | `/progress goal_id` |

### 习惯打卡
| 指令 | 说明 | 示例 |
|------|------|------|
| `/habit add` | 添加习惯 | `/habit add 早起 daily` |
| `/habit list` | 查看习惯 | `/habit list` |
| `/habit check` | 打卡 | `/habit check habit_id` |

### 数据管理
| 指令 | 说明 | 示例 |
|------|------|------|
| `/backup` | 备份数据 | `/backup backup_name` |
| `/restore` | 恢复备份 | `/restore backup_name` |
| `/export` | 导出数据 | `/export txt` (txt/excel/csv) |

### 其他
| 指令 | 说明 |
|------|------|
| `/gui` | 切换至图形界面 |
| `/help` | 查看帮助 |
| `/exit` | 退出程序 |

## 项目结构

```
zhangy_chat/
├── .github/
│   └── workflows/
│       └── ci.yml          # CI/CD 自动化测试
├── tests/
│   ├── __init__.py
│   └── test_all.py         # 功能测试脚本
├── zhangy_chat/
│   ├── __init__.py         # 模块导出
│   ├── main.py             # 核心类
│   ├── task_manager.py     # 任务/目标/习惯管理
│   ├── data_manager.py     # 数据存储/备份/导出
│   ├── assistant.py        # AI 助手核心
│   └── cmd_interface.py    # CMD 命令行界面
├── .gitignore
├── CONTRIBUTING.md
├── LICENSE
├── README.md
├── config.yaml             # 配置文件
├── main.py                 # 主程序入口
├── gui.py                  # GUI 图形界面
├── requirements.txt
├── build.py                # 打包脚本
└── setup.py
```

## 配置说明

编辑 `config.yaml` 自定义：

```yaml
personality:
  name: zhangy
  性格:
    - 理性温柔
    - 耐心细致
    - 高效陪伴
  说话风格:
    - 口语化为主，简洁清晰
    - GUI 回应温和，CMD 回应干练

ui:
  theme: light  # light / dark
  font_size: 10
  default_mode: gui  # gui / cmd

data:
  data_dir: data
  backup_dir: backups
  auto_backup: true

reminder:
  task_reminder: true
  procrastination_check: true
```

## 打包发布

```bash
# 打包 GUI 和 CMD 双版本
python build.py

# 输出文件
# dist/zhangy_chat_gui.exe  - GUI 版本
# dist/zhangy_chat_cmd.exe  - CMD 版本
```

## 测试

```bash
# 运行功能测试
python tests/test_all.py
```

## 版本历史

### v2.0.0 (R2)
- ✨ 新增 CMD 命令行界面，支持 15+ 条指令
- ✨ 新增 GUI 图形界面（5 个功能标签页）
- ✨ 新增任务管理模块（待办/目标/习惯）
- ✨ 新增数据管理模块（备份/导出）
- ✨ 新增 AI 助手核心（情绪疏导/内容辅助）
- ✨ 支持双界面无缝切换

### v1.0.0
- 🎉 初始版本发布

## 开源协议

本项目采用 [MIT License](LICENSE) 开源协议。

## 贡献

欢迎提交 Issue 和 Pull Request！

## 联系方式

如有问题或建议，请通过以下方式联系：

- GitHub Issues
- 提交 PR

---

<div align="center">
  <sub>使用 ❤️ 制作 | Zhangy Chat R2</sub>
</div>
