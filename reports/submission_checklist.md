# Submission Checklist

Use this checklist before committing or packaging the upgraded project.

## Repository Boundary

The Git repository root is:

```text
D:/RAG_Workspace/hybrid_rag_cs_qa
```

The sibling folder below is a reference project and is not part of this Git repository:

```text
D:/RAG_Workspace/raptor
```

Do not delete the sibling `raptor` folder just to commit `hybrid_rag_cs_qa`. It will not be included when committing from the `hybrid_rag_cs_qa` repository. If packaging manually, package only the `hybrid_rag_cs_qa` folder.

## Include In Commit

| Area | Files |
|---|---|
| Expanded dataset | `data/raw/cs_courses_expanded.md`, `data/qa/eval_qa_expanded.jsonl` |
| RAPTOR implementation | `src/hybrid_rag_cs_qa/raptor_*.py`, `src/hybrid_rag_cs_qa/summarizers.py` |
| Dataset and chunking | `src/hybrid_rag_cs_qa/dataset_builder.py`, `src/hybrid_rag_cs_qa/chunking.py` |
| Retrieval/generation changes | `pipeline.py`, `generation.py`, `evaluate.py`, `reranker.py`, `data.py`, `schema.py`, `cli.py` |
| Reports | `reports/*.md`, `reports/figures/*.svg` |
| Tests | `tests/test_*.py` |
| Docs | `README.md`, `RUNBOOK.md`, `RESUME.md`, `pyproject.toml` |

## Exclude From Commit

These are generated or environment-local files and should remain ignored:

| Pattern | Reason |
|---|---|
| `artifacts/*.json` | Generated RAPTOR tree |
| `artifacts/*.joblib` | Trained reranker artifact |
| `reports/*.json` | Large machine-readable experiment outputs |
| `.pytest_cache/` | Test cache |
| `__pycache__/` | Python bytecode cache |
| `*.egg-info/` | Local package metadata |
| `.venv/` | Local virtual environment |

## Verification Commands

```powershell
cs-rag build-expanded-dataset
cs-rag prepare
cs-rag train-reranker
cs-rag build-raptor-tree
cs-rag evaluate
cs-rag evaluate-generation --method graph_raptor_pruned --top-k 3 --adaptive-top-k --multi-hop-top-k 4
cs-rag build-showcase
pytest -q
git diff --check
```

## Suggested Commit Message

```text
Upgrade CS QA RAG with RAPTOR and expanded evaluation
```
