# Hybrid Self-Reflective RAG for CS Course QA

面向计算机课程问答的实验型 RAG 项目。项目不是简单聊天机器人，而是一个可复现实验系统：比较 Naive RAG、Hybrid RAG、Hybrid + Reranker、Graph + Reflection RAG 和 Graph + Pruning RAG 在课程问答任务上的检索、生成和引用表现。

## Highlights

- 构建 34 个课程知识点与 100 条标注 QA，覆盖操作系统、计算机网络、数据库、编译原理和 RAG 方法论。
- 实现 BM25 + TF-IDF dense retrieval + RRF 的混合检索。
- 实现基于课程概念共现的轻量 GraphRAG，用于多跳概念扩展。
- 使用 hard-negative 训练 Logistic Regression reranker。
- 设计 GraphRAG 证据压缩，缓解图扩展带来的上下文噪声。
- 使用 Recall@5、MRR、NDCG、Context Precision 评估检索质量。
- 使用 Faithfulness、Answer Coverage、Citation Accuracy、Citation Recall 评估生成质量。
- 接入本地 Ollama Qwen2.5 0.5B/3B，完成真实 LLM 端到端问答实验。

## Key Results

检索评测，100 条 QA：

| Method | Recall@5 | MRR | NDCG | Context Precision |
|---|---:|---:|---:|---:|
| naive | 0.7500 | 0.7633 | 0.7512 | 0.5905 |
| hybrid | 0.7500 | 0.7583 | 0.7495 | 0.5905 |
| hybrid_rerank | 0.7500 | 0.7700 | 0.7554 | 0.5905 |
| graph_reflect | 0.9400 | 0.9183 | 0.9193 | 0.4140 |
| graph_pruned | 0.9367 | 0.9183 | 0.9173 | 0.6450 |

主要结论：GraphRAG 显著提升召回，但会引入相邻概念噪声；Graph + Pruning 在几乎保持召回的同时，将 Context Precision 从 0.4140 提升到 0.6450。

本地 Ollama 小规模生成评测，前 10 条 QA：

| Model | Faithfulness | Answer Coverage | Citation Accuracy | Citation Recall |
|---|---:|---:|---:|---:|
| `qwen-rag:0.5b` | 0.7251 | 0.3151 | 0.6666 | 1.0000 |
| `qwen-rag:3b` | 0.3378 | 0.2383 | 0.6666 | 1.0000 |

解释：0.5B 更贴近原文拼接，自动词面指标更高；3B 回答更自然，适合展示真实 LLM 问答。项目同时保留自动指标和样例误差分析。

## Quick Start

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
```

运行单条问答：

```powershell
cs-rag ask "GraphRAG 为什么可能提高召回率但降低 Context Precision？"
```

## Ollama LLM

安装 Ollama 后，可使用本地 3B 模型：

```powershell
ollama pull modelscope.cn/Qwen/Qwen2.5-3B-Instruct-GGUF
ollama create qwen-rag:3b -f ollama\Modelfile.qwen-rag-3b

$env:CS_RAG_LLM_MODEL="qwen-rag:3b"
cs-rag ask "GraphRAG 为什么可能提高召回率但降低 Context Precision？" --generator ollama
cs-rag evaluate-generation --generator ollama --limit 10 --out reports/generation_results_ollama_3b.json
```

更多说明见 [OLLAMA.md](OLLAMA.md) 和 [reports/ollama_model_comparison.md](reports/ollama_model_comparison.md)。

## Optional Embedding Backend

默认 dense retriever 使用 TF-IDF，保证轻量可复现。可切换为 sentence-transformers / BGE：

```powershell
pip install -r requirements-embeddings.txt
$env:CS_RAG_DENSE_BACKEND="sentence-transformers"
$env:CS_RAG_EMBEDDING_MODEL="BAAI/bge-small-zh-v1.5"
cs-rag prepare
cs-rag train-reranker
cs-rag evaluate
```

如果模型下载或加载失败，系统会自动回退到 TF-IDF dense retriever。

## Project Structure

```text
data/raw/cs_courses.md          # 34 个课程知识点
data/qa/eval_qa.jsonl           # 100 条标注 QA
src/hybrid_rag_cs_qa/           # RAG、GraphRAG、reranker、generation 代码
tests/                          # 数据、指标、pipeline 测试
ollama/                         # Ollama Modelfile
reports/experiment_results.md   # 检索实验指标
reports/error_analysis.md       # 错误案例分析
reports/generation_results.md   # 抽取式生成评测
reports/generation_results_ollama_3b.md # 本地 3B LLM 生成评测
reports/ollama_model_comparison.md      # 0.5B/3B 对比分析
reports/final_showcase.md       # 最终展示页
reports/interview_cheatsheet.md # 面试速查
RESUME.md                       # 简历材料
RUNBOOK.md                      # 复现手册
```

## Report Materials

- 研究报告：[reports/research_report_template.md](reports/research_report_template.md)
- 最终展示：[reports/final_showcase.md](reports/final_showcase.md)
- 面试速查：[reports/interview_cheatsheet.md](reports/interview_cheatsheet.md)
- 简历素材：[RESUME.md](RESUME.md)

## Resume Bullet

独立完成面向计算机课程问答的 Hybrid Self-Reflective GraphRAG 系统，构建 34 个课程知识点与 100 条标注问答评测集；设计 BM25 + dense retrieval + RRF 融合检索、概念图谱扩展检索、hard-negative 重排序与证据压缩流程，将 Recall@5 从 0.7500 提升到 0.9367，并将 GraphRAG Context Precision 从 0.4140 提升到 0.6450；接入本地 Ollama Qwen2.5 3B 模型，完成真实 LLM 生成实验与引用质量评测。
