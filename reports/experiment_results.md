# Hybrid RAG Experiment Report

## Metrics

| Method | Recall@5 | MRR | NDCG | Context Precision |
|---|---:|---:|---:|---:|
| naive | 0.9667 | 0.9817 | 0.9638 | 0.4391 |
| hybrid | 0.9713 | 0.9756 | 0.9635 | 0.4413 |
| hybrid_rerank | 0.9680 | 0.9337 | 0.9352 | 0.5124 |
| graph_reflect | 0.9773 | 0.9554 | 0.9524 | 0.5307 |
| graph_pruned | 0.9427 | 0.9518 | 0.9347 | 0.4309 |
| raptor | 0.9747 | 0.9763 | 0.9667 | 0.5396 |
| raptor_topdown | 0.9747 | 0.9757 | 0.9652 | 0.5209 |
| hybrid_raptor | 0.9813 | 0.9822 | 0.9723 | 0.4400 |
| graph_raptor_pruned | 0.9667 | 0.9833 | 0.9663 | 0.5353 |

Context Precision is measured on the final evidence context after a common evidence-budget compression step. Recall@5, MRR and NDCG are still measured on the original Top-5 retrieval results.

## Grouped Metrics

### Topic

| Topic | Method | Questions | Recall@5 | MRR | NDCG | Context Precision |
|---|---|---:|---:|---:|---:|---:|
| Compilers | naive | 125 | 0.9640 | 0.9920 | 0.9672 | 0.4427 |
| Computer Networks | naive | 150 | 0.9567 | 0.9653 | 0.9496 | 0.4267 |
| Databases | naive | 125 | 0.9640 | 0.9720 | 0.9548 | 0.4320 |
| Information Retrieval | naive | 100 | 0.9650 | 0.9900 | 0.9684 | 0.4433 |
| Operating Systems | naive | 150 | 0.9700 | 0.9900 | 0.9707 | 0.4444 |
| RAG Systems | naive | 100 | 0.9850 | 0.9850 | 0.9773 | 0.4500 |
| Compilers | hybrid | 125 | 0.9680 | 0.9880 | 0.9680 | 0.4427 |
| Computer Networks | hybrid | 150 | 0.9667 | 0.9622 | 0.9539 | 0.4333 |
| Databases | hybrid | 125 | 0.9680 | 0.9587 | 0.9512 | 0.4347 |
| Information Retrieval | hybrid | 100 | 0.9700 | 0.9850 | 0.9684 | 0.4467 |
| Operating Systems | hybrid | 150 | 0.9733 | 0.9800 | 0.9684 | 0.4467 |
| RAG Systems | hybrid | 100 | 0.9850 | 0.9850 | 0.9757 | 0.4467 |
| Compilers | hybrid_rerank | 125 | 0.9680 | 0.9400 | 0.9363 | 0.5093 |
| Computer Networks | hybrid_rerank | 150 | 0.9433 | 0.9012 | 0.9046 | 0.3978 |
| Databases | hybrid_rerank | 125 | 0.9480 | 0.9252 | 0.9210 | 0.5760 |
| Information Retrieval | hybrid_rerank | 100 | 0.9850 | 0.9517 | 0.9533 | 0.6167 |
| Operating Systems | hybrid_rerank | 150 | 0.9900 | 0.9500 | 0.9571 | 0.5689 |
| RAG Systems | hybrid_rerank | 100 | 0.9800 | 0.9425 | 0.9463 | 0.4200 |
| Compilers | graph_reflect | 125 | 0.9800 | 0.9773 | 0.9683 | 0.5307 |
| Computer Networks | graph_reflect | 150 | 0.9767 | 0.9368 | 0.9428 | 0.4200 |
| Databases | graph_reflect | 125 | 0.9720 | 0.9520 | 0.9470 | 0.5947 |
| Information Retrieval | graph_reflect | 100 | 0.9900 | 0.9825 | 0.9718 | 0.6600 |
| Operating Systems | graph_reflect | 150 | 0.9733 | 0.9451 | 0.9458 | 0.5778 |
| RAG Systems | graph_reflect | 100 | 0.9750 | 0.9483 | 0.9444 | 0.4167 |
| Compilers | graph_pruned | 125 | 0.9640 | 0.9773 | 0.9599 | 0.4427 |
| Computer Networks | graph_pruned | 150 | 0.9300 | 0.9311 | 0.9194 | 0.4200 |
| Databases | graph_pruned | 125 | 0.9400 | 0.9480 | 0.9303 | 0.4267 |
| Information Retrieval | graph_pruned | 100 | 0.9550 | 0.9800 | 0.9536 | 0.4483 |
| Operating Systems | graph_pruned | 150 | 0.9433 | 0.9411 | 0.9307 | 0.4333 |
| RAG Systems | graph_pruned | 100 | 0.9250 | 0.9433 | 0.9191 | 0.4167 |
| Compilers | raptor | 125 | 0.9800 | 0.9893 | 0.9764 | 0.5333 |
| Computer Networks | raptor | 150 | 0.9533 | 0.9556 | 0.9465 | 0.4356 |
| Databases | raptor | 125 | 0.9760 | 0.9645 | 0.9581 | 0.5920 |
| Information Retrieval | raptor | 100 | 0.9800 | 0.9867 | 0.9752 | 0.6533 |
| Operating Systems | raptor | 150 | 0.9800 | 0.9867 | 0.9752 | 0.5867 |
| RAG Systems | raptor | 100 | 0.9850 | 0.9800 | 0.9745 | 0.4533 |
| Compilers | raptor_topdown | 125 | 0.9800 | 0.9713 | 0.9635 | 0.5147 |
| Computer Networks | raptor_topdown | 150 | 0.9567 | 0.9649 | 0.9517 | 0.4333 |
| Databases | raptor_topdown | 125 | 0.9760 | 0.9752 | 0.9636 | 0.5427 |
| Information Retrieval | raptor_topdown | 100 | 0.9800 | 0.9867 | 0.9752 | 0.6033 |
| Operating Systems | raptor_topdown | 150 | 0.9767 | 0.9761 | 0.9664 | 0.5833 |
| RAG Systems | raptor_topdown | 100 | 0.9850 | 0.9867 | 0.9776 | 0.4567 |
| Compilers | hybrid_raptor | 125 | 0.9840 | 0.9920 | 0.9790 | 0.4453 |
| Computer Networks | hybrid_raptor | 150 | 0.9667 | 0.9652 | 0.9558 | 0.4267 |
| Databases | hybrid_raptor | 125 | 0.9880 | 0.9707 | 0.9664 | 0.4320 |
| Information Retrieval | hybrid_raptor | 100 | 0.9850 | 0.9900 | 0.9791 | 0.4467 |
| Operating Systems | hybrid_raptor | 150 | 0.9867 | 0.9900 | 0.9802 | 0.4467 |
| RAG Systems | hybrid_raptor | 100 | 0.9800 | 0.9900 | 0.9775 | 0.4467 |
| Compilers | graph_raptor_pruned | 125 | 0.9720 | 0.9920 | 0.9741 | 0.5300 |
| Computer Networks | graph_raptor_pruned | 150 | 0.9633 | 0.9789 | 0.9627 | 0.4928 |
| Databases | graph_raptor_pruned | 125 | 0.9560 | 0.9667 | 0.9509 | 0.5380 |
| Information Retrieval | graph_raptor_pruned | 100 | 0.9650 | 0.9900 | 0.9676 | 0.5825 |
| Operating Systems | graph_raptor_pruned | 150 | 0.9667 | 0.9900 | 0.9697 | 0.5767 |
| RAG Systems | graph_raptor_pruned | 100 | 0.9800 | 0.9833 | 0.9749 | 0.4933 |


