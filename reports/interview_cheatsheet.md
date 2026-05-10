# Interview Cheatsheet

## 30 秒介绍

我做了一个面向计算机课程问答的 Hybrid Self-Reflective GraphRAG 系统。项目包含 34 个课程知识点和 100 条标注问答，比较了 Naive RAG、Hybrid RAG、reranker、GraphRAG 和证据压缩版 GraphRAG。核心结果是：GraphRAG 明显提升召回，但会引入噪声；我进一步加入证据压缩，在几乎保持召回的同时把 Context Precision 从 0.4140 提升到 0.6450。最后我还接入了本地 Ollama Qwen2.5 3B 模型，完成真实 LLM 生成和引用评测。

## 为什么不是普通 RAG

普通 RAG 主要依赖向量相似度，在专业课程里容易漏掉精确术语和多跳概念。我的系统加入 BM25 + dense retrieval 的混合检索，用图谱扩展概念关系，再用 reranker 和证据压缩控制噪声。

## 最重要的实验结论

Graph + Reflection RAG 的 Recall@5 是 0.9400，说明图扩展有效；但 Context Precision 只有 0.4140。Graph + Pruning RAG 的 Recall@5 仍有 0.9367，同时 Context Precision 提升到 0.6450，说明主要矛盾从“召不回来”变成了“如何筛干净”。

## 可能被问到的问题

Q: 为什么 hybrid 没明显超过 naive？
A: 当前 dense retriever 还是 TF-IDF baseline，语料规模也比较小，BM25 和 TF-IDF 的信号有重合。后续接 BGE/E5 embedding 后，hybrid 的互补性会更明显。

Q: 为什么 Citation Accuracy 不是特别高？
A: GraphRAG 为了提高召回会返回相邻概念证据，部分证据主题相关但不直接支持答案。证据压缩已经把 Citation Accuracy 提升到 0.6450，后续可以用 CrossEncoder reranker 继续优化。

Q: 项目的创新点是什么？
A: 不是单纯做 RAG demo，而是围绕课程问答构建了可复现实验闭环：混合检索、概念图扩展、hard-negative reranker、证据压缩、检索评测和生成评测。

Q: 为什么 3B 模型的自动指标不一定比 0.5B 高？
A: 当前 Faithfulness 和 Coverage 主要基于词面重合。0.5B 更容易直接拼接原文片段，所以指标可能更高，但答案会混入无关内容；3B 回答更自然，词面和标准答案不完全一致，因此指标偏低。这个现象说明我没有只看分数，还做了样例级误差分析。

Q: 本地 Ollama 实验说明了什么？
A: 它说明系统已经跑通真实 LLM 端到端链路，不只是抽取式 baseline。同时，0.5B/3B 对比暴露了小模型生成、citation 约束和自动指标之间的差异，为后续换更强模型、改 prompt 或引入 LLM-as-judge 提供依据。

## 简历 bullet

独立完成面向计算机课程问答的 Hybrid Self-Reflective GraphRAG 系统，构建 34 个课程知识点与 100 条标注问答评测集；设计 BM25 + dense retrieval + RRF 融合检索、概念图谱扩展检索、hard-negative 重排序与证据压缩流程，将 Recall@5 从 0.7500 提升到 0.9367，并将 GraphRAG Context Precision 从 0.4140 提升到 0.6450；接入本地 Ollama Qwen2.5 3B 模型，完成真实 LLM 生成、citation 约束与样例误差分析。
