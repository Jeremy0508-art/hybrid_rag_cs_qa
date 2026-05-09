# Runbook

这份运行手册用于快速复现实验、更新报告和准备展示材料。

## 1. 环境安装

```powershell
pip install -r requirements.txt
pip install -e .
```

可选 embedding 后端：

```powershell
pip install -r requirements-embeddings.txt
$env:CS_RAG_DENSE_BACKEND="sentence-transformers"
$env:CS_RAG_EMBEDDING_MODEL="BAAI/bge-small-zh-v1.5"
```

默认不设置环境变量时，系统使用 TF-IDF dense retriever，保证轻量可复现。

可选真实 LLM 生成：

```powershell
$env:CS_RAG_LLM_BASE_URL="http://localhost:11434/v1/chat/completions"
$env:CS_RAG_LLM_MODEL="qwen2.5:7b-instruct"
```

## 2. 标准复现实验

```powershell
cs-rag prepare
cs-rag train-reranker
cs-rag evaluate
cs-rag evaluate-generation
cs-rag build-showcase
```

如果已配置 LLM endpoint，可运行：

```powershell
cs-rag ask "GraphRAG 为什么可能提高召回率但降低 Context Precision？" --generator openai-compatible
cs-rag evaluate-generation --generator openai-compatible
```

## 3. 输出文件

| 文件 | 作用 |
|---|---|
| `reports/experiment_results.md` | 检索实验指标 |
| `reports/error_analysis.md` | 错误案例分析 |
| `reports/generation_results.md` | 生成质量评测 |
| `reports/final_showcase.md` | 最终展示页 |
| `reports/interview_cheatsheet.md` | 面试讲稿 |
| `reports/figures/*.svg` | 可视化图表 |

## 4. 推荐展示顺序

1. 先讲问题：普通 RAG 在课程问答中会漏召回精确术语和多跳概念。
2. 再讲方法：Hybrid retrieval、GraphRAG、hard-negative reranker、证据压缩。
3. 展示结果：GraphRAG 提升 Recall，Graph + Pruning 提升 Context Precision。
4. 展示错误分析：说明你知道方法的局限，不只是跑指标。
5. 最后讲后续：BGE/E5 embedding、CrossEncoder reranker、真实 LLM 生成。

## 5. 当前关键结果

| Method | Recall@5 | MRR | NDCG | Context Precision |
|---|---:|---:|---:|---:|
| naive | 0.7500 | 0.7633 | 0.7512 | 0.5905 |
| graph_reflect | 0.9400 | 0.9183 | 0.9193 | 0.4140 |
| graph_pruned | 0.9367 | 0.9183 | 0.9173 | 0.6450 |

生成评测：

| Metric | Score |
|---|---:|
| Faithfulness | 0.7558 |
| Citation Accuracy | 0.6450 |
| Citation Recall | 0.9367 |
