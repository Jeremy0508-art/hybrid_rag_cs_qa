# Error Analysis

This analysis compares per-question retrieval behavior across methods.

## GraphRAG Improvements Over Naive

- `q1` 为什么线程切换通常比进程切换开销更低？
  - gold: os-进程与线程
  - naive: recall=0.0000, mrr=0.0000, retrieved=
  - graph: recall=1.0000, mrr=1.0000, retrieved=os-进程与线程, os-cpu-调度算法, os-虚拟内存与页面置换, os-死锁与银行家算法, os-同步互斥与信号量
- `q2` 互斥锁、信号量和管程分别适合解决什么并发问题？
  - gold: os-同步互斥与信号量
  - naive: recall=0.0000, mrr=0.0000, retrieved=ai-rag-检索增强生成
  - graph: recall=1.0000, mrr=1.0000, retrieved=os-同步互斥与信号量, ai-rag-检索增强生成, os-死锁与银行家算法, os-进程与线程, os-cpu-调度算法
- `q27` 图着色寄存器分配中为什么活跃区间冲突的变量不能使用同一寄存器？
  - gold: compiler-寄存器分配
  - naive: recall=0.0000, mrr=0.0000, retrieved=
  - graph: recall=1.0000, mrr=1.0000, retrieved=compiler-寄存器分配, compiler-中间代码与活跃变量
- `q39` 快照读和事务隔离级别之间有什么关系？
  - gold: db-隔离级别与并发异常, db-mvcc-与快照读
  - naive: recall=0.0000, mrr=0.0000, retrieved=
  - graph: recall=1.0000, mrr=1.0000, retrieved=db-隔离级别与并发异常, db-mvcc-与快照读, db-事务与-acid
- `q41` 从正则表达式到词法分析器通常经历什么转换链路？
  - gold: compiler-正则表达式-nfa-与-dfa
  - naive: recall=0.0000, mrr=0.0000, retrieved=
  - graph: recall=1.0000, mrr=1.0000, retrieved=compiler-正则表达式-nfa-与-dfa, compiler-词法分析与语法分析, compiler-lr分析
- `q48` 为什么日志文件系统有助于崩溃恢复？
  - gold: os-文件系统与-inode
  - naive: recall=0.0000, mrr=0.0000, retrieved=
  - graph: recall=1.0000, mrr=1.0000, retrieved=os-文件系统与-inode
- `q51` 进程拥有独立地址空间这一点会如何影响上下文切换成本？
  - gold: os-进程与线程
  - naive: recall=0.0000, mrr=0.0000, retrieved=ai-重排序与-hard-negative
  - graph: recall=1.0000, mrr=1.0000, retrieved=os-进程与线程, os-cpu-调度算法, os-虚拟内存与页面置换, os-死锁与银行家算法, ai-重排序与-hard-negative
- `q52` 条件变量为什么通常和管程一起出现？
  - gold: os-同步互斥与信号量
  - naive: recall=0.0000, mrr=0.0000, retrieved=
  - graph: recall=1.0000, mrr=1.0000, retrieved=os-同步互斥与信号量, os-进程与线程, net-三次握手与四次挥手, os-死锁与银行家算法
- `q53` 破坏死锁的循环等待条件可以怎样避免死锁？
  - gold: os-死锁与银行家算法
  - naive: recall=0.0000, mrr=0.0000, retrieved=
  - graph: recall=1.0000, mrr=1.0000, retrieved=os-死锁与银行家算法, os-进程与线程, os-cpu-调度算法, os-同步互斥与信号量, os-虚拟内存与页面置换
- `q64` 路由聚合和子网划分之间有什么关系？
  - gold: net-子网划分
  - naive: recall=0.0000, mrr=0.0000, retrieved=
  - graph: recall=1.0000, mrr=1.0000, retrieved=net-子网划分, net-ip-路由与-nat, net-dns-解析过程

## GraphRAG Regressions

No cases found.

## Noisy Graph Expansions

- `q1` 为什么线程切换通常比进程切换开销更低？
  - gold: os-进程与线程
  - retrieved: os-进程与线程, os-cpu-调度算法, os-虚拟内存与页面置换, os-死锁与银行家算法, os-同步互斥与信号量
  - context_precision: 0.2000
- `q2` 互斥锁、信号量和管程分别适合解决什么并发问题？
  - gold: os-同步互斥与信号量
  - retrieved: os-同步互斥与信号量, ai-rag-检索增强生成, os-死锁与银行家算法, os-进程与线程, os-cpu-调度算法
  - context_precision: 0.2000
- `q3` 死锁产生需要哪些必要条件，银行家算法如何避免死锁？
  - gold: os-死锁与银行家算法
  - retrieved: os-死锁与银行家算法, os-进程与线程, os-cpu-调度算法, os-同步互斥与信号量, os-虚拟内存与页面置换
  - context_precision: 0.2000
