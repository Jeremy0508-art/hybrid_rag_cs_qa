# Project Showcase

## 项目一句话

面向计算机课程问答，构建 Hybrid Self-Reflective GraphRAG 系统，通过混合检索、概念图扩展、hard-negative 重排序、证据压缩和本地 Ollama LLM 生成，完成可复现的 RAG 检索与生成评测闭环。

## 核心结果

![Retrieval Metrics](figures/retrieval_metrics.svg)

![Generation Metrics](figures/generation_metrics.svg)

## 关键发现

- Naive RAG 在 100 条 QA 中 Recall@5 为 0.7500，说明普通检索会漏掉部分多跳和概念关联问题。
- Graph + Reflection RAG 将 Recall@5 提升到 0.9400，但 Context Precision 下降到 0.4140，说明图扩展带来噪声。
- Graph + Pruning RAG 将 Context Precision 提升到 0.6450，同时保持 0.9367 的 Recall@5。
- 生成评测中 Citation Accuracy 达到 0.6450，Citation Recall 达到 0.9367。
- 本地 Ollama 实验接入 `qwen-rag:3b`，跑通真实 LLM 端到端问答；样例分析显示 3B 模型比 0.5B 更适合展示自然语言回答，但自动指标仍会偏好更贴近原文的抽取式答案。

## 本地 LLM 实验

| Model | Faithfulness | Answer Coverage | Citation Accuracy | Citation Recall |
|---|---:|---:|---:|---:|
| `qwen-rag:0.5b` | 0.7251 | 0.3151 | 0.6666 | 1.0000 |
| `qwen-rag:3b` | 0.3378 | 0.2383 | 0.6666 | 1.0000 |

解释：0.5B 的词面重合指标更高，但容易拼接无关片段；3B 的回答更自然，引用格式经 prompt 收紧后更稳定。这个结果说明项目同时做了自动指标评测和人工误差分析。

## 可复现命令

```powershell
cs-rag train-reranker
cs-rag evaluate
cs-rag evaluate-generation

$env:CS_RAG_LLM_MODEL="qwen-rag:3b"
cs-rag evaluate-generation --generator ollama --limit 10 --out reports/generation_results_ollama_3b.json

cs-rag build-showcase
```
