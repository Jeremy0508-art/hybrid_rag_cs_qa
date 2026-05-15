# Runbook

这份运行手册用于复现扩展数据集、检索评估、生成评估和展示材料。

## 1. Environment

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install -e .
```

可选开发依赖：

```powershell
pip install pytest
```

可选 embedding 后端：

```powershell
pip install -r requirements-embeddings.txt
$env:CS_RAG_DENSE_BACKEND="sentence-transformers"
$env:CS_RAG_EMBEDDING_MODEL="BAAI/bge-small-zh-v1.5"
```

## 2. Standard Reproduction

```powershell
cs-rag build-expanded-dataset
cs-rag prepare
cs-rag train-reranker
cs-rag build-raptor-tree
cs-rag evaluate
cs-rag evaluate-generation --method graph_raptor_pruned --top-k 3 --adaptive-top-k --multi-hop-top-k 4
cs-rag build-showcase
pytest -q
```

主要输出：

| File | Purpose |
|---|---|
| `data/raw/cs_courses_expanded.md` | 扩展后的课程语料 |
| `data/qa/eval_qa_expanded.jsonl` | 扩展后的 QA 评估集 |
| `artifacts/raptor_tree.json` | RAPTOR summary tree |
| `reports/experiment_results.md` | 检索指标和分组分析 |
| `reports/error_analysis.md` | 错误案例 |
| `reports/generation_results.md` | 生成指标和分组分析 |
| `reports/generation_results_*_adaptive.md` | 不同方法的生成对比实验 |
| `reports/final_showcase.md` | 最终展示页 |
| `reports/interview_cheatsheet.md` | 面试速查 |
| `reports/artifact_index.md` | 交付文件索引 |
| `reports/submission_checklist.md` | 提交和打包检查清单 |
| `reports/figures/*.svg` | 可视化图表 |

## 3. Key Numbers

| Method | Recall@5 | MRR | NDCG | Context Precision |
|---|---:|---:|---:|---:|
| naive | 0.9667 | 0.9817 | 0.9638 | 0.4391 |
| hybrid_raptor | 0.9813 | 0.9822 | 0.9723 | 0.4400 |
| graph_raptor_pruned | 0.9667 | 0.9833 | 0.9663 | 0.5353 |

| Generator Setup | Faithfulness | Answer Coverage | Citation Accuracy | Citation Recall |
|---|---:|---:|---:|---:|
| `graph_raptor_pruned`, adaptive top-k | 0.9909 | 0.9814 | 0.4730 | 0.9687 |

## 4. Local Ollama LLM

拉取 3B 模型并创建项目专用模型：

```powershell
ollama pull modelscope.cn/Qwen/Qwen2.5-3B-Instruct-GGUF
ollama create qwen-rag:3b -f ollama\Modelfile.qwen-rag-3b
```

运行真实 LLM 问答：

```powershell
$env:CS_RAG_LLM_MODEL="qwen-rag:3b"
cs-rag ask "Why can GraphRAG improve recall but reduce context precision?" --generator ollama
```

## 5. Demo Order

1. 讲问题：普通 chunk 相似度很难同时处理术语精确匹配、改写问法、多跳线索和引用质量。
2. 讲数据：项目已扩展到 150 个课程文档和 750 条 QA，并加入分组标签。
3. 讲方法：BM25 + dense、GraphRAG、RAPTOR tree、Hybrid RAPTOR、evidence pruning。
4. 讲结果：`hybrid_raptor` 取得最高整体 Recall@5，`graph_raptor_pruned` 更适合作为生成入口。
5. 讲生成：adaptive top-k 为多跳问题提供更多证据预算，同时保留压缩后的上下文质量。
6. 讲后续：更强 embedding、CrossEncoder reranker、LLM summarizer、LLM-as-judge。

## 6. Final Checklist

- `pytest -q` passes.
- `cs-rag evaluate` 和 `cs-rag evaluate-generation` 已重新生成报告。
- README contains the current key results and reproduction commands.
- `RESUME.md` has Chinese and English resume bullets.
- `reports/interview_cheatsheet.md` can support a 30-second and 2-minute explanation.
- `reports/research_report_template.md` matches the expanded RAPTOR version.
