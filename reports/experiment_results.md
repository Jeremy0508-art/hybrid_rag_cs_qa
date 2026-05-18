# Hybrid RAG Experiment Report

## Metrics

| Method | Recall@5 | MRR | NDCG | Context Precision |
|---|---:|---:|---:|---:|
| naive | 0.9618 | 0.9979 | 0.9685 | 0.4068 |
| hybrid | 0.9647 | 0.9071 | 0.9025 | 0.4072 |
| hybrid_rerank | 0.9363 | 0.8978 | 0.8894 | 0.4069 |
| graph_reflect | 0.9256 | 0.8868 | 0.8744 | 0.4522 |
| graph_pruned | 0.8947 | 0.8828 | 0.8594 | 0.3853 |
| raptor | 0.9960 | 0.9972 | 0.9945 | 0.5272 |
| raptor_topdown | 0.9910 | 0.9927 | 0.9890 | 0.5170 |
| hybrid_raptor | 0.9806 | 0.9942 | 0.9758 | 0.4081 |
| graph_raptor_pruned | 0.9587 | 0.9418 | 0.9307 | 0.4533 |

Context Precision is measured on the final evidence context after a common evidence-budget compression step. Recall@5, MRR and NDCG are still measured on the original Top-5 retrieval results.

## Result Interpretation

On the expanded 3,600-QA benchmark, `raptor` becomes the strongest retrieval method with 0.9960 Recall@5, 0.9972 MRR, and 0.9945 NDCG. This is plausible because the expanded corpus is organized around repeated course topics viewed through multiple aspects, and RAPTOR's summary tree directly captures those hierarchical topic signals. In other words, the benchmark now contains many questions where high-level section summaries are helpful, not just exact keyword matching.

`hybrid_raptor` remains strong at 0.9806 Recall@5, but its RRF fusion can mix BM25, dense, graph, and RAPTOR candidates in a way that slightly weakens the pure RAPTOR ranking on this dataset. This is a useful tradeoff rather than a simple failure: hybrid fusion is more robust when retrieval signals disagree, while collapsed RAPTOR is especially well matched to this structured course corpus.

`graph_raptor_pruned` has lower Recall@5 because it is optimized as a generation entry point. It compresses the final evidence set after retrieving graph and RAPTOR candidates, so it gives up some recall to keep the final context smaller and more controllable. The generation comparison reports show the same tradeoff: `hybrid_raptor_adaptive` reaches higher Citation Recall, while `graph_raptor_pruned_adaptive` keeps a more selective evidence context.

## Grouped Metrics

### Topic

