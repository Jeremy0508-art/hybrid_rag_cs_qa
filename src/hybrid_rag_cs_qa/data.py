from __future__ import annotations

import json
import re
from pathlib import Path

from .schema import Chunk, QAItem


CONCEPTS = (
    "进程", "线程", "上下文切换", "同步", "互斥", "信号量", "管程", "死锁", "银行家算法",
    "安全序列", "虚拟内存", "页表", "TLB", "缺页中断", "页面置换", "LRU", "FIFO",
    "调度算法", "时间片轮转", "优先级调度", "文件系统", "inode", "日志文件系统",
    "TCP", "UDP", "三次握手", "四次挥手", "拥塞控制", "滑动窗口", "慢启动", "快速重传",
    "DNS", "HTTP", "HTTPS", "TLS", "网络层", "IP", "路由", "NAT", "子网划分",
    "事务", "ACID", "隔离级别", "脏读", "不可重复读", "幻读", "索引", "B+树",
    "哈希索引", "两阶段锁", "MVCC", "范式", "函数依赖", "关系代数", "查询优化",
    "词法分析", "语法分析", "LL分析", "LR分析", "语义分析", "中间代码", "三地址码",
    "活跃变量", "数据流分析", "寄存器分配", "DFA", "NFA", "正则表达式",
    "RAG", "BM25", "向量检索", "RRF", "重排序", "知识图谱", "GraphRAG", "Self-RAG",
    "幻觉", "忠实度", "Recall@k", "MRR", "NDCG", "LoRA", "对比学习", "hard negative",
)

ENGLISH_CONCEPTS = (
    "process", "thread", "context switch", "scheduler", "mutex", "semaphore", "monitor",
    "condition variable", "deadlock", "banker algorithm", "safe sequence",
    "resource allocation", "virtual memory", "page table", "TLB", "LRU", "page fault",
    "scheduling", "round robin", "priority", "starvation", "file system", "inode",
    "journal", "crash recovery", "TCP", "UDP", "reliability", "flow control", "SYN",
    "ACK", "three-way handshake", "four-way close", "congestion control", "slow start",
    "AIMD", "fast retransmit", "DNS", "recursive resolver", "cache", "TTL", "HTTP",
    "HTTPS", "TLS", "certificate", "IP", "routing", "NAT", "subnet",
    "longest prefix match", "transaction", "ACID", "atomicity", "durability",
    "isolation", "dirty read", "non-repeatable read", "phantom read", "serializable",
    "B+ tree", "hash index", "range query", "selectivity", "MVCC", "snapshot",
    "version", "visibility", "query optimizer", "join order", "cost model",
    "predicate pushdown", "lexer", "parser", "token", "grammar", "LL", "LR", "FIRST",
    "FOLLOW", "shift reduce", "semantic analysis", "type checking", "symbol table",
    "scope", "IR", "three-address code", "data flow", "liveness", "register allocation",
    "graph coloring", "spill", "interference graph", "BM25", "term frequency",
    "inverse document frequency", "sparse retrieval", "embedding", "vector search",
    "semantic similarity", "contrastive learning", "hybrid retrieval", "RRF",
    "rank fusion", "candidate generation", "reranker", "hard negative", "cross encoder",
    "feature model", "GraphRAG", "knowledge graph", "concept graph", "multi-hop",
    "RAPTOR", "summary tree", "recursive summarization", "hierarchical retrieval",
    "Self-RAG", "faithfulness", "citation", "reflection", "Recall@k", "MRR", "NDCG",
    "context precision", "citation accuracy",
)

ALL_CONCEPTS = tuple(dict.fromkeys(CONCEPTS + ENGLISH_CONCEPTS))


def extract_concepts(text: str) -> tuple[str, ...]:
    lower = text.lower()
    return tuple(c for c in ALL_CONCEPTS if _concept_in_text(c, lower))


def _concept_in_text(concept: str, lower_text: str) -> bool:
    lower_concept = concept.lower()
    if re.fullmatch(r"[a-z0-9+#.-]+(?:\s+[a-z0-9+#.-]+)*", lower_concept):
        pattern = r"(?<![a-z0-9+#.-])" + re.escape(lower_concept) + r"(?![a-z0-9+#.-])"
        return re.search(pattern, lower_text) is not None
    return lower_concept in lower_text


def load_chunks(path: Path) -> list[Chunk]:
    raw = path.read_text(encoding="utf-8")
    sections = re.split(r"\n(?=## )", raw)
    chunks: list[Chunk] = []
    for section in sections:
        lines = [line.strip() for line in section.splitlines() if line.strip()]
        if not lines or not lines[0].startswith("## "):
            continue
        header = lines[0].removeprefix("## ").strip()
        course, _, title = header.partition(" / ")
        body = " ".join(lines[1:])
        cid = f"{slug(course)}-{slug(title)}"
        chunks.append(
            Chunk(
                id=cid,
                course=course,
                title=title or course,
                text=body,
                concepts=extract_concepts(f"{header} {body}"),
            )
        )
    return chunks


def load_qa(path: Path) -> list[QAItem]:
    items: list[QAItem] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        obj = json.loads(line)
        items.append(
            QAItem(
                id=obj["id"],
                question=obj["question"],
                answer=obj["answer"],
                evidence_ids=tuple(obj["evidence_ids"]),
                difficulty=obj.get("difficulty", "medium"),
                question_type=obj.get("type", "unknown"),
                topic=obj.get("topic", "unknown"),
                subtopic=obj.get("subtopic", "unknown"),
                expected_concepts=tuple(obj.get("expected_concepts", [])),
                requires_multi_hop=bool(obj.get("requires_multi_hop", False)),
                answer_style=obj.get("answer_style", "unknown"),
            )
        )
    return items


def slug(text: str) -> str:
    mapping = {
        "操作系统": "os",
        "计算机网络": "net",
        "数据库": "db",
        "编译原理": "compiler",
        "人工智能": "ai",
    }
    text = mapping.get(text, text)
    text = re.sub(r"[^A-Za-z0-9\u4e00-\u9fff]+", "-", text).strip("-")
    return text.lower()
