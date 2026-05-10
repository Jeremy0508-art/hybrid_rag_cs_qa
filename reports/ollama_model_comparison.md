# Ollama Local Model Comparison

本记录用于说明本地 Ollama 模型接入后的实际生成现象。评测设置为 `graph_pruned` 检索方法、`top_k=3`、前 10 条 QA 样本，生成器为 `--generator ollama`。

## Models

| Model | Source | Size | Purpose |
|---|---|---:|---|
| `qwen-rag:0.5b` | `modelscope.cn/Qwen/Qwen2.5-0.5B-Instruct-GGUF` | 491 MB | 快速验证本地 LLM 链路 |
| `qwen-rag:3b` | `modelscope.cn/Qwen/Qwen2.5-3B-Instruct-GGUF` | 2.1 GB | 本地 LLM 展示与小规模实验 |

两个 ModelScope GGUF 模型在 Ollama 中默认只有 `completion` 能力，因此分别通过 `ollama/Modelfile.qwen-rag` 和 `ollama/Modelfile.qwen-rag-3b` 补充 Qwen chat 模板。

## Metrics

| Model | Faithfulness | Answer Coverage | Citation Accuracy | Citation Recall |
|---|---:|---:|---:|---:|
| `qwen-rag:0.5b` | 0.7251 | 0.3151 | 0.6666 | 1.0000 |
| `qwen-rag:3b` | 0.3378 | 0.2383 | 0.6666 | 1.0000 |

## Interpretation

自动指标并不完全等价于人工可读质量。0.5B 模型在词面重合指标上更高，但样例中经常把多个检索片段直接拼接在一起，容易混入与问题无关的信息。3B 模型的答案更像真实问答输出，能更自然地概括证据，并且在收紧 prompt 后可以原样引用证据 ID。

这个结果说明，本项目不仅完成了本地 LLM 接入，也观察到了 RAG 生成评测中的一个典型问题：基于词面重合的自动指标会偏好“贴近原文的抽取式答案”，但不一定能充分反映生成答案的可读性、聚焦程度和引用格式质量。因此最终报告中应同时展示自动指标和样例分析。

## Reproduction

```powershell
ollama pull modelscope.cn/Qwen/Qwen2.5-3B-Instruct-GGUF
ollama create qwen-rag:3b -f ollama\Modelfile.qwen-rag-3b

$env:CS_RAG_LLM_MODEL="qwen-rag:3b"
cs-rag ask "GraphRAG 为什么可能提高召回率但降低 Context Precision？" --generator ollama
cs-rag evaluate-generation --generator ollama --limit 10 --out reports/generation_results_ollama_3b.json
```
