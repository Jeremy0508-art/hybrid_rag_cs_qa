# Ollama Local LLM Guide

本项目已经支持 OpenAI-compatible LLM 生成后端。Ollama 安装并启动后，可以直接用于 `cs-rag ask` 和 `cs-rag evaluate-generation`。

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

## 3. 检查服务

```powershell
ollama list
cs-rag check-llm
```

如果 Ollama 正常运行，`cs-rag check-llm` 会列出本地模型，并提示需要设置的环境变量。

## 4. 使用 Ollama 生成答案

```powershell
$env:CS_RAG_LLM_BASE_URL="http://localhost:11434/v1/chat/completions"
$env:CS_RAG_LLM_MODEL="qwen2.5:7b-instruct"

cs-rag ask "GraphRAG 为什么可能提高召回率但降低 Context Precision？" --generator openai-compatible
cs-rag evaluate-generation --generator openai-compatible
```

如果 endpoint 未配置或调用失败，系统会自动回退到抽取式生成。