| Topic | Method | Questions | Recall@5 | MRR | NDCG | Context Precision |
|---|---|---:|---:|---:|---:|---:|
| Compilers | naive | 600 | 0.9575 | 0.9983 | 0.9658 | 0.4050 |
| Computer Networks | naive | 720 | 0.9604 | 0.9979 | 0.9664 | 0.4032 |
| Databases | naive | 600 | 0.9542 | 0.9983 | 0.9627 | 0.4017 |
| Information Retrieval | naive | 480 | 0.9563 | 0.9979 | 0.9639 | 0.4035 |
| Operating Systems | naive | 720 | 0.9618 | 0.9979 | 0.9692 | 0.4074 |
| RAG Systems | naive | 480 | 0.9844 | 0.9969 | 0.9860 | 0.4229 |
| Compilers | hybrid | 600 | 0.9750 | 0.9078 | 0.9094 | 0.4106 |
| Computer Networks | hybrid | 720 | 0.9583 | 0.9058 | 0.8954 | 0.4019 |
| Databases | hybrid | 600 | 0.9533 | 0.9147 | 0.8997 | 0.4011 |
| Information Retrieval | hybrid | 480 | 0.9594 | 0.9059 | 0.8982 | 0.4049 |
| Operating Systems | hybrid | 720 | 0.9625 | 0.9051 | 0.9007 | 0.4069 |
| RAG Systems | hybrid | 480 | 0.9844 | 0.9028 | 0.9151 | 0.4215 |
| Compilers | hybrid_rerank | 600 | 0.9408 | 0.9020 | 0.8932 | 0.3897 |
| Computer Networks | hybrid_rerank | 720 | 0.9347 | 0.8909 | 0.8872 | 0.3759 |
| Databases | hybrid_rerank | 600 | 0.9467 | 0.9078 | 0.9013 | 0.5222 |
| Information Retrieval | hybrid_rerank | 480 | 0.9323 | 0.9028 | 0.8897 | 0.3896 |
| Operating Systems | hybrid_rerank | 720 | 0.9306 | 0.9066 | 0.8899 | 0.3894 |
| RAG Systems | hybrid_rerank | 480 | 0.9323 | 0.8723 | 0.8722 | 0.3740 |
| Compilers | graph_reflect | 600 | 0.9300 | 0.9009 | 0.8857 | 0.4492 |
| Computer Networks | graph_reflect | 720 | 0.9174 | 0.8907 | 0.8683 | 0.3620 |
| Databases | graph_reflect | 600 | 0.9233 | 0.8938 | 0.8775 | 0.5053 |
| Information Retrieval | graph_reflect | 480 | 0.9458 | 0.8993 | 0.8931 | 0.5622 |
| Operating Systems | graph_reflect | 720 | 0.9090 | 0.8625 | 0.8547 | 0.4833 |
| RAG Systems | graph_reflect | 480 | 0.9396 | 0.8787 | 0.8764 | 0.3681 |
| Compilers | graph_pruned | 600 | 0.9042 | 0.8983 | 0.8740 | 0.4181 |
| Computer Networks | graph_pruned | 720 | 0.8847 | 0.8854 | 0.8526 | 0.3620 |
| Databases | graph_pruned | 600 | 0.8992 | 0.8900 | 0.8652 | 0.3667 |
| Information Retrieval | graph_pruned | 480 | 0.9146 | 0.8969 | 0.8785 | 0.4212 |
| Operating Systems | graph_pruned | 720 | 0.8757 | 0.8576 | 0.8381 | 0.3845 |
| RAG Systems | graph_pruned | 480 | 0.9010 | 0.8743 | 0.8571 | 0.3681 |
| Compilers | raptor | 600 | 0.9950 | 0.9978 | 0.9943 | 0.5133 |
| Computer Networks | raptor | 720 | 0.9951 | 0.9972 | 0.9937 | 0.4287 |
| Databases | raptor | 600 | 0.9967 | 0.9978 | 0.9947 | 0.5967 |
| Information Retrieval | raptor | 480 | 0.9958 | 0.9972 | 0.9948 | 0.6389 |
| Operating Systems | raptor | 720 | 0.9965 | 0.9963 | 0.9947 | 0.5694 |
| RAG Systems | raptor | 480 | 0.9969 | 0.9972 | 0.9952 | 0.4306 |
| Compilers | raptor_topdown | 600 | 0.9942 | 0.9989 | 0.9943 | 0.5128 |
| Computer Networks | raptor_topdown | 720 | 0.9840 | 0.9814 | 0.9782 | 0.4935 |
| Databases | raptor_topdown | 600 | 0.9950 | 0.9989 | 0.9946 | 0.5403 |
| Information Retrieval | raptor_topdown | 480 | 0.9948 | 0.9972 | 0.9939 | 0.5774 |
| Operating Systems | raptor_topdown | 720 | 0.9854 | 0.9868 | 0.9828 | 0.5384 |
| RAG Systems | raptor_topdown | 480 | 0.9969 | 0.9986 | 0.9958 | 0.4361 |
| Compilers | hybrid_raptor | 600 | 0.9842 | 0.9983 | 0.9821 | 0.4117 |
| Computer Networks | hybrid_raptor | 720 | 0.9882 | 0.9986 | 0.9807 | 0.4032 |
| Databases | hybrid_raptor | 600 | 0.9842 | 0.9925 | 0.9731 | 0.4017 |
| Information Retrieval | hybrid_raptor | 480 | 0.9729 | 0.9969 | 0.9735 | 0.4049 |
| Operating Systems | hybrid_raptor | 720 | 0.9688 | 0.9972 | 0.9723 | 0.4079 |
| RAG Systems | hybrid_raptor | 480 | 0.9854 | 0.9771 | 0.9716 | 0.4229 |
| Compilers | graph_raptor_pruned | 600 | 0.9683 | 0.9526 | 0.9437 | 0.4344 |
| Computer Networks | graph_raptor_pruned | 720 | 0.9396 | 0.9427 | 0.9183 | 0.3674 |
| Databases | graph_raptor_pruned | 600 | 0.9500 | 0.9383 | 0.9239 | 0.5314 |
| Information Retrieval | graph_raptor_pruned | 480 | 0.9802 | 0.9595 | 0.9538 | 0.5391 |
| Operating Systems | graph_raptor_pruned | 720 | 0.9472 | 0.9248 | 0.9152 | 0.4722 |
| RAG Systems | graph_raptor_pruned | 480 | 0.9823 | 0.9392 | 0.9421 | 0.3937 |