- `q4` LRU 页面置换为什么能利用程序局部性？
  - gold: os-虚拟内存与页面置换
  - retrieved: os-虚拟内存与页面置换, os-页表与-tlb, os-进程与线程, os-cpu-调度算法, os-死锁与银行家算法
  - context_precision: 0.2000
- `q8` TCP 和 UDP 在可靠性和延迟方面有什么区别？
  - gold: net-tcp-与-udp
  - retrieved: net-tcp-与-udp, net-三次握手与四次挥手, ai-rag-评测指标, net-http-https-与-tls, net-dns-解析过程
  - context_precision: 0.2000
- `q9` TCP 为什么建立连接需要三次握手？
  - gold: net-三次握手与四次挥手
  - retrieved: net-三次握手与四次挥手, net-tcp-与-udp, net-http-https-与-tls, net-dns-解析过程, os-进程与线程
  - context_precision: 0.2000
- `q10` 滑动窗口和拥塞控制分别解决什么问题？
  - gold: net-拥塞控制与滑动窗口
  - retrieved: net-tcp-与-udp, net-拥塞控制与滑动窗口, os-进程与线程, ai-bm25-与向量检索, net-dns-解析过程
  - context_precision: 0.2000
- `q11` DNS 递归解析通常会经过哪些服务器？
  - gold: net-dns-解析过程
  - retrieved: net-dns-解析过程, net-tcp-与-udp, net-ip-路由与-nat, net-http-https-与-tls, net-三次握手与四次挥手
  - context_precision: 0.2000
- `q12` HTTPS 相比 HTTP 额外提供了哪些安全能力？
  - gold: net-http-https-与-tls
  - retrieved: net-http-https-与-tls, net-三次握手与四次挥手, net-tcp-与-udp
  - context_precision: 0.3333
- `q13` NAT 为什么会影响端到端连接模型？
  - gold: net-ip-路由与-nat
  - retrieved: net-ip-路由与-nat, net-子网划分, net-dns-解析过程
  - context_precision: 0.3333

## Reranker Wins Over Hybrid

- `q10` 滑动窗口和拥塞控制分别解决什么问题？
  - gold: net-拥塞控制与滑动窗口
  - hybrid: recall=1.0000, mrr=0.3333, retrieved=net-tcp-与-udp, ai-bm25-与向量检索, net-拥塞控制与滑动窗口, os-进程与线程
  - rerank: recall=1.0000, mrr=0.5000, retrieved=net-tcp-与-udp, net-拥塞控制与滑动窗口, os-进程与线程, ai-bm25-与向量检索
- `q38` 最长前缀匹配在路由选择中解决什么问题？
  - gold: net-ip-路由与-nat
  - hybrid: recall=1.0000, mrr=0.5000, retrieved=ai-rag-检索增强生成, net-ip-路由与-nat
  - rerank: recall=1.0000, mrr=1.0000, retrieved=net-ip-路由与-nat, ai-rag-检索增强生成
- `q97` 普通 RAG、GraphRAG 和 Self-RAG 分别缓解什么问题？
  - gold: ai-知识图谱与-graphrag, ai-self-rag-与反思检索, ai-rag-检索增强生成
  - hybrid: recall=1.0000, mrr=0.5000, retrieved=ai-rag-评测指标, ai-rag-检索增强生成, ai-self-rag-与反思检索, ai-知识图谱与-graphrag, ai-lora-与轻量微调
  - rerank: recall=1.0000, mrr=1.0000, retrieved=ai-rag-检索增强生成, ai-rag-评测指标, ai-self-rag-与反思检索, ai-知识图谱与-graphrag, ai-lora-与轻量微调

## Pruned GraphRAG Precision Wins

- `q1` 为什么线程切换通常比进程切换开销更低？
  - gold: os-进程与线程
  - graph: recall=1.0000, mrr=1.0000, retrieved=os-进程与线程, os-cpu-调度算法, os-虚拟内存与页面置换, os-死锁与银行家算法, os-同步互斥与信号量
  - pruned: recall=1.0000, mrr=1.0000, retrieved=os-进程与线程, os-cpu-调度算法, os-虚拟内存与页面置换
- `q2` 互斥锁、信号量和管程分别适合解决什么并发问题？
  - gold: os-同步互斥与信号量
  - graph: recall=1.0000, mrr=1.0000, retrieved=os-同步互斥与信号量, ai-rag-检索增强生成, os-死锁与银行家算法, os-进程与线程, os-cpu-调度算法
  - pruned: recall=1.0000, mrr=1.0000, retrieved=os-同步互斥与信号量, ai-rag-检索增强生成, os-死锁与银行家算法
