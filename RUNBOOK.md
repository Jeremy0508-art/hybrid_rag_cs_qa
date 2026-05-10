# Runbook

这份运行手册用于复现实验、更新报告和准备展示材料。

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
cs-rag prepare
cs-rag train-reranker
cs-rag evaluate
cs-rag evaluate-generation
cs-rag build-showcase
pytest -q
```

主要输出：

| File | Purpose |
|---|---|
| `reports/experiment_results.md` | 检索指标 |
| `reports/error_analysis.md` | 错误案例 |
| `reports/generation_results.md` | 抽取式生成评测 |
| `reports/final_showcase.md` | 最终展示页 |
| `reports/interview_cheatsheet.md` | 面试速查 |
| `reports/figures/*.svg` | 可视化图表 |

## 3. Local Ollama LLM

拉取 3B 模型并创建项目专用模板：

```powershell
ollama pull modelscope.cn/Qwen/Qwen2.5-3B-Instruct-GGUF
ollama create qwen-rag:3b -f ollama\Modelfile.qwen-rag-3b
```

运行真实 LLM 问答：

```powershell
$env:CS_RAG_LLM_MODEL="qwen-rag:3b"
cs-rag ask "GraphRAG 为什么可能提高召回率但降低 Context Precision？" --generator ollama
```

运行 10 条小规模评测：

```powershell
$env:CS_RAG_LLM_MODEL="qwen-rag:3b"
cs-rag evaluate-generation --generator ollama --limit 10 --out reports/generation_results_ollama_3b.json
```

对比报告：

| File | Purpose |
|---|---|
| `reports/generation_results_ollama_0_5b.md` | 0.5B 本地模型样例 |
| `reports/generation_results_ollama_3b.md` | 3B 本地模型样例 |
| `reports/ollama_model_comparison.md` | 0.5B/3B 对比解释 |

## 4. Demo Order

1. 讲问题：普通 RAG 在课程问答中会漏召回精确术语、多跳概念和跨章节关系。
2. 讲方法：Hybrid retrieval、GraphRAG、hard-negative reranker、evidence pruning。
3. 讲结果：GraphRAG 提升 Recall，Graph + Pruning 提升 Context Precision。
4. 讲生成：抽取式 baseline 稳定可复现，本地 Ollama 3B 跑通真实 LLM 链路。
5. 讲误差：0.5B 自动指标高但容易拼接无关片段；3B 更自然但词面指标偏低。
6. 讲后续：BGE/E5 embedding、CrossEncoder reranker、更强 7B LLM、LLM-as-judge。

## 5. Key Numbers

| Method | Recall@5 | MRR | NDCG | Context Precision |
|---|---:|---:|---:|---:|
| naive | 0.7500 | 0.7633 | 0.7512 | 0.5905 |
| graph_reflect | 0.9400 | 0.9183 | 0.9193 | 0.4140 |
| graph_pruned | 0.9367 | 0.9183 | 0.9173 | 0.6450 |

| Generator | Faithfulness | Citation Accuracy | Citation Recall |
|---|---:|---:|---:|
| extractive baseline | 0.7558 | 0.6450 | 0.9367 |
| Ollama `qwen-rag:3b`, 10-sample | 0.3378 | 0.6666 | 1.0000 |

## 6. Final Checklist

- `pytest -q` passes.
- `git status --short` has no unexpected files.
- README contains the key results and reproduction commands.
- `RESUME.md` has the final Chinese and English resume bullets.
- `reports/interview_cheatsheet.md` can support a 30-second and 2-minute explanation.
- `reports/research_report_template.md` contains retrieval, generation, Ollama, error analysis and limitations.
