# Resume Materials

## 中文简历 Bullet

独立构建面向计算机课程问答的 Hybrid GraphRAG + RAPTOR 系统，将数据集扩展到 150 个课程文档和 750 条标注 QA；实现 BM25 + dense RRF 融合检索、GraphRAG 概念扩展、RAPTOR summary tree、Hybrid RAPTOR 检索、证据压缩和自适应生成评估，使整体检索 Recall@5 达到 0.9813，并在生成侧达到 0.9909 Faithfulness、0.9814 Answer Coverage 和 0.9687 Citation Recall。

## English Resume Bullet

Built a Hybrid GraphRAG + RAPTOR system for computer science course QA, expanding the benchmark to 150 course documents and 750 annotated QA examples. Implemented BM25 + dense RRF retrieval, concept-graph expansion, RAPTOR summary-tree construction, Hybrid RAPTOR retrieval, evidence pruning, and adaptive generation evaluation, reaching 0.9813 Recall@5 for retrieval and 0.9909 Faithfulness, 0.9814 Answer Coverage, and 0.9687 Citation Recall for generation.

## 30 秒项目介绍

我做了一个面向计算机课程问答的成熟 RAG 实验系统。项目从原来的基础 RAG 扩展到 150 个课程文档和 750 条标注 QA，覆盖普通事实问答、改写问法和多跳问题。系统实现了 BM25 + dense 混合检索、GraphRAG 概念扩展、RAPTOR summary tree、Hybrid RAPTOR 融合检索、证据压缩和自适应生成预算。当前最强整体检索方法 `hybrid_raptor` 的 Recall@5 达到 0.9813；面向生成的 `graph_raptor_pruned` 在保持 0.9667 Recall@5 的同时提供更高 Context Precision，并在生成评估中达到 0.9909 Faithfulness 和 0.9687 Citation Recall。

## 2 分钟项目介绍

这个项目的动机是，计算机课程问答中经常出现精确术语、概念改写和跨章节多跳线索。普通 RAG 只看 chunk 相似度，容易在改写问题上漏召回，也容易在扩展上下文时引入噪声。

我的系统分为五层。第一层是 BM25 + dense retrieval 的混合检索，用 RRF 融合精确匹配和语义匹配。第二层是课程概念图，用 GraphRAG 补充概念邻接关系。第三层是 RAPTOR summary tree，通过 chunk 聚类和 summary node 递归构建层次化语义索引。第四层是 Hybrid RAPTOR，把普通检索、图扩展和 RAPTOR 候选融合。第五层是证据压缩与自适应生成预算，针对生成任务控制最终上下文噪声。

实验上，我构建了 150 个课程文档和 750 条 QA，指标包括 Recall@5、MRR、NDCG、Context Precision，以及生成侧的 Faithfulness、Answer Coverage、Citation Accuracy 和 Citation Recall。结果显示，`hybrid_raptor` 的 Recall@5 达到 0.9813，是整体最强检索方案；`graph_raptor_pruned` 的 Recall@5 为 0.9667，但 Context Precision 更高，更适合作为最终问答生成入口。

## 面试可强调的创新点

- 不是只做 RAG demo，而是构建了数据、方法、评估、错误分析和展示材料的完整实验闭环。
- 将 RAPTOR 的层次化 summary tree 与 GraphRAG 的显式概念关系结合，分别处理语义组织和概念邻接。
- 对检索和生成分别优化：`hybrid_raptor` 追求整体召回，`graph_raptor_pruned` 追求可引用、低噪声上下文。
- 扩展 QA metadata，支持按 topic、difficulty、type、answer_style、multi_hop 做分组评估。
- 保留可复现 baseline，同时预留 sentence-transformers、LLM summarizer 和本地 Ollama LLM 的升级接口。
