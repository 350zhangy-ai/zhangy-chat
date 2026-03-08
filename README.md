# zhangy-chat R3

<div align="center">
  <h3>高效、专业的本地 AI 助手 - MiniMind 集成版</h3>
  <p>MiniMind 模型 | 思考式响应 | 情绪共情 | 本地运行</p>
</div>

## 简介

zhangy-chat R3 是一个集成 **MiniMind 模型** 的本地 AI 助手。支持两种模式：
- **模型模式**：有 MiniMind 模型时，使用模型推理
- **知识库模式**：无模型时，使用超全知识库回复

所有回应均经过 AI 主动思考（需求拆解、逻辑推理、情绪共情），而非机械匹配预设答案。

## 核心特性

### 🧠 MiniMind 模型集成

**支持模型**：
- MiniMind-768
- MiniMind-512
- MiniMind-GRPO

**模型放置**：
将模型文件放入 `models/zhangy-chat/` 目录，支持以下文件名：
- `full_sft_768.pth`
- `full_sft_512.pth`
- `grpo_768.pth`
- `model.pth`

**无模型时**：
自动切换到知识库模式，使用超全知识库回复（覆盖饮食、编程、工作、学习、情感等 12 个领域）

### 🧠 R3 思考式响应

**像人一样思考**：
- **需求拆解**：分析用户问题的核心诉求和潜在需求
- **情绪识别**：识别用户情绪状态，先共情再解答
- **上下文关联**：基于历史对话理解用户意图
- **个性化适配**：根据用户习惯调整回应风格

**思考过程可视化**（可选）：
```
[思考] 识别需求：emotional_support -> 情绪状态：tired (强度 2) -> 策略：先共情再解答

zhangy-chat：辛苦了，忙到现在确实该歇歇了。身体最重要，不用有负罪感。

---

## 休息建议
...
```

### 📋 任务管理
- **待办事项**：添加、删除、标记任务，支持优先级
- **目标规划**：设定目标，拆解里程碑，进度追踪
- **习惯打卡**：每日/每周习惯，连续打卡统计
- **复盘报告**：生成周期性复盘，查看成长轨迹

### 💾 数据管理
- **本地存储**：所有数据存在本地，不上传云端
- **备份恢复**：一键备份，随时恢复
- **导出功能**：支持导出 TXT、Excel 格式

## 快速开始

### 环境要求

- Python 3.8+
- 8GB+ RAM
- Windows 10+ / macOS 12+ / Linux
- PyTorch（使用模型时需要）

### 安装

```bash
cd zhangy_chat
pip install -r requirements.txt
```

### 运行

```bash
# GUI 图形界面模式（推荐）
python gui.py

# CMD 命令行模式
python main.py -cmd
```

### 添加 MiniMind 模型（可选）

1. 下载 MiniMind 模型文件
2. 创建目录 `models/zhangy-chat/`
3. 将模型文件放入目录，命名为 `full_sft_768.pth` 或其他支持的文件名
4. 重启 zhangy-chat，自动加载模型

## 使用指南

### CMD 指令

| 指令 | 说明 | 示例 |
|------|------|------|
| `/add <标题>` | 添加任务 | `/add 学习 Python` |
| `/del <ID>` | 删除任务 | `/del abc12345` |
| `/list [状态]` | 查看任务 | `/list pending` |
| `/mark <ID> <状态>` | 标记任务 | `/mark abc12345 completed` |
| `/goal add <标题>` | 添加目标 | `/goal add 考研上岸` |
| `/goal list` | 查看目标 | `/goal list` |
| `/habit add <名称>` | 添加习惯 | `/habit add 早起` |
| `/habit check <ID>` | 习惯打卡 | `/habit check abc12345` |
| `/backup` | 备份数据 | `/backup` |
| `/export <格式>` | 导出数据 | `/export excel` |
| `/mem [8/16/32/64]` | 设置内存 | `/mem 16` |
| `/mood [心情]` | 设置心情 | `/mood 高效` |
| `/preset [预设]` | 切换预设 | `/preset 办公` |
| `/status` | 查看当前状态 | `/status` |
| `/think` | 思考模式 | `/think on` |
| `/gui` | 切换图形界面 | `/gui` |
| `/exit` | 退出程序 | `/exit` |

### 思考模式指令

| 指令 | 说明 | 示例 |
|------|------|------|
| `/think on` | 开启思考模式 | `/think on` |
| `/think off` | 关闭思考模式 | `/think off` |
| `/think light` | 轻量思考 | `/think light` |
| `/think mid` | 中度思考（默认） | `/think mid` |
| `/think heavy` | 深度思考 | `/think heavy` |
| `/think show` | 显示思考过程 | `/think show` |
| `/think hide` | 隐藏思考过程 | `/think hide` |

### 心情标签

