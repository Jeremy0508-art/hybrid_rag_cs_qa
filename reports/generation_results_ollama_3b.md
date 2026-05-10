# Generation Evaluation Report

- Method: `graph_pruned`
- Generator: `ollama`
- Used generators: `ollama`
- Top-k evidence: `3`
- Questions: `10`
- Limit: `10`

## Metrics

| Metric | Score |
|---|---:|
| Faithfulness | 0.3378 |
| Answer Coverage | 0.2383 |
| Citation Accuracy | 0.6666 |
| Citation Recall | 1.0000 |

## Sample Outputs

### q1

- Question: 为什么线程切换通常比进程切换开销更低？
- Generated: [os-进程与线程] 线程共享地址空间和文件句柄，减少了切换时需要管理的资源。 [os-进程与线程] 线程切换涉及的操作较少，因此开销较低。
- Gold: 线程共享同一进程的地址空间和资源，因此切换时不需要像进程切换那样更换完整资源上下文。
- Citations: os-进程与线程, os-cpu-调度算法, os-虚拟内存与页面置换
- Scores: faithfulness=0.1579, coverage=0.1000, citation_accuracy=0.3333, citation_recall=1.0000

### q2

- Question: 互斥锁、信号量和管程分别适合解决什么并发问题？
- Generated: 互斥锁适合解决竞态条件问题；信号量适用于更复杂的资源计数约束问题；管程通过条件变量实现等待与通知，适合复杂同步操作。 [os-同步互斥与信号量]
- Gold: 互斥锁用于保护临界区，信号量适合描述资源计数约束，管程把共享数据和操作封装起来并通过条件变量实现等待通知。
- Citations: os-同步互斥与信号量, ai-rag-检索增强生成, os-死锁与银行家算法
- Scores: faithfulness=0.0556, coverage=0.0714, citation_accuracy=0.3333, citation_recall=1.0000

### q3

- Question: 死锁产生需要哪些必要条件，银行家算法如何避免死锁？
- Generated: 死锁产生需要互斥、请求并保持、不可剥夺、循环等待四个必要条件 [os-死锁与银行家算法]
银行家算法通过检查系统是否存在安全序列来决定是否分配资源，从而避免系统进入不安全状态 [os-死锁与银行家算法]
- Gold: 死锁需要互斥、请求并保持、不可剥夺和循环等待。银行家算法通过安全性检查，只在系统仍存在安全序列时分配资源。
- Citations: os-死锁与银行家算法
- Scores: faithfulness=0.7200, coverage=0.3571, citation_accuracy=1.0000, citation_recall=1.0000

### q4

- Question: LRU 页面置换为什么能利用程序局部性？
- Generated: LRU 页面置换算法优先淘汰最长时间未被访问的页面 [os-虚拟内存与页面置换]
程序局部性意味着最近使用的页面更有可能在未来继续使用 [os-虚拟内存与页面置换]
- Gold: LRU 淘汰最长时间未被访问的页面，假设近期未访问的页面近期继续被访问的概率较低，因此符合时间局部性。
- Citations: os-虚拟内存与页面置换
- Scores: faithfulness=0.4545, coverage=0.3571, citation_accuracy=1.0000, citation_recall=1.0000

### q5

- Question: TLB 为什么可以降低虚拟地址转换开销？
- Generated: TLB 是页表项的高速缓存。[os-页表与-tlb]
TLB 可以显著降低地址转换开销。[os-页表与-tlb]
未命中时需要重新访问页表，增加额外开销。[os-页表与-tlb]
若页表项无效还可能触发缺页中断，进一步增加开销。[os-页表与-tlb]
- Gold: TLB 缓存常用页表项，命中时无需再次访问页表，因此能减少地址转换所需的内存访问次数。
- Citations: os-页表与-tlb
- Scores: faithfulness=0.4839, coverage=0.0909, citation_accuracy=1.0000, citation_recall=1.0000