- `q3` 死锁产生需要哪些必要条件，银行家算法如何避免死锁？
  - gold: os-死锁与银行家算法
  - graph: recall=1.0000, mrr=1.0000, retrieved=os-死锁与银行家算法, os-进程与线程, os-cpu-调度算法, os-同步互斥与信号量, os-虚拟内存与页面置换
  - pruned: recall=1.0000, mrr=1.0000, retrieved=os-死锁与银行家算法
- `q4` LRU 页面置换为什么能利用程序局部性？
  - gold: os-虚拟内存与页面置换
  - graph: recall=1.0000, mrr=1.0000, retrieved=os-虚拟内存与页面置换, os-页表与-tlb, os-进程与线程, os-cpu-调度算法, os-死锁与银行家算法
  - pruned: recall=1.0000, mrr=1.0000, retrieved=os-虚拟内存与页面置换
- `q5` TLB 为什么可以降低虚拟地址转换开销？
  - gold: os-页表与-tlb
  - graph: recall=1.0000, mrr=1.0000, retrieved=os-页表与-tlb, os-虚拟内存与页面置换
  - pruned: recall=1.0000, mrr=1.0000, retrieved=os-页表与-tlb
- `q8` TCP 和 UDP 在可靠性和延迟方面有什么区别？
  - gold: net-tcp-与-udp
  - graph: recall=1.0000, mrr=1.0000, retrieved=net-tcp-与-udp, net-三次握手与四次挥手, ai-rag-评测指标, net-http-https-与-tls, net-dns-解析过程
  - pruned: recall=1.0000, mrr=1.0000, retrieved=net-tcp-与-udp, net-三次握手与四次挥手, ai-rag-评测指标
- `q9` TCP 为什么建立连接需要三次握手？
  - gold: net-三次握手与四次挥手
  - graph: recall=1.0000, mrr=1.0000, retrieved=net-三次握手与四次挥手, net-tcp-与-udp, net-http-https-与-tls, net-dns-解析过程, os-进程与线程
  - pruned: recall=1.0000, mrr=1.0000, retrieved=net-三次握手与四次挥手, net-tcp-与-udp, net-http-https-与-tls
- `q10` 滑动窗口和拥塞控制分别解决什么问题？
  - gold: net-拥塞控制与滑动窗口
  - graph: recall=1.0000, mrr=0.5000, retrieved=net-tcp-与-udp, net-拥塞控制与滑动窗口, os-进程与线程, ai-bm25-与向量检索, net-dns-解析过程
  - pruned: recall=1.0000, mrr=0.5000, retrieved=net-tcp-与-udp, net-拥塞控制与滑动窗口, os-进程与线程
- `q11` DNS 递归解析通常会经过哪些服务器？
  - gold: net-dns-解析过程
  - graph: recall=1.0000, mrr=1.0000, retrieved=net-dns-解析过程, net-tcp-与-udp, net-ip-路由与-nat, net-http-https-与-tls, net-三次握手与四次挥手
  - pruned: recall=1.0000, mrr=1.0000, retrieved=net-dns-解析过程, net-tcp-与-udp
- `q12` HTTPS 相比 HTTP 额外提供了哪些安全能力？
  - gold: net-http-https-与-tls
  - graph: recall=1.0000, mrr=1.0000, retrieved=net-http-https-与-tls, net-三次握手与四次挥手, net-tcp-与-udp
  - pruned: recall=1.0000, mrr=1.0000, retrieved=net-http-https-与-tls

## Remaining Misses

- `q43` 寄存器不足时编译器通常如何处理变量？
  - gold: compiler-寄存器分配
  - retrieved: compiler-中间代码与活跃变量
  - recall: 0.0000
- `q47` 如果问题包含精确术语“BCNF”，稀疏检索为什么可能有优势？
  - gold: db-范式与函数依赖, ai-bm25-与向量检索
  - retrieved: db-范式与函数依赖
  - recall: 0.5000
- `q75` 变量未声明属于哪一类编译错误检查？
  - gold: compiler-语义分析与类型检查
  - retrieved: 
  - recall: 0.0000
- `q77` 变量溢出到内存通常发生在什么情况下？
  - gold: compiler-寄存器分配
  - retrieved: 
  - recall: 0.0000
- `q81` 图路径扩展为什么可能带来无关证据？
  - gold: ai-知识图谱与-graphrag
  - retrieved: 
  - recall: 0.0000
- `q95` 符号表为什么会同时影响语义分析和后续代码生成？
  - gold: compiler-中间代码与活跃变量, compiler-语义分析与类型检查
  - retrieved: compiler-语义分析与类型检查, ai-rag-检索增强生成
  - recall: 0.5000
- `q100` 为什么轻量微调在本项目中优先作用于检索模块而不是生成模块？
  - gold: ai-重排序与-hard-negative, ai-lora-与轻量微调
  - retrieved: 
  - recall: 0.0000