from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from .data import slug


@dataclass(frozen=True)
class TopicSpec:
    course: str
    title: str
    concepts: tuple[str, ...]
    definition: str
    mechanism: str
    tradeoff: str
    example: str


ASPECTS = (
    ("Foundations", "defines the core vocabulary and the baseline mental model."),
    ("Mechanisms", "explains the internal steps and the conditions that make the idea work."),
    ("Tradeoffs", "compares benefits, costs, failure modes, and design alternatives."),
    ("Applications", "connects the idea to realistic engineering and exam-style scenarios."),
    ("Evaluation", "describes how to judge whether the idea has been applied correctly."),
)


TOPICS: tuple[TopicSpec, ...] = (
    TopicSpec(
        "Operating Systems",
        "Process and Thread Management",
        ("process", "thread", "context switch", "scheduler"),
        "A process owns an address space and operating system resources, while a thread is the schedulable execution unit inside a process.",
        "The kernel records process control blocks, thread state, registers, stacks, and scheduling metadata to pause and resume execution.",
        "Threads reduce switching overhead because they share memory, but shared memory also increases synchronization risk.",
        "A browser may isolate tabs as processes while using multiple threads inside each tab for rendering, networking, and scripting.",
    ),
    TopicSpec(
        "Operating Systems",
        "Synchronization and Mutual Exclusion",
        ("mutex", "semaphore", "monitor", "condition variable"),
        "Synchronization coordinates concurrent execution so that shared data remains consistent.",
        "Mutexes guard critical sections, semaphores count available resources, and monitors combine protected state with wait and notify operations.",
        "Coarse locks are simple but reduce concurrency; fine-grained locks improve throughput but increase deadlock and debugging complexity.",
        "A bounded buffer commonly uses a mutex plus two condition variables to coordinate producers and consumers.",
    ),
    TopicSpec(
        "Operating Systems",
        "Deadlock and Resource Allocation",
        ("deadlock", "banker algorithm", "safe sequence", "resource allocation"),
        "Deadlock is a state where tasks wait forever because each task holds a resource needed by another task.",
        "Deadlock analysis checks mutual exclusion, hold and wait, no preemption, and circular wait; the banker algorithm admits requests only if a safe sequence remains.",
        "Avoidance can preserve safety but requires maximum demand information that is not always available.",
        "A database worker pool can deadlock if every worker holds one lock and waits for another lock in a cycle.",
    ),
    TopicSpec(
        "Operating Systems",
        "Virtual Memory and Page Replacement",
        ("virtual memory", "page table", "TLB", "LRU", "page fault"),
        "Virtual memory gives each process a logical address space that is translated to physical memory.",
        "The MMU uses page tables and the TLB to translate addresses; a page fault loads missing data from secondary storage.",
        "LRU exploits temporal locality but exact LRU is expensive, so systems often use approximations.",
        "When physical frames are scarce, a replacement policy chooses which page to evict before bringing in the faulting page.",
    ),
    TopicSpec(
        "Operating Systems",
        "CPU Scheduling",
        ("scheduling", "round robin", "priority", "starvation"),
        "CPU scheduling chooses which ready task should run next.",
        "Schedulers estimate fairness, response time, throughput, and priority while reacting to blocking and time-slice expiration.",
        "Shortest-job policies improve average waiting time but can starve long jobs; round robin improves responsiveness but adds switching overhead.",
        "Interactive systems often prefer time slicing so users see progress even when many processes are runnable.",
    ),
    TopicSpec(
        "Operating Systems",
        "File Systems and Journaling",
        ("file system", "inode", "journal", "crash recovery"),
        "A file system organizes persistent data, metadata, directories, and allocation structures.",
        "Inode-like structures store metadata and block pointers, while journals record intended metadata updates before applying them.",
        "Journaling improves crash recovery but adds write overhead and does not automatically protect application-level consistency.",
        "After a power loss, the file system replays or rolls back journal entries to restore a consistent metadata state.",
    ),
    TopicSpec(
        "Computer Networks",
        "TCP and UDP Transport",
        ("TCP", "UDP", "reliability", "flow control"),
        "TCP provides reliable ordered byte streams, while UDP provides lightweight datagram delivery without reliability guarantees.",
        "TCP uses sequence numbers, acknowledgments, retransmission, flow control, and congestion control.",
        "TCP is safer for correctness-sensitive transfers; UDP is better when low latency matters and the application can handle loss.",
        "Video calls often use UDP because late packets may be less useful than fresh packets.",
    ),
    TopicSpec(
        "Computer Networks",
        "TCP Handshake and Connection Teardown",
        ("SYN", "ACK", "three-way handshake", "four-way close"),
        "TCP uses a three-way handshake to establish a connection and synchronize sequence numbers.",
        "The client sends SYN, the server replies SYN-ACK, and the client confirms with ACK; teardown usually closes each direction independently.",
        "The handshake prevents stale duplicate segments from being mistaken for a new connection but adds latency before data transfer.",
        "HTTPS connections may combine TCP setup with TLS setup unless connection reuse or newer protocols reduce the cost.",
    ),
    TopicSpec(
        "Computer Networks",
        "Congestion Control",
        ("congestion control", "slow start", "AIMD", "fast retransmit"),
        "Congestion control prevents senders from overwhelming the network.",
        "TCP estimates congestion through acknowledgments, loss, and timing, then adjusts the congestion window.",
        "Aggressive growth improves utilization but can increase packet loss; conservative growth protects stability but may underuse capacity.",
        "After packet loss, TCP often reduces its window and then gradually probes for available bandwidth.",
    ),
    TopicSpec(
        "Computer Networks",
        "DNS Resolution",
        ("DNS", "recursive resolver", "cache", "TTL"),
        "DNS maps domain names to resource records such as IP addresses.",
        "A resolver may query root, top-level domain, and authoritative servers, then cache results according to TTL.",
        "Caching reduces latency and load but stale or poisoned records can misdirect clients.",
        "A browser usually asks a local resolver before it can open a connection to a web server by domain name.",
    ),
    TopicSpec(
        "Computer Networks",
        "HTTP HTTPS and TLS",
        ("HTTP", "HTTPS", "TLS", "certificate"),
        "HTTP is an application protocol for request-response resource transfer; HTTPS protects HTTP with TLS.",
        "TLS authenticates the server, negotiates keys, and protects confidentiality and integrity.",
        "Encryption improves security but increases handshake and certificate-validation work.",
        "A client validates the server certificate chain before trusting that it is communicating with the intended site.",
    ),
    TopicSpec(
        "Computer Networks",
        "Routing NAT and Subnetting",
        ("IP", "routing", "NAT", "subnet", "longest prefix match"),
        "Network-layer forwarding moves packets across networks using addresses and routing tables.",
        "Routers use longest-prefix match to choose next hops; NAT rewrites addresses and ports at network boundaries.",
        "NAT conserves public addresses but complicates end-to-end connectivity and inbound connections.",
        "Subnetting reduces broadcast scope and lets administrators allocate address blocks by organizational need.",
    ),
    TopicSpec(
        "Databases",
        "Transactions and ACID",
        ("transaction", "ACID", "atomicity", "durability"),
        "A transaction groups operations into a unit that should behave consistently despite failures and concurrency.",
        "Atomicity rolls back partial work, consistency preserves constraints, isolation controls interference, and durability preserves committed results.",
        "Stronger guarantees simplify application logic but may reduce concurrency or increase logging cost.",
        "A bank transfer should debit one account and credit another account atomically.",
    ),
    TopicSpec(
        "Databases",
        "Isolation Levels and Anomalies",
        ("isolation", "dirty read", "non-repeatable read", "phantom read", "serializable"),
        "Isolation levels define which concurrent effects a transaction may observe.",
        "Lower levels allow more anomalies, while serializable isolation makes concurrent execution equivalent to some serial order.",
        "Strict isolation improves correctness but can increase blocking, aborts, or coordination overhead.",
        "A reporting transaction can see inconsistent totals if it reads data while another transaction is partially updating rows.",
    ),
    TopicSpec(
        "Databases",
        "Index Structures",
        ("B+ tree", "hash index", "range query", "selectivity"),
        "Indexes accelerate lookup by storing search keys in auxiliary structures.",
        "B+ trees support ordered traversal and range queries, while hash indexes target equality lookup.",
        "Indexes speed reads but consume storage and slow writes because index entries must be maintained.",
        "A query filtering by a highly selective user id can benefit from an index on that column.",
    ),
    TopicSpec(
        "Databases",
        "MVCC and Snapshot Reads",
        ("MVCC", "snapshot", "version", "visibility"),
        "MVCC keeps multiple versions so readers and writers can proceed with less blocking.",
        "A transaction reads versions visible according to its snapshot and commit timestamps.",
        "MVCC improves read concurrency but needs version cleanup and careful conflict handling.",
        "Snapshot isolation lets a long analytical query read a stable view while updates continue.",
    ),
    TopicSpec(
        "Databases",
        "Query Optimization",
        ("query optimizer", "join order", "cost model", "predicate pushdown"),
        "A query optimizer chooses an execution plan that should return the same result with lower cost.",
        "The optimizer estimates cardinalities, access paths, join orders, and operator costs.",
        "Cost estimates can be wrong when statistics are stale or predicates are correlated.",
        "Predicate pushdown filters rows early so later joins process less data.",
    ),
    TopicSpec(
        "Compilers",
        "Lexical and Syntax Analysis",
        ("lexer", "parser", "token", "grammar"),
        "Lexical analysis turns characters into tokens, and syntax analysis checks token sequences against grammar rules.",
        "Lexers often use finite automata, while parsers build parse trees or abstract syntax trees.",
        "A simple grammar is easier to parse but may require later semantic checks to express language rules.",
        "A compiler reports a syntax error when tokens cannot match any valid production.",
    ),
    TopicSpec(
        "Compilers",
        "LL and LR Parsing",
        ("LL", "LR", "FIRST", "FOLLOW", "shift reduce"),
        "LL parsers predict productions top-down, while LR parsers recognize handles bottom-up.",
        "LL parsing relies on FIRST and FOLLOW sets; LR parsing uses states, ACTION tables, and GOTO tables.",
        "LL parsers are simple and readable, while LR parsers handle a broader class of grammars.",
        "Expression grammars with precedence are often easier to support with LR-family techniques.",
    ),
    TopicSpec(
        "Compilers",
        "Semantic Analysis and Type Checking",
        ("semantic analysis", "type checking", "symbol table", "scope"),
        "Semantic analysis checks meaning after syntax has been accepted.",
        "The compiler tracks declarations, scopes, types, and function signatures in symbol tables.",
        "Static type checks catch errors early but can reject programs that would run safely under dynamic checks.",
        "Calling a function with the wrong number of arguments is usually detected during semantic analysis.",
    ),
    TopicSpec(
        "Compilers",
        "Intermediate Representation and Data Flow",
        ("IR", "three-address code", "data flow", "liveness"),
        "Intermediate representation is a compiler-internal program form used for analysis and optimization.",
        "Data-flow analysis propagates facts across control-flow graph edges until a fixed point is reached.",
        "Richer IR makes optimization easier but can increase compiler complexity.",
        "Liveness analysis determines whether a variable value may be used later.",
    ),
    TopicSpec(
        "Compilers",
        "Register Allocation",
        ("register allocation", "graph coloring", "spill", "interference graph"),
        "Register allocation maps many program values onto a limited set of machine registers.",
        "Graph coloring treats simultaneously live variables as interfering nodes that cannot share a register.",
        "Good allocation improves performance, while spilling adds memory traffic.",
        "If too many variables are live at once, the allocator spills some values to the stack.",
    ),
    TopicSpec(
        "Information Retrieval",
        "BM25 and Sparse Retrieval",
        ("BM25", "term frequency", "inverse document frequency", "sparse retrieval"),
        "BM25 is a lexical retrieval method based on term matching and document-frequency weighting.",
        "It rewards query terms that appear in a document while normalizing for document length.",
        "BM25 handles exact terminology well but struggles with paraphrases and semantic matches.",
        "A query containing an exact protocol name such as TCP is often well served by BM25.",
    ),
    TopicSpec(
        "Information Retrieval",
        "Dense Retrieval and Embeddings",
        ("embedding", "vector search", "semantic similarity", "contrastive learning"),
        "Dense retrieval maps queries and documents into vectors so semantic similarity can be computed.",
        "Embedding models learn representations where related meanings tend to have nearby vectors.",
        "Dense retrieval handles paraphrases but may miss exact rare terms or produce plausible semantic drift.",
        "A question about reliable transport may retrieve a TCP passage even if the word TCP is absent.",
    ),
    TopicSpec(
        "Information Retrieval",
        "Hybrid Retrieval and RRF",
        ("hybrid retrieval", "RRF", "rank fusion", "candidate generation"),
        "Hybrid retrieval combines complementary retrievers such as BM25 and dense search.",
        "Reciprocal rank fusion adds rank-based scores from several result lists without requiring calibrated raw scores.",
        "Fusion improves robustness but can introduce noise if one retriever returns many off-topic candidates.",
        "A production RAG system often uses sparse and dense candidates before reranking.",
    ),
    TopicSpec(
        "Information Retrieval",
        "Reranking and Hard Negatives",
        ("reranker", "hard negative", "cross encoder", "feature model"),
        "Reranking reorders retrieved candidates using a more precise relevance model.",
        "Hard negatives are retrieved passages that look similar to the query but do not support the answer.",
        "Reranking improves top-k precision but adds latency and depends on representative training data.",
        "A hard-negative course passage may mention GraphRAG but not explain the asked failure mode.",
    ),
    TopicSpec(
        "RAG Systems",
        "GraphRAG Retrieval",
        ("GraphRAG", "knowledge graph", "concept graph", "multi-hop"),
        "GraphRAG uses explicit relationships between concepts, entities, or chunks to expand retrieval.",
        "A graph retriever can follow concept co-occurrence or entity links to find neighboring evidence.",
        "Graph expansion improves recall for multi-hop questions but can reduce context precision when neighbors are noisy.",
        "A question about deadlock prevention may expand from deadlock to resource allocation and safe sequence.",
    ),
    TopicSpec(
        "RAG Systems",
        "RAPTOR Tree Retrieval",
        ("RAPTOR", "summary tree", "recursive summarization", "hierarchical retrieval"),
        "RAPTOR builds a hierarchy of summaries over document chunks so retrieval can operate at multiple abstraction levels.",
        "Leaf chunks are clustered, summarized into parent nodes, embedded, and recursively summarized into higher layers.",
        "Summary nodes help broad questions but can hide details, so final answers should cite original leaf evidence.",
        "A broad question about retrieval failure modes may first match a summary node and then expand to detailed child chunks.",
    ),
    TopicSpec(
        "RAG Systems",
        "Self-RAG and Faithfulness",
        ("Self-RAG", "faithfulness", "citation", "reflection"),
        "Self-RAG adds checks that decide whether retrieval is sufficient and whether generated claims are supported.",
        "Reflection can trigger another retrieval pass, reject unsupported evidence, or ask the generator to cite specific chunks.",
        "Reflection reduces hallucination risk but can add complexity and may over-retrieve if thresholds are poorly tuned.",
        "A citation-aware answer should attach evidence ids to claims that come from retrieved context.",
    ),
    TopicSpec(
        "RAG Systems",
        "RAG Evaluation Metrics",
        ("Recall@k", "MRR", "NDCG", "context precision", "citation accuracy"),
        "RAG evaluation measures both retrieval quality and generation quality.",
        "Recall@k checks whether gold evidence was retrieved, MRR and NDCG judge ranking, and citation metrics judge evidence use.",
        "A method can improve recall while lowering context precision if it returns extra irrelevant chunks.",
        "Graph expansion may retrieve all gold evidence plus noisy neighbors, so both recall and precision must be reported.",
    ),
)