### Question Type

| Question Type | Method | Questions | Recall@5 | MRR | NDCG | Context Precision |
|---|---|---:|---:|---:|---:|---:|
| application | naive | 360 | 1.0000 | 1.0000 | 1.0000 | 0.3333 |
| comparison | naive | 360 | 1.0000 | 1.0000 | 1.0000 | 0.3333 |
| concept_linking | naive | 360 | 0.6833 | 1.0000 | 0.7494 | 0.4481 |
| definition | naive | 360 | 1.0000 | 1.0000 | 1.0000 | 0.3333 |
| diagnostic | naive | 360 | 1.0000 | 1.0000 | 1.0000 | 0.3333 |
| hierarchical_summary | naive | 360 | 1.0000 | 1.0000 | 1.0000 | 0.3333 |
| mechanism | naive | 360 | 1.0000 | 1.0000 | 1.0000 | 0.3333 |
| misconception | naive | 360 | 1.0000 | 1.0000 | 1.0000 | 0.3333 |
| multi_hop | naive | 360 | 0.9736 | 1.0000 | 0.9787 | 0.6491 |
| multi_hop_paraphrase | naive | 360 | 0.9611 | 0.9792 | 0.9573 | 0.6370 |
| application | hybrid | 360 | 1.0000 | 0.5417 | 0.6617 | 0.3333 |
| comparison | hybrid | 360 | 1.0000 | 1.0000 | 1.0000 | 0.3333 |
| concept_linking | hybrid | 360 | 0.7083 | 0.9972 | 0.7652 | 0.4574 |
| definition | hybrid | 360 | 1.0000 | 0.9958 | 0.9969 | 0.3333 |
| diagnostic | hybrid | 360 | 1.0000 | 0.9972 | 0.9979 | 0.3333 |
| hierarchical_summary | hybrid | 360 | 1.0000 | 0.6014 | 0.7056 | 0.3333 |
| mechanism | hybrid | 360 | 1.0000 | 0.9972 | 0.9979 | 0.3333 |
| misconception | hybrid | 360 | 1.0000 | 0.9958 | 0.9969 | 0.3333 |
| multi_hop | hybrid | 360 | 0.9722 | 0.9847 | 0.9627 | 0.6472 |
| multi_hop_paraphrase | hybrid | 360 | 0.9667 | 0.9597 | 0.9404 | 0.6343 |
| application | hybrid_rerank | 360 | 1.0000 | 0.7958 | 0.8492 | 0.3481 |
| comparison | hybrid_rerank | 360 | 1.0000 | 1.0000 | 1.0000 | 0.3792 |
| concept_linking | hybrid_rerank | 360 | 0.8403 | 0.9819 | 0.8398 | 0.5417 |
| definition | hybrid_rerank | 360 | 1.0000 | 1.0000 | 1.0000 | 0.3759 |
| diagnostic | hybrid_rerank | 360 | 1.0000 | 0.9940 | 0.9955 | 0.4144 |
| hierarchical_summary | hybrid_rerank | 360 | 0.9972 | 0.7619 | 0.8231 | 0.3287 |
| mechanism | hybrid_rerank | 360 | 1.0000 | 1.0000 | 1.0000 | 0.3778 |
| misconception | hybrid_rerank | 360 | 1.0000 | 0.9981 | 0.9986 | 0.3806 |
| multi_hop | hybrid_rerank | 360 | 0.9181 | 0.8953 | 0.8625 | 0.5991 |
| multi_hop_paraphrase | hybrid_rerank | 360 | 0.6069 | 0.5512 | 0.5253 | 0.3231 |
| application | graph_reflect | 360 | 0.9833 | 0.7581 | 0.8167 | 0.3676 |
| comparison | graph_reflect | 360 | 1.0000 | 0.9889 | 0.9917 | 0.4861 |
| concept_linking | graph_reflect | 360 | 0.7722 | 0.9283 | 0.7651 | 0.4722 |
| definition | graph_reflect | 360 | 1.0000 | 0.9907 | 0.9930 | 0.4824 |
| diagnostic | graph_reflect | 360 | 0.9917 | 0.9792 | 0.9824 | 0.4750 |
| hierarchical_summary | graph_reflect | 360 | 0.9639 | 0.7717 | 0.8215 | 0.3148 |
| mechanism | graph_reflect | 360 | 1.0000 | 0.9931 | 0.9949 | 0.4875 |
| misconception | graph_reflect | 360 | 1.0000 | 0.9877 | 0.9908 | 0.4829 |
| multi_hop | graph_reflect | 360 | 0.8736 | 0.8349 | 0.7942 | 0.5699 |
| multi_hop_paraphrase | graph_reflect | 360 | 0.6708 | 0.6356 | 0.5939 | 0.3833 |
| application | graph_pruned | 360 | 0.9694 | 0.7546 | 0.8107 | 0.3231 |
| comparison | graph_pruned | 360 | 1.0000 | 0.9889 | 0.9917 | 0.3810 |
| concept_linking | graph_pruned | 360 | 0.7083 | 0.9250 | 0.7325 | 0.4722 |
| definition | graph_pruned | 360 | 0.9917 | 0.9889 | 0.9896 | 0.3745 |
| diagnostic | graph_pruned | 360 | 0.9917 | 0.9792 | 0.9824 | 0.3519 |
| hierarchical_summary | graph_pruned | 360 | 0.9444 | 0.7671 | 0.8134 | 0.3148 |
| mechanism | graph_pruned | 360 | 1.0000 | 0.9931 | 0.9949 | 0.3440 |
| misconception | graph_pruned | 360 | 0.9917 | 0.9856 | 0.9872 | 0.3718 |
| multi_hop | graph_pruned | 360 | 0.7750 | 0.8306 | 0.7461 | 0.5366 |
| multi_hop_paraphrase | graph_pruned | 360 | 0.5750 | 0.6153 | 0.5455 | 0.3833 |
| application | raptor | 360 | 1.0000 | 1.0000 | 1.0000 | 0.4889 |
| comparison | raptor | 360 | 1.0000 | 1.0000 | 1.0000 | 0.4889 |
| concept_linking | raptor | 360 | 1.0000 | 1.0000 | 1.0000 | 0.6667 |
| definition | raptor | 360 | 1.0000 | 1.0000 | 1.0000 | 0.4889 |
| diagnostic | raptor | 360 | 1.0000 | 1.0000 | 1.0000 | 0.4889 |
| hierarchical_summary | raptor | 360 | 1.0000 | 1.0000 | 1.0000 | 0.3333 |
| mechanism | raptor | 360 | 1.0000 | 1.0000 | 1.0000 | 0.4889 |
| misconception | raptor | 360 | 1.0000 | 1.0000 | 1.0000 | 0.4889 |
| multi_hop | raptor | 360 | 1.0000 | 1.0000 | 0.9931 | 0.7056 |
| multi_hop_paraphrase | raptor | 360 | 0.9597 | 0.9722 | 0.9520 | 0.6333 |
| application | raptor_topdown | 360 | 1.0000 | 1.0000 | 1.0000 | 0.4838 |
| comparison | raptor_topdown | 360 | 1.0000 | 1.0000 | 1.0000 | 0.4662 |
| concept_linking | raptor_topdown | 360 | 1.0000 | 1.0000 | 1.0000 | 0.6778 |
| definition | raptor_topdown | 360 | 1.0000 | 1.0000 | 1.0000 | 0.4847 |
| diagnostic | raptor_topdown | 360 | 1.0000 | 1.0000 | 1.0000 | 0.4787 |
| hierarchical_summary | raptor_topdown | 360 | 1.0000 | 1.0000 | 1.0000 | 0.3333 |
| mechanism | raptor_topdown | 360 | 1.0000 | 1.0000 | 1.0000 | 0.4741 |
| misconception | raptor_topdown | 360 | 1.0000 | 1.0000 | 1.0000 | 0.4718 |
| multi_hop | raptor_topdown | 360 | 1.0000 | 1.0000 | 0.9931 | 0.7056 |
| multi_hop_paraphrase | raptor_topdown | 360 | 0.9097 | 0.9271 | 0.8967 | 0.5944 |
| application | hybrid_raptor | 360 | 1.0000 | 0.9792 | 0.9846 | 0.3333 |
| comparison | hybrid_raptor | 360 | 1.0000 | 1.0000 | 1.0000 | 0.3333 |
| concept_linking | hybrid_raptor | 360 | 0.8667 | 1.0000 | 0.8485 | 0.4648 |
| definition | hybrid_raptor | 360 | 1.0000 | 1.0000 | 1.0000 | 0.3333 |
| diagnostic | hybrid_raptor | 360 | 1.0000 | 1.0000 | 1.0000 | 0.3333 |
| hierarchical_summary | hybrid_raptor | 360 | 1.0000 | 0.9833 | 0.9877 | 0.3333 |
| mechanism | hybrid_raptor | 360 | 1.0000 | 1.0000 | 1.0000 | 0.3333 |
| misconception | hybrid_raptor | 360 | 1.0000 | 1.0000 | 1.0000 | 0.3333 |
| multi_hop | hybrid_raptor | 360 | 0.9750 | 1.0000 | 0.9800 | 0.6481 |
| multi_hop_paraphrase | hybrid_raptor | 360 | 0.9639 | 0.9792 | 0.9574 | 0.6352 |
| application | graph_raptor_pruned | 360 | 0.9611 | 0.7806 | 0.8277 | 0.3838 |
| comparison | graph_raptor_pruned | 360 | 1.0000 | 0.9986 | 0.9990 | 0.4833 |
| concept_linking | graph_raptor_pruned | 360 | 0.8139 | 0.9694 | 0.8280 | 0.5426 |
| definition | graph_raptor_pruned | 360 | 1.0000 | 0.9944 | 0.9959 | 0.4556 |
| diagnostic | graph_raptor_pruned | 360 | 0.9917 | 0.9833 | 0.9855 | 0.4870 |
| hierarchical_summary | graph_raptor_pruned | 360 | 0.9639 | 0.8190 | 0.8568 | 0.3407 |
| mechanism | graph_raptor_pruned | 360 | 1.0000 | 0.9986 | 0.9990 | 0.4264 |
| misconception | graph_raptor_pruned | 360 | 1.0000 | 0.9972 | 0.9979 | 0.4847 |
| multi_hop | graph_raptor_pruned | 360 | 0.9361 | 0.9618 | 0.9293 | 0.4681 |
| multi_hop_paraphrase | graph_raptor_pruned | 360 | 0.9208 | 0.9153 | 0.8882 | 0.4604 |