### Question Type

| Question Type | Method | Questions | Recall@5 | MRR | NDCG | Context Precision |
|---|---|---:|---:|---:|---:|---:|
| comparison | naive | 150 | 1.0000 | 1.0000 | 1.0000 | 0.3333 |
| definition | naive | 150 | 1.0000 | 1.0000 | 1.0000 | 0.3333 |
| mechanism | naive | 150 | 1.0000 | 1.0000 | 1.0000 | 0.3333 |
| multi_hop | naive | 150 | 0.9267 | 1.0000 | 0.9417 | 0.6178 |
| multi_hop_paraphrase | naive | 150 | 0.9067 | 0.9087 | 0.8775 | 0.5778 |
| comparison | hybrid | 150 | 1.0000 | 1.0000 | 1.0000 | 0.3333 |
| definition | hybrid | 150 | 1.0000 | 0.9967 | 0.9975 | 0.3333 |
| mechanism | hybrid | 150 | 1.0000 | 1.0000 | 1.0000 | 0.3333 |
| multi_hop | hybrid | 150 | 0.9267 | 0.9700 | 0.9267 | 0.6156 |
| multi_hop_paraphrase | hybrid | 150 | 0.9300 | 0.9111 | 0.8934 | 0.5911 |
| comparison | hybrid_rerank | 150 | 1.0000 | 1.0000 | 1.0000 | 0.4889 |
| definition | hybrid_rerank | 150 | 1.0000 | 1.0000 | 1.0000 | 0.4889 |
| mechanism | hybrid_rerank | 150 | 1.0000 | 1.0000 | 1.0000 | 0.4489 |
| multi_hop | hybrid_rerank | 150 | 0.9833 | 0.9567 | 0.9524 | 0.6822 |
| multi_hop_paraphrase | hybrid_rerank | 150 | 0.8567 | 0.7117 | 0.7235 | 0.4533 |
| comparison | graph_reflect | 150 | 1.0000 | 1.0000 | 1.0000 | 0.4889 |
| definition | graph_reflect | 150 | 1.0000 | 1.0000 | 1.0000 | 0.4889 |
| mechanism | graph_reflect | 150 | 1.0000 | 1.0000 | 1.0000 | 0.4889 |
| multi_hop | graph_reflect | 150 | 0.9733 | 0.9667 | 0.9513 | 0.6800 |
| multi_hop_paraphrase | graph_reflect | 150 | 0.9133 | 0.8102 | 0.8108 | 0.5067 |
| comparison | graph_pruned | 150 | 1.0000 | 1.0000 | 1.0000 | 0.3389 |
| definition | graph_pruned | 150 | 1.0000 | 1.0000 | 1.0000 | 0.3356 |
| mechanism | graph_pruned | 150 | 1.0000 | 1.0000 | 1.0000 | 0.3378 |
| multi_hop | graph_pruned | 150 | 0.9533 | 0.9667 | 0.9408 | 0.6356 |
| multi_hop_paraphrase | graph_pruned | 150 | 0.7600 | 0.7922 | 0.7328 | 0.5067 |
| comparison | raptor | 150 | 1.0000 | 1.0000 | 1.0000 | 0.4889 |
| definition | raptor | 150 | 1.0000 | 1.0000 | 1.0000 | 0.4889 |
| mechanism | raptor | 150 | 1.0000 | 1.0000 | 1.0000 | 0.4889 |
| multi_hop | raptor | 150 | 1.0000 | 1.0000 | 0.9839 | 0.6667 |
| multi_hop_paraphrase | raptor | 150 | 0.8733 | 0.8816 | 0.8496 | 0.5644 |
| comparison | raptor_topdown | 150 | 1.0000 | 1.0000 | 1.0000 | 0.4622 |
| definition | raptor_topdown | 150 | 1.0000 | 1.0000 | 1.0000 | 0.4733 |
| mechanism | raptor_topdown | 150 | 1.0000 | 1.0000 | 1.0000 | 0.4622 |
| multi_hop | raptor_topdown | 150 | 1.0000 | 1.0000 | 0.9839 | 0.6667 |
| multi_hop_paraphrase | raptor_topdown | 150 | 0.8733 | 0.8787 | 0.8418 | 0.5400 |
| comparison | hybrid_raptor | 150 | 1.0000 | 1.0000 | 1.0000 | 0.3333 |
| definition | hybrid_raptor | 150 | 1.0000 | 1.0000 | 1.0000 | 0.3333 |
| mechanism | hybrid_raptor | 150 | 1.0000 | 1.0000 | 1.0000 | 0.3333 |
| multi_hop | hybrid_raptor | 150 | 0.9933 | 1.0000 | 0.9776 | 0.6222 |
| multi_hop_paraphrase | hybrid_raptor | 150 | 0.9133 | 0.9108 | 0.8840 | 0.5778 |
| comparison | graph_raptor_pruned | 150 | 1.0000 | 1.0000 | 1.0000 | 0.5944 |
| definition | graph_raptor_pruned | 150 | 1.0000 | 1.0000 | 1.0000 | 0.6111 |
| mechanism | graph_raptor_pruned | 150 | 1.0000 | 1.0000 | 1.0000 | 0.5544 |
| multi_hop | graph_raptor_pruned | 150 | 0.9467 | 0.9967 | 0.9562 | 0.4733 |
| multi_hop_paraphrase | graph_raptor_pruned | 150 | 0.8867 | 0.9200 | 0.8754 | 0.4433 |