def build_expanded_dataset(corpus_path: Path, qa_path: Path) -> tuple[int, int]:
    documents = _build_documents()
    qa_items = _build_qa_items(documents)

    corpus_path.parent.mkdir(parents=True, exist_ok=True)
    qa_path.parent.mkdir(parents=True, exist_ok=True)

    corpus_path.write_text("\n\n".join(document["markdown"] for document in documents) + "\n", encoding="utf-8")
    qa_path.write_text(
        "\n".join(json.dumps(item, ensure_ascii=False) for item in qa_items) + "\n",
        encoding="utf-8",
    )
    return len(documents), len(qa_items)


def _build_documents() -> list[dict[str, object]]:
    documents: list[dict[str, object]] = []
    for topic in TOPICS:
        for aspect, aspect_note in ASPECTS:
            title = f"{topic.title} {aspect}"
            chunk_id = f"{slug(topic.course)}-{slug(title)}"
            body = (
                f"{topic.definition} {topic.mechanism} {topic.tradeoff} {topic.example} "
                f"The {aspect.lower()} view of {topic.title} {aspect_note} "
                f"Important concepts include {', '.join(topic.concepts)}. "
                f"In a RAG benchmark, this passage should be treated as evidence for questions about "
                f"{topic.title}, especially when the question asks about {aspect.lower()}."
            )
            documents.append(
                {
                    "id": chunk_id,
                    "course": topic.course,
                    "title": title,
                    "topic": topic,
                    "aspect": aspect,
                    "markdown": f"## {topic.course} / {title}\n{body}",
                }
            )
    return documents