### Difficulty

| Difficulty | Method | Questions | Recall@5 | MRR | NDCG | Context Precision |
|---|---|---:|---:|---:|---:|---:|
| easy | naive | 360 | 1.0000 | 1.0000 | 1.0000 | 0.3333 |
| hard | naive | 1440 | 0.9045 | 0.9948 | 0.9214 | 0.5169 |
| medium | naive | 1800 | 1.0000 | 1.0000 | 1.0000 | 0.3333 |
| easy | hybrid | 360 | 1.0000 | 0.9958 | 0.9969 | 0.3333 |
| hard | hybrid | 1440 | 0.9118 | 0.9847 | 0.9165 | 0.5181 |
| medium | hybrid | 1800 | 1.0000 | 0.8272 | 0.8724 | 0.3333 |
| easy | hybrid_rerank | 360 | 1.0000 | 1.0000 | 1.0000 | 0.3759 |
| hard | hybrid_rerank | 1440 | 0.8413 | 0.8556 | 0.8058 | 0.4696 |
| medium | hybrid_rerank | 1800 | 0.9994 | 0.9112 | 0.9342 | 0.3629 |
| easy | graph_reflect | 360 | 1.0000 | 0.9907 | 0.9930 | 0.4824 |
| hard | graph_reflect | 1440 | 0.8271 | 0.8445 | 0.7839 | 0.4751 |
| medium | graph_reflect | 1800 | 0.9894 | 0.8999 | 0.9231 | 0.4278 |
| easy | graph_pruned | 360 | 0.9917 | 0.9889 | 0.9896 | 0.3745 |
| hard | graph_pruned | 1440 | 0.7625 | 0.8375 | 0.7517 | 0.4360 |
| medium | graph_pruned | 1800 | 0.9811 | 0.8979 | 0.9196 | 0.3469 |
| easy | raptor | 360 | 1.0000 | 1.0000 | 1.0000 | 0.4889 |
| hard | raptor | 1440 | 0.9899 | 0.9931 | 0.9863 | 0.6236 |
| medium | raptor | 1800 | 1.0000 | 1.0000 | 1.0000 | 0.4578 |
| easy | raptor_topdown | 360 | 1.0000 | 1.0000 | 1.0000 | 0.4847 |
| hard | raptor_topdown | 1440 | 0.9774 | 0.9818 | 0.9724 | 0.6141 |
| medium | raptor_topdown | 1800 | 1.0000 | 1.0000 | 1.0000 | 0.4458 |
| easy | hybrid_raptor | 360 | 1.0000 | 1.0000 | 1.0000 | 0.3333 |
| hard | hybrid_raptor | 1440 | 0.9514 | 0.9948 | 0.9465 | 0.5204 |
| medium | hybrid_raptor | 1800 | 1.0000 | 0.9925 | 0.9945 | 0.3333 |
| easy | graph_raptor_pruned | 360 | 1.0000 | 0.9944 | 0.9959 | 0.4556 |
| hard | graph_raptor_pruned | 1440 | 0.9156 | 0.9575 | 0.9078 | 0.4895 |
| medium | graph_raptor_pruned | 1800 | 0.9850 | 0.9188 | 0.9361 | 0.4238 |