### Difficulty

| Difficulty | Method | Questions | Recall@5 | MRR | NDCG | Context Precision |
|---|---|---:|---:|---:|---:|---:|
| easy | naive | 150 | 1.0000 | 1.0000 | 1.0000 | 0.3333 |
| hard | naive | 300 | 0.9167 | 0.9543 | 0.9096 | 0.5978 |
| medium | naive | 300 | 1.0000 | 1.0000 | 1.0000 | 0.3333 |
| easy | hybrid | 150 | 1.0000 | 0.9967 | 0.9975 | 0.3333 |
| hard | hybrid | 300 | 0.9283 | 0.9406 | 0.9100 | 0.6033 |
| medium | hybrid | 300 | 1.0000 | 1.0000 | 1.0000 | 0.3333 |
| easy | hybrid_rerank | 150 | 1.0000 | 1.0000 | 1.0000 | 0.4889 |
| hard | hybrid_rerank | 300 | 0.9200 | 0.8342 | 0.8379 | 0.5678 |
| medium | hybrid_rerank | 300 | 1.0000 | 1.0000 | 1.0000 | 0.4689 |
| easy | graph_reflect | 150 | 1.0000 | 1.0000 | 1.0000 | 0.4889 |
| hard | graph_reflect | 300 | 0.9433 | 0.8884 | 0.8811 | 0.5933 |
| medium | graph_reflect | 300 | 1.0000 | 1.0000 | 1.0000 | 0.4889 |
| easy | graph_pruned | 150 | 1.0000 | 1.0000 | 1.0000 | 0.3356 |
| hard | graph_pruned | 300 | 0.8567 | 0.8794 | 0.8368 | 0.5711 |
| medium | graph_pruned | 300 | 1.0000 | 1.0000 | 1.0000 | 0.3383 |
| easy | raptor | 150 | 1.0000 | 1.0000 | 1.0000 | 0.4889 |
| hard | raptor | 300 | 0.9367 | 0.9408 | 0.9168 | 0.6156 |
| medium | raptor | 300 | 1.0000 | 1.0000 | 1.0000 | 0.4889 |
| easy | raptor_topdown | 150 | 1.0000 | 1.0000 | 1.0000 | 0.4733 |
| hard | raptor_topdown | 300 | 0.9367 | 0.9393 | 0.9129 | 0.6033 |
| medium | raptor_topdown | 300 | 1.0000 | 1.0000 | 1.0000 | 0.4622 |
| easy | hybrid_raptor | 150 | 1.0000 | 1.0000 | 1.0000 | 0.3333 |
| hard | hybrid_raptor | 300 | 0.9533 | 0.9554 | 0.9308 | 0.6000 |
| medium | hybrid_raptor | 300 | 1.0000 | 1.0000 | 1.0000 | 0.3333 |
| easy | graph_raptor_pruned | 150 | 1.0000 | 1.0000 | 1.0000 | 0.6111 |
| hard | graph_raptor_pruned | 300 | 0.9167 | 0.9583 | 0.9158 | 0.4583 |
| medium | graph_raptor_pruned | 300 | 1.0000 | 1.0000 | 1.0000 | 0.5744 |


