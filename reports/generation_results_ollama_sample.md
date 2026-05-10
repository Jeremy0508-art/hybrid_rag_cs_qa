# Generation Evaluation Report

- Method: `graph_pruned`
- Generator: `ollama`
- Used generators: `ollama`
- Top-k evidence: `3`
- Questions: `1`
- Limit: `1`

## Metrics

| Metric | Score |
|---|---:|
| Faithfulness | 0.8421 |
| Answer Coverage | 0.0000 |
| Citation Accuracy | 0.3333 |
| Citation Recall | 1.0000 |

## Sample Outputs

### q1

- Question: 为什么线程切换通常比进程切换开销更低？
- Generated: 线程切换通常比进程切换开销更低；共享内存也会引入同步问题；CPU 调度算法决定就绪进程获得处理器的顺序；先来先服务实现简单但可能导致短作业等待过长。
- Gold: 线程共享同一进程的地址空间和资源，因此切换时不需要像进程切换那样更换完整资源上下文。
- Citations: os-进程与线程, os-cpu-调度算法, os-虚拟内存与页面置换
- Scores: faithfulness=0.8421, coverage=0.0000, citation_accuracy=0.3333, citation_recall=1.0000
