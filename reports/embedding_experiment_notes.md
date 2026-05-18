# Embedding Backend Experiment Notes

## Current Status

The project supports two dense retrieval backends:

| Backend | How to enable | Notes |
|---|---|---|
| TF-IDF | Default | Lightweight, deterministic, no model download required |
| sentence-transformers | Environment variables | Can use BGE/E5 or another local embedding model |

## Enable BGE

```powershell
pip install -r requirements-embeddings.txt
$env:CS_RAG_DENSE_BACKEND="sentence-transformers"
$env:CS_RAG_EMBEDDING_MODEL="BAAI/bge-small-zh-v1.5"
cs-rag prepare
cs-rag train-reranker
cs-rag evaluate
```

## Run Note

The current main reports use the default TF-IDF dense backend for reproducibility. The code path for sentence-transformers is implemented, but the first local attempt to load `BAAI/bge-small-zh-v1.5` required downloading model files from HuggingFace and timed out in this environment.

This does not block the project architecture. If the model is already cached locally, or if a HuggingFace mirror/proxy is configured, the same CLI commands can run with the sentence-transformers backend.

## Recommended Next Experiments

1. Pre-download `BAAI/bge-small-zh-v1.5` in a stable network environment.
2. Set `CS_RAG_EMBEDDING_MODEL` to a local model directory.
3. Compare BGE/E5 against the TF-IDF baseline on the same 3,600 QA benchmark.
4. Add a CrossEncoder or bge-reranker after candidate fusion for paraphrase-heavy questions.
