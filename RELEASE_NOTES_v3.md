# GitHub Release v3.0.0 发布说明

## 操作步骤

### 方法 1: 通过 GitHub UI 创建 Release

1. 访问 https://github.com/350zhangy-ai/zhangy-chat/releases/new
2. 选择 tag: `v3.0.0`
3. 标题: `Zhangy Chat R3 - 智能适配版本`
4. 复制下方发布说明内容
5. 点击 "Publish release"

### 方法 2: 使用 GitHub CLI

```bash
gh release create v3.0.0 --title "Zhangy Chat R3 - 智能适配版本" --generate-notes
```

---

## 发布说明内容

### 🎉 主要更新

Zhangy Chat R3 是一个智能适配版本，在 R2 基础上新增**内存配置**、**心情选择**、**场景预设**三大核心功能，实现真正的个性化适配体验。

### ✨ R3 新增功能

#### 🔧 内存配置 (8/16/32/64GiB)
- **智能检测**: 自动检测物理内存，推荐最优配置
- **参数适配**: 根据内存配置调整缓存 (64-1024MB)、并发数 (2-16)、批次大小 (16-128)
- **低配保护**: 8GiB 模式下内存占用≤150MB
- **高配加速**: 64GiB 模式下全量加载，响应更快
- **GUI 配置**: 设置页下拉框选择，无需重启生效
- **CMD 指令**: `/mem [8/16/32/64]`

#### 💚 心情选择 (5 种标签)
- **😟 焦虑/低落**: 共情治愈，语气温柔
- **🎯 高效/专注**: 简洁干练，直奔主题
- **😊 轻松/愉悦**: 亲切活泼，增加互动
- **🌿 平静/温和**: 温和平稳，给予安全感
- **😴 疲惫/需要休息**: 关怀为主，强调休息
- **话术映射**: 每种心情配备专属前缀/后缀/风格指南
- **GUI 面板**: 对话页顶部一键切换
- **CMD 指令**: `/mood [焦虑/高效/轻松/平静/疲惫]`

#### 📋 场景预设 (4 类模式)
- **💼 高效办公**: 任务优先、简洁回应、专注模式
- **📚 备考冲刺**: 学习计划、打卡提醒、知识点梳理
- **🍵 休闲陪伴**: 轻松聊天、生活建议、兴趣话题
- **💚 情绪疏导**: 共情倾听、压力缓解、心理调节
- **功能联动**: 预设自动调整功能开关、界面显示、回应风格
- **GUI 选择**: 设置页单选框快速切换
- **CMD 指令**: `/preset [办公/备考/陪伴/疏导]`

### 🔄 R2 功能保留

- ✅ 双界面切换 (GUI + CMD)
- ✅ 任务管理 (待办/目标/习惯)
- ✅ 数据管理 (备份/导出)
- ✅ AI 助手 (问答/情绪疏导/内容辅助)
- ✅ 复盘报告生成

### 📁 新增文件

- `zhangy_chat/memory_manager.py` - 内存配置管理模块
- `zhangy_chat/mood_manager.py` - 心情标签管理模块
- `zhangy_chat/preset_manager.py` - 场景预设管理模块
- `tests/test_r3.py` - R3 新增功能测试脚本

### 🔄 更新文件

- `zhangy_chat/assistant.py` - 适配心情/预设动态调整回应风格
- `zhangy_chat/cmd_interface.py` - 新增 /mem /mood /preset /status 指令
- `gui.py` - 新增心情面板、内存配置、预设选择界面
- `zhangy_chat/__init__.py` - 导出新增模块
- `requirements.txt` - 新增 psutil 依赖
- `README.md` - 完整更新 R3 文档

### 📊 代码统计

- 新增代码：~1500 行
- 新增模块：3 个核心模块
- 新增指令：4 条 CMD 指令
- 新增界面元素：心情面板、内存配置器、预设选择器

### 📋 系统要求

- Python 3.8+
- 8GB+ RAM (推荐 16GB+)
- Windows 10+ / macOS 12+ / Linux (Ubuntu 20.04+)

### 🚀 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# GUI 模式
python gui.py

# CMD 模式
python main.py -cmd
```

### ⚠️ 注意事项

- 首次运行会自动检测内存并推荐配置
- 心情和预设配置本地存储，下次启动自动加载
- 切换预设不影响原有任务/目标数据

### 📄 开源协议

MIT License

---

**Full Changelog**: https://github.com/350zhangy-ai/zhangy-chat/compare/v2.0.0...v3.0.0