def _build_qa_items(documents: list[dict[str, object]]) -> list[dict[str, object]]:
    qa_items: list[dict[str, object]] = []
    for index, document in enumerate(documents):
        topic = document["topic"]
        assert isinstance(topic, TopicSpec)
        evidence_id = str(document["id"])
        next_document = documents[(index + 1) % len(documents)]
        next_topic = next_document["topic"]
        assert isinstance(next_topic, TopicSpec)

        qa_items.extend(
            [
                _qa(
                    index,
                    1,
                    f"What is the core idea of {document['title']}?",
                    topic.definition,
                    [evidence_id],
                    topic,
                    document["aspect"],
                    "definition",
                    "easy",
                    False,
                ),
                _qa(
                    index,
                    2,
                    f"How does {document['title']} work internally?",
                    topic.mechanism,
                    [evidence_id],
                    topic,
                    document["aspect"],
                    "mechanism",
                    "medium",
                    False,
                ),
                _qa(
                    index,
                    3,
                    f"What tradeoff should be considered for {document['title']}?",
                    topic.tradeoff,
                    [evidence_id],
                    topic,
                    document["aspect"],
                    "comparison",
                    "medium",
                    False,
                ),
                _qa(
                    index,
                    4,
                    f"Why might {document['title']} and {next_document['title']} both matter in a RAG-style system?",
                    f"{topic.example} {next_topic.example}",
                    [evidence_id, str(next_document["id"])],
                    topic,
                    document["aspect"],
                    "multi_hop",
                    "hard",
                    True,
                    "title-explicit",
                ),
                _qa(
                    index,
                    5,
                    (
                        f"Why would the {str(document['aspect']).lower()} perspective on {topic.concepts[0]} "
                        f"and the {str(next_document['aspect']).lower()} perspective on {next_topic.concepts[0]} "
                        "need to be combined when answering a grounded systems question?"
                    ),
                    f"{topic.example} {next_topic.example}",
                    [evidence_id, str(next_document["id"])],
                    topic,
                    document["aspect"],
                    "multi_hop_paraphrase",
                    "hard",
                    True,
                    "paraphrase",
                ),
            ]
        )
    return qa_items


def _qa(
    doc_index: int,
    variant: int,
    question: str,
    answer: str,
    evidence_ids: list[str],
    topic: TopicSpec,
    aspect: object,
    question_type: str,
    difficulty: str,
    requires_multi_hop: bool,
    answer_style: str = "citation-grounded",
) -> dict[str, object]:
    return {
        "id": f"expanded-q{doc_index + 1:03d}-{variant}",
        "question": question,
        "answer": answer,
        "evidence_ids": evidence_ids,
        "difficulty": difficulty,
        "type": question_type,
        "topic": topic.course,
        "subtopic": topic.title,
        "aspect": str(aspect),
        "expected_concepts": list(topic.concepts),
        "requires_multi_hop": requires_multi_hop,
        "answer_style": answer_style,
    }
