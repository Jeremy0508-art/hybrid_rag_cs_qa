# Hybrid RAG Experiment Report

## Metrics

| Method | Recall@5 | MRR | NDCG | Context Precision |
|---|---:|---:|---:|---:|
| naive | 0.7500 | 0.7633 | 0.7512 | 0.5905 |
| hybrid | 0.7500 | 0.7583 | 0.7495 | 0.5905 |
| hybrid_rerank | 0.7500 | 0.7700 | 0.7554 | 0.5905 |
| graph_reflect | 0.9400 | 0.9183 | 0.9193 | 0.4140 |
| graph_pruned | 0.9367 | 0.9183 | 0.9173 | 0.6450 |

## Preliminary Conclusion

GraphRAG-style expansion is expected to improve recall on concept-related or multi-hop questions, but may reduce context precision when graph neighbors introduce noisy evidence. The error analysis file lists concrete cases for follow-up refinement.