| 心情 | 说明 | 回应风格 |
|------|------|----------|
| 焦虑/低落 | 情绪低落时 | 共情优先，语气温柔 |
| 高效/专注 | 工作需要时 | 简洁干练，直奔主题 |
| 轻松/愉悦 | 休闲聊天时 | 亲切活泼，轻松互动 |
| 平静/温和 | 日常状态 | 温和平稳，给予安全感 |
| 疲惫/休息 | 累的时候 | 关怀为主，强调休息 |

### 场景预设

| 预设 | 说明 | 适用场景 |
|------|------|----------|
| 高效办公 | 任务拆解、时间管理 | 工作、职场 |
| 备考冲刺 | 学习计划、知识点梳理 | 考试、考研 |
| 休闲陪伴 | 轻松聊天、生活建议 | 日常、闲聊 |
| 情绪疏导 | 共情倾听、压力缓解 | 情绪低落时 |

## 知识库覆盖

### 12 大领域

| 领域 | 关键词 |
|------|--------|
| 饮食 | 饿/吃饭/吃啥/外卖/食堂/减肥餐 |
| 编程 | Python/Java/JavaScript/写程序/debug |
| 工作 | 上班/辞职/跳槽/面试/加班/涨薪 |
| 学习 | 考试/考研/考证/复习/备考 |
| 情感 | 喜欢/暗恋/表白/恋爱/分手/相亲 |
| 健康 | 运动/减肥/健身/生病/失眠/熬夜 |
| 购物 | 淘宝/京东/手机/电脑/数码推荐 |
| 旅行 | 旅游/景点/酒店/机票/攻略 |
| 情绪 | 累/压力/焦虑/担心/崩溃/烦 |
| 无聊 | 无聊/没事干/剧荒/游戏 |
| 金钱 | 存款/理财/基金/股票/借钱 |
| 人际 | 朋友/社交/孤独/矛盾/吵架 |

## 项目结构

```
zhangy_chat/
├── zhangy_chat/
│   ├── __init__.py         # 模块导出
│   ├── main.py             # 核心类
│   ├── task_manager.py     # 任务管理
│   ├── data_manager.py     # 数据管理
│   ├── assistant.py        # AI 助手（MiniMind 集成）
│   ├── cmd_interface.py    # CMD 界面
│   ├── memory_manager.py   # 内存管理
│   ├── mood_manager.py     # 心情管理
│   ├── preset_manager.py   # 预设管理
│   └── thinking_engine.py  # 思考决策引擎
├── models/
│   └── zhangy-chat/        # 放置 MiniMind 模型
│       ├── full_sft_768.pth
│       └── ...
├── gui.py                  # GUI 界面
├── main.py                 # 主程序入口
├── config.yaml             # 配置文件
├── requirements.txt        # 依赖
└── README.md               # 说明文档
```

## 配置说明

### 模型配置

| 参数 | 说明 | 默认值 |
|------|------|--------|
| model_path | 模型文件路径 | models/zhangy-chat/ |
| model_file | 模型文件名 | full_sft_768.pth |

### 思考模式配置

| 参数 | 说明 | 默认值 |
|------|------|--------|
| thinking_mode | 是否开启思考 | True |
| thinking_depth | 思考深度 (light/mid/heavy) | mid |
| show_thinking_process | 显示思考过程 | False |

### 内存配置

| 内存 | 缓存 | 并发 | 数据加载 |
|------|------|------|----------|
| 8GiB | 64MB | 2 | 分块加载 |
| 16GiB | 256MB | 4 | 分块加载 |
| 32GiB | 512MB | 8 | 混合加载 |
| 64GiB | 1024MB | 16 | 全量加载 |

## 测试

```bash
# 基础功能测试
python -c "from zhangy_chat import Assistant; a = Assistant(); print(a.chat('你好'))"

# 检查模型加载
python -c "from zhangy_chat import Assistant; a = Assistant(); print('Model:', a.model is not None)"
```

## 版本历史

### v3.0.0 (R3) - MiniMind 集成版
- ✨ 集成 MiniMind 模型支持
- ✨ 新增 thinking_engine.py 思考决策引擎
- ✨ 需求拆解：分析用户核心诉求和潜在需求
- ✨ 情绪识别：识别情绪状态，先共情再解答
- ✨ 上下文关联：基于历史对话理解意图
- ✨ 个性化适配：根据用户习惯调整回应
- ✨ 思考过程可视化（可选开关）
- ✨ CMD 思考指令：/think on/off/light/mid/heavy/show/hide
- ✨ 超全知识库：覆盖 12 大生活领域
- ✨ 8/16/32/64GiB 内存配置
- ✨ 5 种心情标签选择
- ✨ 4 类场景预设切换

## 灵感来源

- **MiniMind**: https://github.com/jingyaogong/minimind
- 思考链（CoT）展示方式参考 MiniMind 的推理过程可视化

## 开源协议

MIT License

---

<div align="center">
  <sub>使用 ❤️ 制作 | zhangy-chat R3 MiniMind 集成版</sub>
</div>
