# Dataset Expansion Plan

## Target

Upgrade the current small CS QA corpus into a mature evaluation corpus that can
stress-test naive RAG, hybrid retrieval, GraphRAG, RAPTOR tree retrieval,
reranking, and citation-aware generation.

## Corpus Scale

| Phase | Documents | Fine-grained chunks | QA items |
|---|---:|---:|---:|
| Phase 1 - previous | 150 | 150 coarse course documents | 750 |
| Phase 2 - current | 360 | 360 section-level course documents | 3,600 |
| Phase 3 | 500+ | 1,500+ fine-grained chunks | 5,000+ |

## Topic Coverage

- Operating systems: process/thread, memory, scheduling, filesystems, deadlock,
  synchronization, virtual memory, I/O.
- Computer networks: TCP/UDP, congestion control, DNS, HTTP/TLS, routing, NAT,
  subnetting, reliability.
- Databases: transactions, isolation, indexing, MVCC, query optimization,
  normalization, distributed databases.
- Compilers: lexical analysis, parsing, semantic analysis, IR, optimization,
  register allocation.
- Information retrieval and RAG: BM25, dense retrieval, hybrid retrieval, RRF,
  reranking, GraphRAG, RAPTOR, Self-RAG, evaluation.
- Machine learning foundations: embeddings, representation learning, contrastive
  learning, model adaptation, LoRA.

## QA Types

- Factual definition questions.
- Comparison questions.
- Multi-hop reasoning questions.
- Concept-linking questions that require graph expansion.
- Hierarchical summary questions that should benefit from RAPTOR.
- Citation-sensitive questions where every claim needs evidence.
- Negative and misconception-correction questions.

## Required QA Metadata

Each QA row should eventually include:

- `id`
- `question`
- `answer`
- `evidence_ids`
- `topic`
- `subtopic`
- `difficulty`
- `type`
- `expected_concepts`
- `requires_multi_hop`
- `answer_style`
- optional `negative_evidence_ids`

## Acceptance Criteria

- Every evidence id resolves to a chunk.
- Every topic has at least 50 QA items by Phase 2.
- At least 25% of QA items require multiple evidence chunks.
- At least 20% of QA items are designed for summary-level or hierarchical
  retrieval.
- Evaluation reports are grouped by method, topic, difficulty, and question type.

## Current Phase 2 Status

- Complete: `data/raw/cs_courses_expanded.md` contains 360 course documents.
- Complete: `data/qa/eval_qa_expanded.jsonl` contains 3,600 QA items.
- Complete: QA metadata includes topic, subtopic, expected concepts,
  multi-hop flag, and answer style.
- Complete: QA now covers definition, mechanism, comparison, application,
  misconception, diagnostic, hierarchical summary, concept linking, multi-hop,
  and multi-hop paraphrase questions.
- Complete: retrieval and generation reports include grouped evaluation.
- Next: rerun retrieval and generation evaluations on the 3,600-item benchmark,
  then decide whether Phase 3 should add more real course material or finer
  chunk-level annotations.
