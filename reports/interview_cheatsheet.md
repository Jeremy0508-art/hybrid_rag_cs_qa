# Interview Cheatsheet

## 30 秒介绍

我做了一个面向计算机课程问答的成熟 RAG 实验系统。项目从原来的基础 RAG 扩展到 360 个课程文档和 3,600 条标注 QA，覆盖普通事实问答、改写问法、摘要型问题、概念连接和多跳问题。系统实现了 BM25 + dense 混合检索、GraphRAG 概念扩展、RAPTOR summary tree、Hybrid RAPTOR 融合检索、证据压缩和自适应生成预算。3,600 QA 评估中，RAPTOR collapsed retrieval 的 Recall@5 达到 0.9960；面向生成的 `graph_raptor_pruned` 在压缩最终证据上下文的同时，在生成评估中达到 0.9930 Faithfulness 和 0.8351 Citation Recall。

## 为什么不是普通 RAG

普通 RAG 主要依赖 chunk 级相似度，面对课程问答里的概念改写、多跳线索和跨章节关联时容易漏召回。这个项目同时引入三类补充信号：BM25 保留术语精确匹配，RAPTOR summary tree 提供层次化语义摘要，GraphRAG 提供概念邻接扩展。最后再用证据压缩控制噪声，避免把召回提升直接转化为低质量上下文。

## 最重要实验结论

`raptor` 是整体检索最强方法：Recall@5 = 0.9960，MRR = 0.9972，NDCG = 0.9945。`graph_raptor_pruned` 是更适合生成的折中方案：Recall@5 = 0.9587，MRR = 0.9418，Context Precision = 0.4533。生成侧使用 `graph_raptor_pruned` + adaptive top-k 后，Faithfulness = 0.9930，Answer Coverage = 0.8519，Citation Recall = 0.8351。

## 可被追问的问题

Q: 为什么要引入 RAPTOR？
A: GraphRAG 擅长沿概念关系扩展，但它本身不生成层次化摘要。RAPTOR 可以把底层 chunk 聚类成 summary node，让检索先看到更高层的主题线索，再回落到底层证据，因此更适合处理改写问法和跨 chunk 问题。

Q: 为什么还需要 GraphRAG？
A: RAPTOR 解决的是层次化语义组织，GraphRAG 解决的是显式概念关系。课程问答里很多问题不是同义改写，而是概念之间的依赖或并列关系，所以两者互补。

Q: 为什么 `graph_raptor_pruned` 的 Recall 不如 `hybrid_raptor`？
A: 它是面向生成优化的方法，会主动压缩候选证据，牺牲少量召回换取更干净的上下文。对于最终问答系统，低噪声证据通常比单纯返回更多 chunk 更重要。

Q: RAPTOR 代码是否直接复制参考项目？
A: 没有直接照搬。参考项目用于理解聚类、summary 和树构建思想；主项目重新实现了适配本项目 schema、chunk metadata、评估闭环和 CLI 的版本。这样更容易维护，也不会把参考项目的实验假设硬塞进主项目。

## 简历 bullet

独立构建面向计算机课程问答的 Hybrid GraphRAG + RAPTOR 系统，将数据集扩展到 360 个课程文档和 3,600 条标注 QA；实现 BM25 + dense RRF 融合检索、GraphRAG 概念扩展、RAPTOR summary tree、Hybrid RAPTOR 检索、证据压缩和自适应生成评估，使 RAPTOR 检索在 3,600 QA 上达到 0.9960 Recall@5，并在生成侧达到 0.9930 Faithfulness、0.8519 Answer Coverage 和 0.8351 Citation Recall。
