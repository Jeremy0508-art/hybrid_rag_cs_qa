# Hybrid GraphRAG + RAPTOR for CS Course QA

面向计算机课程问答的可复现 RAG 实验系统。项目从一个基础 RAG 小实验升级为包含扩展数据集、混合检索、GraphRAG、RAPTOR summary tree、证据压缩、生成评估和分组分析的完整项目。

## Highlights

- 构建 150 个课程文档和 750 条标注 QA，覆盖 citation-grounded、title-explicit、paraphrase 和 multi-hop paraphrase 问题。
- 实现 BM25 + dense retrieval + RRF 的混合检索。
- 实现课程概念图扩展，用于 GraphRAG 和多跳候选补充。
- 实现 RAPTOR tree：chunk 聚类、summary node 生成、递归树构建、collapsed 和 top-down 检索。
- 实现 Hybrid RAPTOR，将普通检索、GraphRAG 和 RAPTOR 候选融合。
- 实现面向生成的 `graph_raptor_pruned`，用证据压缩降低上下文噪声。
- 支持自适应生成 top-k，多跳问题自动扩大证据预算。
- 输出整体指标和按 topic、difficulty、type、answer_style、multi_hop 的分组评估。

## Key Results

检索评估，750 条 QA：

| Method | Recall@5 | MRR | NDCG | Context Precision |
|---|---:|---:|---:|---:|
| naive | 0.9667 | 0.9817 | 0.9638 | 0.2667 |
| hybrid | 0.9713 | 0.9756 | 0.9635 | 0.2685 |
| graph_reflect | 0.9773 | 0.9554 | 0.9524 | 0.2709 |
| raptor | 0.9747 | 0.9763 | 0.9667 | 0.2699 |
| raptor_topdown | 0.9747 | 0.9757 | 0.9652 | 0.2699 |
| hybrid_raptor | 0.9813 | 0.9822 | 0.9723 | 0.2725 |
| graph_raptor_pruned | 0.9667 | 0.9833 | 0.9663 | 0.3864 |

生成评估，默认 `graph_raptor_pruned` + adaptive top-k：

| Faithfulness | Answer Coverage | Citation Accuracy | Citation Recall |
|---:|---:|---:|---:|
| 0.9909 | 0.9814 | 0.4065 | 0.9687 |

主要结论：`hybrid_raptor` 是整体召回和排序最强的检索方法；`graph_raptor_pruned` 更适合作为生成入口，因为它用少量召回换取更干净的最终证据上下文。

## Quick Start

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install -e .

cs-rag build-expanded-dataset
cs-rag prepare
cs-rag train-reranker
cs-rag build-raptor-tree
cs-rag evaluate
cs-rag evaluate-generation --method graph_raptor_pruned --top-k 3 --adaptive-top-k --multi-hop-top-k 4
cs-rag build-showcase
pytest -q
```

运行单条问答：

```powershell
cs-rag ask "Why can GraphRAG improve recall but reduce context precision?"
```

## Optional Embedding Backend

默认 dense retriever 使用轻量、可复现的 TF-IDF backend。可以切换到 sentence-transformers / BGE：

```powershell
pip install -r requirements-embeddings.txt
$env:CS_RAG_DENSE_BACKEND="sentence-transformers"
$env:CS_RAG_EMBEDDING_MODEL="BAAI/bge-small-zh-v1.5"
cs-rag prepare
cs-rag evaluate
```

如果模型下载或加载失败，系统会自动回退到 TF-IDF dense retriever。

## Local Ollama LLM

安装 Ollama 后，可使用本地模型运行真实 LLM 问答：

```powershell
ollama pull modelscope.cn/Qwen/Qwen2.5-3B-Instruct-GGUF
ollama create qwen-rag:3b -f ollama\Modelfile.qwen-rag-3b

$env:CS_RAG_LLM_MODEL="qwen-rag:3b"
cs-rag ask "Why can GraphRAG improve recall but reduce context precision?" --generator ollama
```

更多说明见 [OLLAMA.md](OLLAMA.md) 和 [reports/ollama_model_comparison.md](reports/ollama_model_comparison.md)。

## Project Structure

```text
data/raw/cs_courses_expanded.md       # 150 个课程文档
data/qa/eval_qa_expanded.jsonl        # 750 条标注 QA
src/hybrid_rag_cs_qa/                 # RAG、GraphRAG、RAPTOR、evaluation、generation
tests/                                # 数据、检索、RAPTOR、生成相关测试
artifacts/                            # 构建出的索引、reranker、RAPTOR tree
reports/experiment_results.md         # 检索评估与分组分析
reports/generation_results.md         # 生成评估与分组分析
reports/error_analysis.md             # 错误案例分析
reports/final_showcase.md             # 最终展示页
reports/interview_cheatsheet.md       # 面试速查
RESUME.md                             # 简历材料
RUNBOOK.md                            # 复现手册
```

## Report Materials

- 研究报告模板：[reports/research_report_template.md](reports/research_report_template.md)
- 最终展示：[reports/final_showcase.md](reports/final_showcase.md)
- 面试速查：[reports/interview_cheatsheet.md](reports/interview_cheatsheet.md)
- 交付文件索引：[reports/artifact_index.md](reports/artifact_index.md)
- 提交前检查：[reports/submission_checklist.md](reports/submission_checklist.md)
- 简历素材：[RESUME.md](RESUME.md)

额外生成的对比报告：

- [reports/generation_results_graph_raptor_pruned.md](reports/generation_results_graph_raptor_pruned.md)
- [reports/generation_results_graph_raptor_pruned_adaptive.md](reports/generation_results_graph_raptor_pruned_adaptive.md)
- [reports/generation_results_hybrid_raptor.md](reports/generation_results_hybrid_raptor.md)
- [reports/generation_results_hybrid_raptor_adaptive.md](reports/generation_results_hybrid_raptor_adaptive.md)

## Resume Bullet

独立构建面向计算机课程问答的 Hybrid GraphRAG + RAPTOR 系统，将数据集扩展到 150 个课程文档和 750 条标注 QA；实现 BM25 + dense RRF 融合检索、GraphRAG 概念扩展、RAPTOR summary tree、Hybrid RAPTOR 检索、证据压缩和自适应生成评估，使整体检索 Recall@5 达到 0.9813，并在生成侧达到 0.9909 Faithfulness、0.9814 Answer Coverage 和 0.9687 Citation Recall。