### Requires Multi-hop

| Requires Multi-hop | Method | Questions | Recall@5 | MRR | NDCG | Context Precision |
|---|---|---:|---:|---:|---:|---:|
| False | naive | 450 | 1.0000 | 1.0000 | 1.0000 | 0.3333 |
| True | naive | 300 | 0.9167 | 0.9543 | 0.9096 | 0.5978 |
| False | hybrid | 450 | 1.0000 | 0.9989 | 0.9992 | 0.3333 |
| True | hybrid | 300 | 0.9283 | 0.9406 | 0.9100 | 0.6033 |
| False | hybrid_rerank | 450 | 1.0000 | 1.0000 | 1.0000 | 0.4756 |
| True | hybrid_rerank | 300 | 0.9200 | 0.8342 | 0.8379 | 0.5678 |
| False | graph_reflect | 450 | 1.0000 | 1.0000 | 1.0000 | 0.4889 |
| True | graph_reflect | 300 | 0.9433 | 0.8884 | 0.8811 | 0.5933 |
| False | graph_pruned | 450 | 1.0000 | 1.0000 | 1.0000 | 0.3374 |
| True | graph_pruned | 300 | 0.8567 | 0.8794 | 0.8368 | 0.5711 |
| False | raptor | 450 | 1.0000 | 1.0000 | 1.0000 | 0.4889 |
| True | raptor | 300 | 0.9367 | 0.9408 | 0.9168 | 0.6156 |
| False | raptor_topdown | 450 | 1.0000 | 1.0000 | 1.0000 | 0.4659 |
| True | raptor_topdown | 300 | 0.9367 | 0.9393 | 0.9129 | 0.6033 |
| False | hybrid_raptor | 450 | 1.0000 | 1.0000 | 1.0000 | 0.3333 |
| True | hybrid_raptor | 300 | 0.9533 | 0.9554 | 0.9308 | 0.6000 |
| False | graph_raptor_pruned | 450 | 1.0000 | 1.0000 | 1.0000 | 0.5867 |
| True | graph_raptor_pruned | 300 | 0.9167 | 0.9583 | 0.9158 | 0.4583 |


