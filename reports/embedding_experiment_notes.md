# Embedding Backend Experiment Notes

## 当前状态

项目已经支持两种 dense retriever 后端：

| 后端 | 启用方式 | 说明 |
|---|---|---|
| TF-IDF | 默认 | 轻量、可复现、无需下载模型 |
| sentence-transformers | 设置环境变量 | 可使用 BGE/E5 等真实 embedding 模型 |

## 启用 BGE

```powershell
pip install -r requirements-embeddings.txt
$env:CS_RAG_DENSE_BACKEND="sentence-transformers"
$env:CS_RAG_EMBEDDING_MODEL="BAAI/bge-small-zh-v1.5"
cs-rag prepare
cs-rag train-reranker
cs-rag evaluate
```

## 本次运行记录

当前环境已成功安装 `sentence-transformers`，但首次加载 `BAAI/bge-small-zh-v1.5` 时需要从 HuggingFace 下载模型文件，下载超过 10 分钟后超时。主实验结果因此仍采用默认 TF-IDF dense retriever。

这不影响项目代码能力：如果本地已有模型缓存，或配置 HuggingFace 镜像/代理，系统会自动切换到 sentence-transformers 后端。

## 可选解决方案

1. 使用网络更稳定的环境预先下载 `BAAI/bge-small-zh-v1.5`。
2. 将 `CS_RAG_EMBEDDING_MODEL` 设置为本地模型目录。
3. 尝试更小的多语言模型，例如：

```powershell
$env:CS_RAG_EMBEDDING_MODEL="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
```

4. 若只是复现实验流程，继续使用默认 TF-IDF 后端即可。
