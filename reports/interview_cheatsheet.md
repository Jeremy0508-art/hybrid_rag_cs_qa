# Interview Cheatsheet

## 30 秒介绍

我做了一个面向计算机课程问答的 Hybrid Self-Reflective GraphRAG 系统。项目包含 34 个课程知识点和 100 条标注问答，比较了 Naive RAG、Hybrid RAG、reranker、GraphRAG 和证据压缩版 GraphRAG。核心结果是：GraphRAG 明显提升召回，但会引入噪声；我进一步加入证据压缩，在几乎保持召回的同时把 Context Precision 从 0.4140 提升到 0.6450。

## 为什么不是普通 RAG

普通 RAG 主要依赖向量相似度，在专业课程里容易漏掉精确术语和多跳概念。我的系统加入 BM25 + dense retrieval 的混合检索，用图谱扩展概念关系，再用 reranker 和证据压缩控制噪声。

## 最重要的实验结论

Graph + Reflection RAG 的 Recall@5 是 0.9400，说明图扩展有效；但 Context Precision 只有 0.4140。Graph + Pruning RAG 的 Recall@5 仍有 0.9367，同时 Context Precision 提升到 0.6450，说明主要矛盾从“召不回来”变成了“如何筛干净”。

## 可能被问到的问题

Q: 为什么 hybrid 没明显超过 naive？
A: 当前 dense retriever 还是 TF-IDF baseline，语料规模也比较小，BM25 和 TF-IDF 的信号有重叠。后续接 BGE/E5 embedding 后，hybrid 的互补性会更明显。

Q: 为什么 Citation Accuracy 不是特别高？
A: GraphRAG 为了提高召回会返回相邻概念证据，部分证据主题相关但不直接支持答案。证据压缩已经把 Citation Accuracy 提升到 0.6450，后续可以用 CrossEncoder reranker 继续优化。

Q: 项目的创新点是什么？
A: 不是单纯做 RAG demo，而是围绕课程问答构建了可复现实验闭环：混合检索、概念图扩展、hard-negative reranker、证据压缩、检索评测和生成评测。

## 简历 bullet

独立完成面向计算机课程问答的 Hybrid Self-Reflective GraphRAG 系统，构建 34 个课程知识点与 100 条标注问答评测集；设计 BM25 + dense retrieval + RRF 融合检索、概念图谱扩展检索、hard-negative 重排序与证据压缩流程，将 Recall@5 从 0.7500 提升到 0.9367，并将 GraphRAG Context Precision 从 0.4140 提升到 0.6450。
