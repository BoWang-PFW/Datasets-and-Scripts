# 商业 API 版本使用指南

## 📦 安装依赖

```bash
pip install -r requirements_api.txt
```

或单独安装：
```bash
# ChatGPT
pip install openai

# Claude
pip install anthropic
```

---

## 🔑 设置 API Key

### 方法1: 环境变量（推荐）

```bash
# ChatGPT
export OPENAI_API_KEY="sk-..."

# Claude
export ANTHROPIC_API_KEY="sk-ant-..."
```

### 方法2: 命令行参数

```bash
python run_scan_api.py /path/to/code --api openai --key "sk-..."
```

---

## 🚀 使用方法

### ChatGPT (OpenAI)

```bash
# 基础用法（使用 gpt-4o-mini，快速便宜）
python run_scan_api.py ./dataset --api openai

# 测试模式（前5个文件）
python run_scan_api.py ./dataset --api openai -t 5

# 使用 GPT-4（更准确但更贵）
python run_scan_api.py ./dataset --api openai --model gpt-4o

# 指定输出文件
python run_scan_api.py ./dataset --api openai -o my_results.json
```

### Claude (Anthropic)

```bash
# 基础用法（使用 Haiku，快速便宜）
python run_scan_api.py ./dataset --api claude

# 测试模式
python run_scan_api.py ./dataset --api claude -t 5

# 使用 Sonnet（更准确但更贵）
python run_scan_api.py ./dataset --api claude --model claude-3-5-sonnet-20241022

# 扫描 .cpp 文件
python run_scan_api.py ./dataset --api claude -p "*.cpp"
```

---

## 💰 成本估算

### ChatGPT (OpenAI)

| 模型 | 输入 | 输出 | 每文件成本* | 100文件成本 |
|------|------|------|------------|-------------|
| **gpt-4o-mini** | $0.15/1M tokens | $0.60/1M tokens | ~$0.002 | ~$0.20 |
| gpt-4o | $2.50/1M tokens | $10.00/1M tokens | ~$0.03 | ~$3.00 |

### Claude (Anthropic)

| 模型 | 输入 | 输出 | 每文件成本* | 100文件成本 |
|------|------|------|------------|-------------|
| **claude-3-5-haiku** | $0.80/1M tokens | $4.00/1M tokens | ~$0.01 | ~$1.00 |
| claude-3-5-sonnet | $3.00/1M tokens | $15.00/1M tokens | ~$0.04 | ~$4.00 |

\*假设每个文件约1000行代码

**推荐：**
- 日常测试：gpt-4o-mini 或 claude-3-5-haiku
- 正式研究：gpt-4o 或 claude-3-5-sonnet

---

## 🎯 推荐配置

**快速且便宜（研究初期）：**
```bash
# OpenAI
python run_scan_api.py ./dataset --api openai --model gpt-4o-mini -t 50

# Claude
python run_scan_api.py ./dataset --api claude --model claude-3-5-haiku-20241022 -t 50
```

**高准确度（论文最终数据）：**
```bash
# OpenAI
python run_scan_api.py ./dataset --api openai --model gpt-4o

# Claude  
python run_scan_api.py ./dataset --api claude --model claude-3-5-sonnet-20241022
```

---

## 🔧 配置优化

修改 `config.py`：

```python
# API 版本建议设置
DELAY_BETWEEN_FILES = 0.2  # API 更快，可以减少延迟

# 对于大规模扫描
DELAY_BETWEEN_FILES = 0.5  # 避免触发速率限制
```

---

## ⚡ 速度对比

| 方案 | 单文件耗时 | 100文件耗时 | 成本 |
|------|-----------|------------|------|
| Ollama (本地) | 10-30秒 | 20-50分钟 | 免费 |
| **gpt-4o-mini** | 2-5秒 | 5-10分钟 | ~$0.20 |
| **claude-haiku** | 2-5秒 | 5-10分钟 | ~$1.00 |
| gpt-4o | 3-8秒 | 8-15分钟 | ~$3.00 |
| claude-sonnet | 3-8秒 | 8-15分钟 | ~$4.00 |

---

## 📊 分析结果

使用原有的分析工具：

```bash
python analyze_results.py results/scan_results_openai_xxx.json
python analyze_results.py results/scan_results_claude_xxx.json
```

---

## 🆚 与 Ollama 版本对比

**优势：**
- ✅ 快 3-10 倍
- ✅ 质量更稳定
- ✅ 不占用本地资源
- ✅ 可以用更强大的模型

**劣势：**
- ❌ 需要付费
- ❌ 需要网络连接
- ❌ 有 API 速率限制

**建议：**
- 初期开发/测试：Ollama（免费）
- 大规模实验：商业 API（快速）
- 论文对比实验：两者都用（全面）

---

## 🔒 安全提示

1. **不要把 API key 写入代码**
2. **不要提交 API key 到 Git**
3. **使用环境变量或配置文件**

```bash
# .gitignore 添加
.env
api_keys.txt
```

---

## 🐛 常见问题

### 1. API Key 错误
```
Error: Set OPENAI_API_KEY environment variable
```
**解决：** 设置环境变量或使用 `--key` 参数

### 2. 速率限制
```
Error: Rate limit exceeded
```
**解决：** 增加 `DELAY_BETWEEN_FILES` 到 1 秒

### 3. Token 超限
```
Error: maximum context length exceeded
```
**解决：** 代码已自动截断到 8000 字符，检查是否有超大文件

---

## 💡 提示

1. **先用测试模式** `-t 5` 验证效果
2. **监控成本**：100 个文件约 $0.2-$4
3. **对比实验**：可以同时用 ChatGPT 和 Claude 扫描同一数据集
4. **保存结果**：商业 API 的结果会自动加上 `_openai` 或 `_claude` 后缀

---

## 📞 获取 API Key

- **OpenAI**: https://platform.openai.com/api-keys
- **Anthropic**: https://console.anthropic.com/settings/keys

需要绑定信用卡，但都有免费额度。