### Requires Multi-hop

| Requires Multi-hop | Method | Questions | Recall@5 | MRR | NDCG | Context Precision |
|---|---|---:|---:|---:|---:|---:|
| False | naive | 2520 | 1.0000 | 1.0000 | 1.0000 | 0.3333 |
| True | naive | 1080 | 0.8727 | 0.9931 | 0.8952 | 0.5781 |
| False | hybrid | 2520 | 1.0000 | 0.8756 | 0.9081 | 0.3333 |
| True | hybrid | 1080 | 0.8824 | 0.9806 | 0.8894 | 0.5796 |
| False | hybrid_rerank | 2520 | 0.9996 | 0.9357 | 0.9524 | 0.3721 |
| True | hybrid_rerank | 1080 | 0.7884 | 0.8095 | 0.7425 | 0.4880 |
| False | graph_reflect | 2520 | 0.9913 | 0.9242 | 0.9416 | 0.4423 |
| True | graph_reflect | 1080 | 0.7722 | 0.7996 | 0.7177 | 0.4752 |
| False | graph_pruned | 2520 | 0.9841 | 0.9225 | 0.9386 | 0.3516 |
| True | graph_pruned | 1080 | 0.6861 | 0.7903 | 0.6747 | 0.4640 |
| False | raptor | 2520 | 1.0000 | 1.0000 | 1.0000 | 0.4667 |
| True | raptor | 1080 | 0.9866 | 0.9907 | 0.9817 | 0.6685 |
| False | raptor_topdown | 2520 | 1.0000 | 1.0000 | 1.0000 | 0.4561 |
| True | raptor_topdown | 1080 | 0.9699 | 0.9757 | 0.9632 | 0.6593 |
| False | hybrid_raptor | 2520 | 1.0000 | 0.9946 | 0.9960 | 0.3333 |
| True | hybrid_raptor | 1080 | 0.9352 | 0.9931 | 0.9286 | 0.5827 |
| False | graph_raptor_pruned | 2520 | 0.9881 | 0.9388 | 0.9517 | 0.4374 |
| True | graph_raptor_pruned | 1080 | 0.8903 | 0.9488 | 0.8818 | 0.4904 |