### Answer Style

| Answer Style | Method | Questions | Recall@5 | MRR | NDCG | Context Precision |
|---|---|---:|---:|---:|---:|---:|
| citation-grounded | naive | 450 | 1.0000 | 1.0000 | 1.0000 | 0.3333 |
| paraphrase | naive | 150 | 0.9067 | 0.9087 | 0.8775 | 0.5778 |
| title-explicit | naive | 150 | 0.9267 | 1.0000 | 0.9417 | 0.6178 |
| citation-grounded | hybrid | 450 | 1.0000 | 0.9989 | 0.9992 | 0.3333 |
| paraphrase | hybrid | 150 | 0.9300 | 0.9111 | 0.8934 | 0.5911 |
| title-explicit | hybrid | 150 | 0.9267 | 0.9700 | 0.9267 | 0.6156 |
| citation-grounded | hybrid_rerank | 450 | 1.0000 | 1.0000 | 1.0000 | 0.4756 |
| paraphrase | hybrid_rerank | 150 | 0.8567 | 0.7117 | 0.7235 | 0.4533 |
| title-explicit | hybrid_rerank | 150 | 0.9833 | 0.9567 | 0.9524 | 0.6822 |
| citation-grounded | graph_reflect | 450 | 1.0000 | 1.0000 | 1.0000 | 0.4889 |
| paraphrase | graph_reflect | 150 | 0.9133 | 0.8102 | 0.8108 | 0.5067 |
| title-explicit | graph_reflect | 150 | 0.9733 | 0.9667 | 0.9513 | 0.6800 |
| citation-grounded | graph_pruned | 450 | 1.0000 | 1.0000 | 1.0000 | 0.3374 |
| paraphrase | graph_pruned | 150 | 0.7600 | 0.7922 | 0.7328 | 0.5067 |
| title-explicit | graph_pruned | 150 | 0.9533 | 0.9667 | 0.9408 | 0.6356 |
| citation-grounded | raptor | 450 | 1.0000 | 1.0000 | 1.0000 | 0.4889 |
| paraphrase | raptor | 150 | 0.8733 | 0.8816 | 0.8496 | 0.5644 |
| title-explicit | raptor | 150 | 1.0000 | 1.0000 | 0.9839 | 0.6667 |
| citation-grounded | raptor_topdown | 450 | 1.0000 | 1.0000 | 1.0000 | 0.4659 |
| paraphrase | raptor_topdown | 150 | 0.8733 | 0.8787 | 0.8418 | 0.5400 |
| title-explicit | raptor_topdown | 150 | 1.0000 | 1.0000 | 0.9839 | 0.6667 |
| citation-grounded | hybrid_raptor | 450 | 1.0000 | 1.0000 | 1.0000 | 0.3333 |
| paraphrase | hybrid_raptor | 150 | 0.9133 | 0.9108 | 0.8840 | 0.5778 |
| title-explicit | hybrid_raptor | 150 | 0.9933 | 1.0000 | 0.9776 | 0.6222 |
| citation-grounded | graph_raptor_pruned | 450 | 1.0000 | 1.0000 | 1.0000 | 0.5867 |
| paraphrase | graph_raptor_pruned | 150 | 0.8867 | 0.9200 | 0.8754 | 0.4433 |
| title-explicit | graph_raptor_pruned | 150 | 0.9467 | 0.9967 | 0.9562 | 0.4733 |

## Preliminary Conclusion

GraphRAG-style expansion is expected to improve recall on concept-related or multi-hop questions, but may reduce context precision when graph neighbors introduce noisy evidence. The error analysis file lists concrete cases for follow-up refinement.
