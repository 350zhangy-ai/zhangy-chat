# Zhangy Chat - MiniMind 模型版本

## 简介

此版本集成了 **MiniMind** 超轻量级大语言模型（26M 参数），实现真正的本地 AI 推理，思考过程可见（CoT 推理链展示）。

## 文件说明

| 文件 | 说明 |
|------|------|
| `minimind_assistant.py` | MiniMind 模型助手核心 |
| `gui_minimind.py` | MiniMind GUI 界面 |

## 下载 MiniMind 模型

### 方式 1: HuggingFace（推荐）
```bash
# 下载 MiniMind2-small (26M)
git lfs install
git clone https://huggingface.co/jingyaogong/minimind2-small
```

### 方式 2: ModelScope（国内）
```bash
# 下载 MiniMind2-small
git clone https://www.modelscope.cn/gongjy/MiniMind2-PyTorch.git
```

### 方式 3: 手动下载
从以下地址下载模型权重：
- **HuggingFace**: https://huggingface.co/jingyaogong/minimind2-small
- **ModelScope**: https://www.modelscope.cn/models/gongjy/MiniMind2-PyTorch

下载后解压到项目目录，例如：`D:\zhangy ai\zhangy_chat\models\minimind2-small`

## 运行方式

### 1. 使用备用回复（无需下载模型）
```bash
python gui_minimind.py
```
此时使用预设的备用回复系统，思考过程为模拟展示。

### 2. 使用 MiniMind 模型推理
修改 `gui_minimind.py` 中的模型路径：
```python
self.assistant = MiniMindAssistant(model_path="models/minimind2-small")
```

然后运行：
```bash
python gui_minimind.py
```

## 思考过程展示

```
<think>
匹配关键词：你好
</think>

你好！有什么可以帮你的？
```

## 界面布局

- **左侧**: 思考过程显示区（黑底绿字，终端风格）
- **右侧**: 对话区（GitHub Dark 主题）
- **底部**: 思考过程开关（可勾选）

## MiniMind 模型规格

| 型号 | 参数量 | 推理占用 | 说明 |
|------|--------|----------|------|
| MiniMind2-small | 26M | 0.5GB | 最轻量，适合个人 GPU |
| MiniMind2 | 104M | 1.0GB | 性能更强 |
| MiniMind2-MoE | 145M | 1.0GB | MoE 架构 |

## 注意事项

1. **无模型时**: 使用备用回复系统，思考过程为模拟展示
2. **有模型时**: 使用 MiniMind 进行真实推理，思考过程为模型生成
3. **CPU 推理**: 26M 模型 CPU 推理约 1-3 秒/句
4. **GPU 加速**: 如有 GPU，可添加 `device_map="auto"` 加速

## 灵感来源

- **MiniMind 项目**: https://github.com/jingyaogong/minimind
- 2 小时即可从 0 训练 26M 参数的超小语言模型

---

**版本**: MiniMind 集成版  
**基于**: Zhangy Chat R3 + MiniMind 26M  
**发布时间**: 2026
