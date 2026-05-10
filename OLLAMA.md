# Ollama Local LLM Guide

本项目已经支持两种本地 Ollama 调用方式：

- `--generator ollama`：调用 Ollama 原生 `/api/generate`，推荐优先使用。
- `--generator openai-compatible`：调用 Ollama 的 `/v1/chat/completions` 兼容接口，适合 chat 模板完整的模型。

## 1. 安装 Ollama

Windows 可从官网下载：

https://ollama.com/download

也可以尝试：

```powershell
winget install --id Ollama.Ollama -e --accept-package-agreements --accept-source-agreements
```

本次会话中，`winget` 能找到 Ollama，但下载安装长时间超时，因此没有在当前环境完成安装。

## 2. 下载一个模型

推荐中文问答模型，例如：

```powershell
ollama pull qwen2.5:7b-instruct
```

如果机器显存/内存较小，可以先用更小模型验证流程：

```powershell
ollama pull qwen2.5:3b-instruct
```

如果你从 ModelScope 下载 GGUF 模型，也可以。当前已经验证可拉取：

```powershell
ollama pull modelscope.cn/Qwen/Qwen2.5-0.5B-Instruct-GGUF
```

这个 0.5B 模型很小，适合验证“RAG 检索 + 本地 LLM 生成”的完整链路，但生成质量不适合作为最终展示结论。正式写报告或面试展示时，优先换成 `qwen2.5:3b-instruct`、`qwen2.5:7b-instruct` 或同级别中文指令模型。

ModelScope 这个 GGUF 模型默认只有 `completion` 能力，因此项目里提供了一个 Ollama Modelfile，给它补上问答模板：

```powershell
ollama create qwen-rag:0.5b -f ollama\Modelfile.qwen-rag
```

## 3. 检查服务

```powershell
ollama list
cs-rag check-llm
```

如果 Ollama 正常运行，`cs-rag check-llm` 会列出本地模型，并提示需要设置的环境变量。

## 4. 使用 Ollama 原生接口生成答案

推荐先用这个方式，因为它直接走 Ollama `/api/generate`：

```powershell
$env:CS_RAG_LLM_MODEL="qwen-rag:0.5b"

cs-rag ask "GraphRAG 为什么可能提高召回率但降低 Context Precision？" --generator ollama
cs-rag evaluate-generation --generator ollama --limit 1 --out reports/generation_results_ollama_sample.json
```

如果你换成更强模型，只需要改模型名：

```powershell
$env:CS_RAG_LLM_MODEL="qwen2.5:7b-instruct"
cs-rag ask "RAG 中重排序器为什么常用 hard negative 训练？" --generator ollama
```

## 5. 使用 OpenAI-compatible 接口

```powershell
$env:CS_RAG_LLM_BASE_URL="http://localhost:11434/v1/chat/completions"
$env:CS_RAG_LLM_MODEL="qwen2.5:7b-instruct"

cs-rag ask "GraphRAG 为什么可能提高召回率但降低 Context Precision？" --generator openai-compatible
cs-rag evaluate-generation --generator openai-compatible
```

如果 endpoint 未配置或调用失败，系统会自动回退到抽取式生成。
