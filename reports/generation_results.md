# Generation Evaluation Report

- Method: `graph_pruned`
- Generator: `extractive`
- Used generators: `extractive`
- Top-k evidence: `3`
- Questions: `100`

## Metrics

| Metric | Score |
|---|---:|
| Faithfulness | 0.7558 |
| Answer Coverage | 0.2073 |
| Citation Accuracy | 0.6450 |
| Citation Recall | 0.9367 |

## Sample Outputs

### q1

- Question: 为什么线程切换通常比进程切换开销更低？
- Generated: 进程是资源分配的基本单位，拥有独立地址空间、文件句柄和其他系统资源。 [os-进程与线程]CPU 调度算法决定就绪进程获得处理器的顺序。 [os-cpu-调度算法]虚拟内存通过地址转换让进程获得大于物理内存的逻辑地址空间。 [os-虚拟内存与页面置换]
- Gold: 线程共享同一进程的地址空间和资源，因此切换时不需要像进程切换那样更换完整资源上下文。
- Citations: os-进程与线程, os-cpu-调度算法, os-虚拟内存与页面置换
- Scores: faithfulness=0.7667, coverage=0.0000, citation_accuracy=0.3333, citation_recall=1.0000

### q2

- Question: 互斥锁、信号量和管程分别适合解决什么并发问题？
- Generated: 并发程序中多个线程访问共享变量时可能产生竞态条件，因此需要同步和互斥机制。 [os-同步互斥与信号量]死锁是多个进程因竞争资源而永久等待的状态。 [os-死锁与银行家算法]RAG 通过在生成答案前检索外部知识，缓解大模型知识过时和幻觉问题。 [ai-rag-检索增强生成]
- Gold: 互斥锁用于保护临界区，信号量适合描述资源计数约束，管程把共享数据和操作封装起来并通过条件变量实现等待通知。
- Citations: os-同步互斥与信号量, ai-rag-检索增强生成, os-死锁与银行家算法
- Scores: faithfulness=0.7188, coverage=0.0000, citation_accuracy=0.3333, citation_recall=1.0000

### q3

- Question: 死锁产生需要哪些必要条件，银行家算法如何避免死锁？
- Generated: 死锁产生通常需要互斥、请求并保持、不可剥夺、循环等待四个必要条件。 [os-死锁与银行家算法]
- Gold: 死锁需要互斥、请求并保持、不可剥夺和循环等待。银行家算法通过安全性检查，只在系统仍存在安全序列时分配资源。
- Citations: os-死锁与银行家算法
- Scores: faithfulness=0.7500, coverage=0.2857, citation_accuracy=1.0000, citation_recall=1.0000

### q4

- Question: LRU 页面置换为什么能利用程序局部性？
- Generated: LRU 页面置换算法优先淘汰最长时间未被访问的页面，适合利用程序局部性。 [os-虚拟内存与页面置换]
- Gold: LRU 淘汰最长时间未被访问的页面，假设近期未访问的页面近期继续被访问的概率较低，因此符合时间局部性。
- Citations: os-虚拟内存与页面置换
- Scores: faithfulness=0.7857, coverage=0.4286, citation_accuracy=1.0000, citation_recall=1.0000

### q5

- Question: TLB 为什么可以降低虚拟地址转换开销？
- Generated: TLB 是页表项的高速缓存，可以显著降低地址转换开销。 [os-页表与-tlb]
- Gold: TLB 缓存常用页表项，命中时无需再次访问页表，因此能减少地址转换所需的内存访问次数。
- Citations: os-页表与-tlb
- Scores: faithfulness=0.7000, coverage=0.0909, citation_accuracy=1.0000, citation_recall=1.0000
