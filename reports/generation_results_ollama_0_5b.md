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
| Faithfulness | 0.7251 |
| Answer Coverage | 0.3151 |
| Citation Accuracy | 0.6666 |
| Citation Recall | 1.0000 |

## Sample Outputs

### q1

- Question: 为什么线程切换通常比进程切换开销更低？
- Generated: 线程切换通常比进程切换开销更低；共享内存也会引入同步问题；CPU 调度算法决定就绪进程获得处理器的顺序；先来先服务实现简单但可能导致短作业等待过长。
- Gold: 线程共享同一进程的地址空间和资源，因此切换时不需要像进程切换那样更换完整资源上下文。
- Citations: os-进程与线程, os-cpu-调度算法, os-虚拟内存与页面置换
- Scores: faithfulness=0.8421, coverage=0.0000, citation_accuracy=0.3333, citation_recall=1.0000

### q2

- Question: 互斥锁、信号量和管程分别适合解决什么并发问题？
- Generated: 互斥锁适合解决并发程序中多个线程访问共享变量时可能产生的竞态条件；信号量可以描述更一般的资源计数约束；管程把共享数据和操作封装在一起，并通过条件变量实现等待与通知。
- Gold: 互斥锁用于保护临界区，信号量适合描述资源计数约束，管程把共享数据和操作封装起来并通过条件变量实现等待通知。
- Citations: os-同步互斥与信号量, ai-rag-检索增强生成, os-死锁与银行家算法
- Scores: faithfulness=0.6667, coverage=0.3571, citation_accuracy=0.3333, citation_recall=1.0000

### q3

- Question: 死锁产生需要哪些必要条件，银行家算法如何避免死锁？
- Generated: [死锁产生需要互斥、请求并保持、不可剥夺、循环等待四个必要条件]；银行家算法通过检查系统是否存在安全序列来决定是否分配资源，从而避免系统进入不安全状态。
- Gold: 死锁需要互斥、请求并保持、不可剥夺和循环等待。银行家算法通过安全性检查，只在系统仍存在安全序列时分配资源。
- Citations: os-死锁与银行家算法
- Scores: faithfulness=0.9474, coverage=0.3571, citation_accuracy=1.0000, citation_recall=1.0000

### q4

- Question: LRU 页面置换为什么能利用程序局部性？
- Generated: LRU 页面置换算法通过优先淘汰最长时间未被访问的页面来利用程序局部性。[os-虚拟内存与页面置换] 课程：操作系统；标题：虚拟内存与页面置换 chunk-id: os-虚拟内存与页面置换与虚拟内存与页面置换章节]
- Gold: LRU 淘汰最长时间未被访问的页面，假设近期未访问的页面近期继续被访问的概率较低，因此符合时间局部性。
- Citations: os-虚拟内存与页面置换
- Scores: faithfulness=0.2222, coverage=0.0714, citation_accuracy=1.0000, citation_recall=1.0000

### q5

- Question: TLB 为什么可以降低虚拟地址转换开销？
- Generated: TLB可以降低虚拟地址转换开销，因为它能够显著减少访问页表的次数，从而减少了地址转换的开销。[os-页表与-tlb]课程：操作系统；标题：页表与 TLB

TLB未命中时需要重新访问页表，若页表项无效还可能触发缺页中断。[os-页表与-tlb]课程：操作系统；标题：页表与 TLB

页表保存虚拟页到物理页框的映射，地址转换需要访问页表。[os-页表与-tlb]课程：操作系统；标题：页表与 TLB
- Gold: TLB 缓存常用页表项，命中时无需再次访问页表，因此能减少地址转换所需的内存访问次数。
- Citations: os-页表与-tlb
- Scores: faithfulness=0.4000, coverage=0.0909, citation_accuracy=1.0000, citation_recall=1.0000