### Answer Style

| Answer Style | Method | Questions | Recall@5 | MRR | NDCG | Context Precision |
|---|---|---:|---:|---:|---:|---:|
| citation-grounded | naive | 1800 | 1.0000 | 1.0000 | 1.0000 | 0.3333 |
| paraphrase | naive | 720 | 0.9806 | 0.9896 | 0.9787 | 0.4852 |
| summary-level | naive | 360 | 1.0000 | 1.0000 | 1.0000 | 0.3333 |
| title-explicit | naive | 720 | 0.8285 | 1.0000 | 0.8641 | 0.5486 |
| citation-grounded | hybrid | 1800 | 1.0000 | 0.9064 | 0.9309 | 0.3333 |
| paraphrase | hybrid | 720 | 0.9833 | 0.9778 | 0.9686 | 0.4838 |
| summary-level | hybrid | 360 | 1.0000 | 0.6014 | 0.7056 | 0.3333 |
| title-explicit | hybrid | 720 | 0.8403 | 0.9910 | 0.8639 | 0.5523 |
| citation-grounded | hybrid_rerank | 1800 | 1.0000 | 0.9580 | 0.9690 | 0.3791 |
| paraphrase | hybrid_rerank | 720 | 0.8035 | 0.7747 | 0.7620 | 0.3519 |
| summary-level | hybrid_rerank | 360 | 0.9972 | 0.7619 | 0.8231 | 0.3287 |
| title-explicit | hybrid_rerank | 720 | 0.8792 | 0.9386 | 0.8511 | 0.5704 |
| citation-grounded | graph_reflect | 1800 | 0.9950 | 0.9420 | 0.9557 | 0.4597 |
| paraphrase | graph_reflect | 720 | 0.8354 | 0.8116 | 0.7924 | 0.4331 |
| summary-level | graph_reflect | 360 | 0.9639 | 0.7717 | 0.8215 | 0.3148 |
| title-explicit | graph_reflect | 720 | 0.8229 | 0.8816 | 0.7796 | 0.5211 |
| citation-grounded | graph_pruned | 1800 | 0.9906 | 0.9409 | 0.9539 | 0.3549 |
| paraphrase | graph_pruned | 720 | 0.7833 | 0.8005 | 0.7664 | 0.3775 |
| summary-level | graph_pruned | 360 | 0.9444 | 0.7671 | 0.8134 | 0.3148 |
| title-explicit | graph_pruned | 720 | 0.7417 | 0.8778 | 0.7393 | 0.5044 |
| citation-grounded | raptor | 1800 | 1.0000 | 1.0000 | 1.0000 | 0.4889 |
| paraphrase | raptor | 720 | 0.9799 | 0.9861 | 0.9760 | 0.5611 |
| summary-level | raptor | 360 | 1.0000 | 1.0000 | 1.0000 | 0.3333 |
| title-explicit | raptor | 720 | 1.0000 | 1.0000 | 0.9965 | 0.6861 |
| citation-grounded | raptor_topdown | 1800 | 1.0000 | 1.0000 | 1.0000 | 0.4775 |
| paraphrase | raptor_topdown | 720 | 0.9549 | 0.9635 | 0.9483 | 0.5331 |
| summary-level | raptor_topdown | 360 | 1.0000 | 1.0000 | 1.0000 | 0.3333 |
| title-explicit | raptor_topdown | 720 | 1.0000 | 1.0000 | 0.9965 | 0.6917 |
| citation-grounded | hybrid_raptor | 1800 | 1.0000 | 0.9958 | 0.9969 | 0.3333 |
| paraphrase | hybrid_raptor | 720 | 0.9819 | 0.9896 | 0.9787 | 0.4843 |
| summary-level | hybrid_raptor | 360 | 1.0000 | 0.9833 | 0.9877 | 0.3333 |
| title-explicit | hybrid_raptor | 720 | 0.9208 | 1.0000 | 0.9142 | 0.5565 |
| citation-grounded | graph_raptor_pruned | 1800 | 0.9906 | 0.9511 | 0.9614 | 0.4472 |
| paraphrase | graph_raptor_pruned | 720 | 0.9604 | 0.9563 | 0.9431 | 0.4726 |
| summary-level | graph_raptor_pruned | 360 | 0.9639 | 0.8190 | 0.8568 | 0.3407 |
| title-explicit | graph_raptor_pruned | 720 | 0.8750 | 0.9656 | 0.8787 | 0.5053 |

## Preliminary Conclusion

GraphRAG-style expansion is expected to improve recall on concept-related or multi-hop questions, but may reduce context precision when graph neighbors introduce noisy evidence. The error analysis file lists concrete cases for follow-up refinement.
