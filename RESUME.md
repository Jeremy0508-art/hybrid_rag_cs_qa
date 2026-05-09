# Resume Materials

## 中文简历 Bullet

独立完成面向计算机课程问答的 Hybrid Self-Reflective GraphRAG 系统，构建 34 个课程知识点与 100 条标注问答评测集；设计 BM25 + dense retrieval + RRF 融合检索、概念图谱扩展检索、hard-negative 重排序与证据压缩流程，将 Recall@5 从 0.7500 提升到 0.9367，并将 GraphRAG Context Precision 从 0.4140 提升到 0.6450；进一步设计 Faithfulness、Citation Accuracy、Citation Recall 等生成质量评测指标，完成完整实验报告与错误案例分析。

## English Resume Bullet

Built a Hybrid Self-Reflective GraphRAG system for computer science course QA with 34 knowledge chunks and 100 annotated QA examples. Designed a BM25 + dense retrieval + RRF pipeline, concept-graph expansion, hard-negative reranking, and evidence pruning, improving Recall@5 from 0.7500 to 0.9367 and GraphRAG Context Precision from 0.4140 to 0.6450. Implemented retrieval and generation evaluation with MRR, NDCG, Faithfulness, Citation Accuracy, and Citation Recall.

## 30 秒项目介绍

我做了一个面向计算机课程问答的 Hybrid Self-Reflective GraphRAG 系统。这个项目不是单纯的聊天机器人，而是一个可复现实验系统：我构建了 34 个课程知识点和 100 条标注问答，比较普通 RAG、混合检索、重排序、GraphRAG 和证据压缩版 GraphRAG。实验发现 GraphRAG 能把 Recall@5 从 0.7500 提升到 0.9400，但会引入噪声；因此我加入证据压缩模块，在几乎保持召回率的同时把 Context Precision 从 0.4140 提升到 0.6450。

## 2 分钟项目介绍

这个项目的动机是，计算机课程问答里有很多精确术语和跨章节概念，比如 MVCC 和隔离级别、NFA/DFA 和词法分析、GraphRAG 和 Citation Accuracy。普通向量 RAG 容易因为语义漂移或分块边界漏召回关键证据。

我的系统分成四层。第一层是 BM25 + dense retrieval 的混合检索，用 RRF 融合精确匹配和语义相似。第二层是课程概念图谱，从文本中抽取概念并建立共现关系，用 GraphRAG 扩展多跳候选证据。第三层是 hard-negative reranker，在初召回候选集中学习区分表面相关但不支持答案的负样本。第四层是证据压缩，针对 GraphRAG 引入噪声的问题，只保留更少、更高置信的证据块。

实验上，我构建了 100 条 QA 评测集，指标包括 Recall@5、MRR、NDCG、Context Precision，以及生成侧的 Faithfulness、Citation Accuracy 和 Citation Recall。结果显示，GraphRAG 明显提升召回，但降低上下文精度；加入证据压缩后，Recall@5 仍保持 0.9367，同时 Context Precision 提升到 0.6450。这个结果说明，课程问答 RAG 的关键不只是召回更多证据，还要控制证据边界和引用质量。

## 面试可强调的创新点

- 不是只做 RAG demo，而是构建了数据、方法、评测、错误分析的完整实验闭环。
- 针对课程问答特点，同时处理精确术语检索和多跳概念关联。
- 发现 GraphRAG 的高召回与低精度矛盾，并设计证据压缩模块缓解。
- 同时评估检索质量和生成引用质量，结果更适合科研项目汇报。
