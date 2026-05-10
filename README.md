# Hybrid Self-Reflective RAG for CS Course QA

面向计算机专业课程问答的实验型 RAG 项目。项目目标不是做一个普通聊天机器人，而是构建可复现实验：比较 Naive RAG、Hybrid RAG、Hybrid + Reranker、Graph + Reflection RAG 和 Graph + Pruning RAG 在课程问答任务上的检索与生成表现。

## 研究问题

在计算机课程问答场景中，BM25 与向量检索融合、课程概念图谱扩展、候选集内 hard-negative 重排序训练、证据压缩，是否能够提升证据召回率、排序质量和引用准确率？

## 功能

- Markdown 课程资料切分与索引
- BM25 稀疏检索
- TF-IDF 向量检索 baseline
- 可选 sentence-transformers / BGE embedding 后端
- RRF 排序融合
- 基于课程概念共现的轻量 GraphRAG
- 基于 hard negative 的 Logistic Regression 重排序器
- GraphRAG 证据压缩，降低图扩展噪声
- Recall@k、MRR、NDCG、Context Precision 评测
- Faithfulness、Answer Coverage、Citation Accuracy、Citation Recall 生成评测
- 可选 OpenAI-compatible / Ollama 真实 LLM 生成后端
- 自动生成实验结果与错误案例分析

## 快速开始

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install -e .
cs-rag prepare
cs-rag train-reranker
cs-rag evaluate
cs-rag evaluate-generation
cs-rag build-showcase
cs-rag check-llm
```

更完整的复现实验说明见 [RUNBOOK.md](RUNBOOK.md)。

## 使用真实 Embedding 检索

默认 dense retriever 使用 TF-IDF，优点是轻量、无需下载模型。如果想升级为 sentence-transformers / BGE embedding：

```powershell
pip install -r requirements-embeddings.txt
$env:CS_RAG_DENSE_BACKEND="sentence-transformers"
$env:CS_RAG_EMBEDDING_MODEL="BAAI/bge-small-zh-v1.5"
cs-rag prepare
cs-rag train-reranker
cs-rag evaluate
```

如果模型下载或加载失败，系统会回退到 TF-IDF dense retriever。

## 使用真实 LLM 生成

默认生成器是 `extractive`，不需要 API。若你有本地 Ollama 或任意 OpenAI-compatible `/v1/chat/completions` 服务，可以这样切换：

推荐优先使用 Ollama 原生接口：

```powershell
$env:CS_RAG_LLM_MODEL="qwen-rag:0.5b"
cs-rag ask "GraphRAG 为什么可能提高召回率但降低 Context Precision？" --generator ollama
cs-rag evaluate-generation --generator ollama --limit 1 --out reports/generation_results_ollama_sample.json
```

已验证的 3B 本地模型命令：

```powershell
$env:CS_RAG_LLM_MODEL="qwen-rag:3b"
cs-rag evaluate-generation --generator ollama --limit 10 --out reports/generation_results_ollama_3b.json
```

如果使用 Ollama 的 OpenAI-compatible 接口：

```powershell
$env:CS_RAG_LLM_BASE_URL="http://localhost:11434/v1/chat/completions"
$env:CS_RAG_LLM_MODEL="qwen2.5:7b-instruct"
cs-rag ask "GraphRAG 为什么可能提高召回率但降低 Context Precision？" --generator openai-compatible
cs-rag evaluate-generation --generator openai-compatible
```

如果未配置 endpoint 或调用失败，系统会自动回退到抽取式生成。0.5B 小模型适合验证流程，正式展示建议使用 3B/7B 级别中文指令模型。

Ollama 安装、本地模型运行与 0.5B/3B 对比说明见 [OLLAMA.md](OLLAMA.md) 和 [reports/ollama_model_comparison.md](reports/ollama_model_comparison.md)。

## 目录结构

```text
data/raw/cs_courses.md        # 课程语料，当前包含 34 个知识点
data/qa/eval_qa.jsonl         # 评测集，当前包含 100 条标注问答
src/hybrid_rag_cs_qa/         # 实验代码
artifacts/                    # 训练后的 reranker
reports/experiment_results.md # 检索指标表格
reports/error_analysis.md     # 错误案例分析
reports/generation_results.md # 生成答案质量评测
reports/final_showcase.md     # 最终展示页
reports/interview_cheatsheet.md # 面试讲稿
reports/figures/              # 自动生成的 SVG 图表
reports/embedding_experiment_notes.md # embedding 后端实验记录
RUNBOOK.md                     # 复现实验与展示流程
OLLAMA.md                      # 本地 Ollama 运行说明
```

## 当前实验结果

运行 `cs-rag evaluate` 后会自动更新 `reports/experiment_results.md`。当前 100 条 QA 上：

- `hybrid_rerank` 相比 `hybrid` 提升了 MRR，说明候选集内 hard-negative 训练开始发挥作用。
- `graph_reflect` 显著提升 Recall@5、MRR 和 NDCG，但 Context Precision 更低，说明图扩展带来噪声。
- `graph_pruned` 在几乎保持召回的同时，将 Context Precision 从 `0.4140` 提升到 `0.6450`，说明证据压缩能有效降低 GraphRAG 噪声。
- `evaluate-generation` 会生成 Faithfulness、Answer Coverage、Citation Accuracy 和 Citation Recall，用于评估答案是否被上下文支持、是否覆盖标准答案要点，以及引用是否命中标注证据。
- `build-showcase` 会生成最终展示页、SVG 指标图和面试讲稿。

## 可写进报告的结论

GraphRAG 通过课程概念图扩展候选证据，在多跳问题和概念关联问题上能补足普通向量检索的漏召回；但图扩展会引入相邻概念文本，导致上下文精度下降。加入证据压缩后，系统几乎保持 GraphRAG 的召回能力，同时明显提升 Context Precision 和 Citation Accuracy。

## 简历描述

独立完成面向计算机课程问答的 Hybrid Self-Reflective GraphRAG 系统，构建 34 个课程知识点与 100 条标注问答评测集；设计 BM25 + dense retrieval + RRF 融合检索、概念图谱扩展检索、hard-negative 监督式重排序与证据压缩流程，并使用 Recall@k、MRR、NDCG、Context Precision、Faithfulness、Citation Recall 等指标完成系统性实验评估。
