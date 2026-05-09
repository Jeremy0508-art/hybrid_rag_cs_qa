# Project Showcase

## 项目一句话

面向计算机课程问答，构建 Hybrid Self-Reflective GraphRAG 系统，通过混合检索、图扩展、hard-negative 重排序和证据压缩提升证据召回与引用准确率。

## 核心结果

![Retrieval Metrics](figures/retrieval_metrics.svg)

![Generation Metrics](figures/generation_metrics.svg)

## 关键发现

- Naive RAG 在 100 条 QA 上 Recall@5 为 0.7500，说明普通检索会漏掉部分多跳和概念关联问题。
- Graph + Reflection RAG 将 Recall@5 提升到 0.9400，但 Context Precision 下降到 0.4140，说明图扩展带来噪声。
- Graph + Pruning RAG 将 Context Precision 提升到 0.6450，同时保持 0.9367 的 Recall@5。
- 生成评测中 Citation Accuracy 达到 0.6450，Citation Recall 达到 0.9367。

## 可复现命令

```powershell
cs-rag train-reranker
cs-rag evaluate
cs-rag evaluate-generation
cs-rag build-showcase
```
