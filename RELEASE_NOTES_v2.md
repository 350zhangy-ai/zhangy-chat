# GitHub Release v2.0.0 发布说明

## 操作步骤

### 方法 1: 通过 GitHub UI 创建 Release

1. 访问 https://github.com/350zhangy-ai/zhangy-chat/releases/new
2. 选择 tag: `v2.0.0` (已创建)
3. 标题: `Zhangy Chat R2 - 双界面版本`
4. 复制下方发布说明内容
5. 点击 "Publish release"

### 方法 2: 使用 GitHub CLI

```bash
# 安装 gh CLI (如果未安装)
# Windows: winget install GitHub.cli

# 创建 release
gh release create v2.0.0 --title "Zhangy Chat R2 - 双界面版本" --notes-file RELEASE_NOTES_v2.md

# 或直接创建
gh release create v2.0.0 --title "Zhangy Chat R2 - 双界面版本" --generate-notes
```

---

## 发布说明内容

### 🎉 主要更新

Zhangy Chat R2 是一个重大版本更新，新增了**双界面切换**功能，支持**图形界面**和**命令行界面**两种操作模式，并添加了完整的**任务管理**、**数据导出**、**情绪疏导**等功能。

### ✨ 新功能

#### 🎯 双界面切换
- **GUI 图形界面**: 5 个功能标签页（对话/任务/目标/习惯/设置）
- **CMD 命令行**: 15+ 条高效指令
- **一键切换**: 在两种模式间无缝切换

#### 📋 任务与目标管理
- **待办事项**: 添加/删除/标记任务，优先级排序
- **目标规划**: 目标拆解、里程碑管理、进度追踪
- **习惯打卡**: 每日/每周习惯，连续打卡统计
- **复盘报告**: 周期性复盘，生成成长报告

#### 💬 AI 助手增强
- **智能问答**: 学习/职场/生活问题解答
- **情绪疏导**: 焦虑/沮丧/疲惫/压力检测与疏导
- **内容辅助**: 文案润色、摘要生成、大纲制定
- **每日小贴士**: 每日一句正能量

#### 🔒 数据管理
- **本地存储**: 所有数据存储在本地，保护隐私
- **备份恢复**: 一键备份/恢复数据
- **多格式导出**: 支持 TXT、Excel、CSV 格式导出
- **收藏夹**: 收藏高频问题和答案

### 📝 CMD 指令列表

```
任务管理:
  /add <标题> [描述]           添加任务
  /del <ID>                   删除任务
  /list [状态]                查看任务
  /mark <ID> <状态>           标记任务状态

目标规划:
  /goal add <标题> [描述]      添加目标
  /goal list                  查看目标
  /goal milestone <ID> <内容>  添加里程碑
  /review [天数]              生成复盘报告
  /progress <ID>              查看目标进度

习惯打卡:
  /habit add <名称> [频率]     添加习惯
  /habit list                 查看习惯
  /habit check <ID>           打卡

数据管理:
  /backup [名称]              备份数据
  /restore <名称>             恢复备份
  /export <格式>              导出数据 (txt/excel/csv)

其他:
  /gui                        切换至图形界面
  /help                       查看帮助
  /exit                       退出
```

### 🚀 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# GUI 模式
python gui.py

# CMD 模式
python main.py -cmd
```

### 📦 打包发布

```bash
# 打包 GUI 和 CMD 双版本
python build.py

# 输出:
# dist/zhangy_chat_gui.exe  - GUI 版本
# dist/zhangy_chat_cmd.exe  - CMD 版本
```

### 📋 系统要求

- Python 3.8+
- 8GB+ RAM
- Windows 10+ / macOS 12+ / Linux (Ubuntu 20.04+)

### 📁 新增文件

- `zhangy_chat/task_manager.py` - 任务/目标/习惯管理模块
- `zhangy_chat/data_manager.py` - 数据存储/备份/导出模块
- `zhangy_chat/assistant.py` - AI 助手核心模块
- `zhangy_chat/cmd_interface.py` - CMD 命令行界面模块
- `tests/test_all.py` - 功能测试脚本

### 🔄 更新文件

- `gui.py` - 全新 GUI 图形界面（5 标签页）
- `main.py` - 支持 -cmd 参数
- `config.yaml` - 新增 UI/数据/提醒配置
- `build.py` - 支持双版本打包
- `README.md` - 完整更新文档

### 📊 代码统计

- 新增代码：~2000 行
- 修改文件：11 个
- 新增模块：4 个核心模块
- 新增指令：15+ 条 CMD 指令

### ⚠️ 注意事项

- 此版本为重大更新，建议备份原有数据
- 配置文件格式有更新，请检查 config.yaml
- Python 依赖更新，请运行 `pip install -r requirements.txt`

### 📄 开源协议

MIT License

---

**Full Changelog**: https://github.com/350zhangy-ai/zhangy-chat/compare/v1.0.0...v2.0.0
