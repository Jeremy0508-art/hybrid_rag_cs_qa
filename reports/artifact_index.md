# Artifact Index

This file lists the main artifacts to inspect, reproduce, or present.

## Core Inputs

| File | Purpose |
|---|---|
| `data/raw/cs_courses_expanded.md` | Expanded 150-document CS course corpus |
| `data/qa/eval_qa_expanded.jsonl` | Expanded 750-item QA benchmark |

## Core Code

| File | Purpose |
|---|---|
| `src/hybrid_rag_cs_qa/pipeline.py` | Search method orchestration |
| `src/hybrid_rag_cs_qa/raptor_builder.py` | RAPTOR recursive tree construction |
| `src/hybrid_rag_cs_qa/raptor_retriever.py` | RAPTOR collapsed and top-down retrieval |
| `src/hybrid_rag_cs_qa/evaluate.py` | Retrieval evaluation and grouped metrics |
| `src/hybrid_rag_cs_qa/generation.py` | Generation evaluation and adaptive top-k |
| `src/hybrid_rag_cs_qa/cli.py` | Reproducible CLI entry points |

## Main Reports

| File | Purpose |
|---|---|
| `reports/experiment_results.md` | Retrieval metrics across all methods |
| `reports/generation_results.md` | Default generation metrics for `graph_raptor_pruned` with adaptive top-k |
| `reports/error_analysis.md` | Retrieval error and behavior analysis |
| `reports/research_report_template.md` | Research-style writeup |
| `reports/final_showcase.md` | Short project showcase |
| `reports/interview_cheatsheet.md` | Interview-ready explanation |

## Comparison Reports

| File | Purpose |
|---|---|
| `reports/generation_results_graph_raptor_pruned.md` | Non-adaptive generation report for `graph_raptor_pruned` |
| `reports/generation_results_graph_raptor_pruned_adaptive.md` | Adaptive generation report for `graph_raptor_pruned` |
| `reports/generation_results_hybrid_raptor.md` | Non-adaptive generation report for `hybrid_raptor` |
| `reports/generation_results_hybrid_raptor_adaptive.md` | Adaptive generation report for `hybrid_raptor` |

## Generated Artifacts

| File | Purpose |
|---|---|
| `artifacts/reranker.joblib` | Trained feature reranker |
| `artifacts/raptor_tree.json` | Serialized RAPTOR tree |
| `reports/figures/retrieval_metrics.svg` | Retrieval metrics chart |
| `reports/figures/generation_metrics.svg` | Generation metrics chart |

The large JSON result files are generated for reproducibility but ignored by git via `reports/*.json`.
