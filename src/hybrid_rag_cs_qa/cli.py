from __future__ import annotations

import argparse
from pathlib import Path

from .dataset_builder import build_expanded_dataset
from .data import load_chunks, load_qa
from .evaluate import evaluate
from .generation import evaluate_generation
from .graph_rag import GraphExpander
from .llm import print_llm_status
from .pipeline import RagPipeline
from .raptor_builder import RaptorTreeBuilder
from .raptor_retriever import RaptorRetriever
from .raptor_store import save_raptor_tree
from .reranker import FeatureReranker
from .retrievers import BM25Retriever, DenseRetriever, rrf_fuse
from .showcase import build_showcase


ROOT = Path(__file__).resolve().parents[2]
CORPUS = ROOT / "data" / "raw" / "cs_courses_expanded.md"
QA = ROOT / "data" / "qa" / "eval_qa_expanded.jsonl"
LEGACY_CORPUS = ROOT / "data" / "raw" / "cs_courses.md"
LEGACY_QA = ROOT / "data" / "qa" / "eval_qa.jsonl"
RERANKER = ROOT / "artifacts" / "reranker.joblib"
RAPTOR_TREE = ROOT / "artifacts" / "raptor_tree.json"
RESULTS = ROOT / "reports" / "experiment_results.json"


def main() -> None:
    parser = argparse.ArgumentParser(description="Hybrid RAG CS QA experiments")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("build-expanded-dataset")
    sub.add_parser("prepare")
    sub.add_parser("build-raptor-tree")
    sub.add_parser("train-reranker")
    sub.add_parser("evaluate")
    sub.add_parser("build-showcase")
    sub.add_parser("check-llm")
    gen_eval = sub.add_parser("evaluate-generation")
    gen_eval.add_argument("--method", default="graph_raptor_pruned")
    gen_eval.add_argument("--top-k", type=int, default=3)
    gen_eval.add_argument("--adaptive-top-k", action="store_true")
    gen_eval.add_argument("--multi-hop-top-k", type=int, default=None)
    gen_eval.add_argument("--generator", default="extractive", choices=["extractive", "openai-compatible", "ollama", "llm"])
    gen_eval.add_argument("--limit", type=int, default=None)
    gen_eval.add_argument("--out", default=None)
    ask = sub.add_parser("ask")
    ask.add_argument("question")
    ask.add_argument("--method", default="graph_raptor_pruned")
    ask.add_argument("--generator", default="extractive", choices=["extractive", "openai-compatible", "ollama", "llm"])
    args = parser.parse_args()

    if args.command == "build-expanded-dataset":
        docs, qa_items = build_expanded_dataset(CORPUS, QA)
        print(f"Saved expanded corpus to {CORPUS}")
        print(f"Saved expanded QA to {QA}")
        print(f"Documents: {docs}")
        print(f"QA items: {qa_items}")
    elif args.command == "prepare":
        chunks = load_chunks(CORPUS)
        qa_items = load_qa(QA)
        pipeline = RagPipeline(CORPUS, reranker_path=RERANKER)
        print(f"Loaded {len(chunks)} chunks and {len(qa_items)} QA items.")
        print(f"Dense backend: {pipeline.dense.backend}")
        if pipeline.dense.backend == "sentence_transformers":
            print(f"Embedding model: {pipeline.dense.model_name}")
        for chunk in chunks[:3]:
            print(f"- {chunk.id}: {chunk.title} concepts={','.join(chunk.concepts)}")
    elif args.command == "build-raptor-tree":
        chunks = load_chunks(CORPUS)
        tree = RaptorTreeBuilder().build(chunks)
        save_raptor_tree(tree, RAPTOR_TREE)
        print(f"Saved RAPTOR tree to {RAPTOR_TREE}")
        print(f"Nodes: {len(tree.nodes)}")
        print(f"Leaves: {len(tree.leaf_ids)}")
        print(f"Roots: {len(tree.root_ids)}")
        print(f"Layers: {sorted(tree.layer_to_node_ids)}")
    elif args.command == "train-reranker":
        chunks = load_chunks(CORPUS)
        qa_items = load_qa(QA)
        bm25 = BM25Retriever(chunks)
        dense = DenseRetriever(chunks)
        graph = GraphExpander(chunks)
        raptor_tree = RaptorTreeBuilder().build(chunks)
        raptor = RaptorRetriever(chunks, raptor_tree)
        candidate_sets = {
            item.id: rrf_fuse(
                [
                    bm25.search(item.question, top_k=30),
                    dense.search(item.question, top_k=30),
                    graph.expand(item.question, top_k=30),
                    raptor.search(item.question, top_k=30),
                ],
                top_k=30,
            )
            for item in qa_items
        }
        FeatureReranker().fit_from_candidates(qa_items, candidate_sets, chunks).save(RERANKER)
        print(f"Saved reranker to {RERANKER}")
    elif args.command == "evaluate":
        report = evaluate(CORPUS, QA, RERANKER, RESULTS)
        print(f"Saved results to {RESULTS}")
        for method, metrics in report.items():
            print(method, {k: v for k, v in metrics.items() if k not in {"examples", "groups", "rows"}})
    elif args.command == "evaluate-generation":
        out_path = Path(args.out) if args.out else ROOT / "reports" / "generation_results.json"
        report = evaluate_generation(
            CORPUS,
            QA,
            RERANKER,
            out_path,
            method=args.method,
            top_k=args.top_k,
            generator=args.generator,
            limit=args.limit,
            adaptive_top_k=args.adaptive_top_k,
            multi_hop_top_k=args.multi_hop_top_k,
        )
        print(f"Saved generation results to {out_path}")
        print({k: v for k, v in report.items() if k not in {"groups", "rows"}})
    elif args.command == "build-showcase":
        paths = build_showcase(RESULTS, ROOT / "reports" / "generation_results.json", ROOT / "reports")
        for name, path in paths.items():
            print(f"{name}: {path}")
    elif args.command == "check-llm":
        print_llm_status()
    elif args.command == "ask":
        pipeline = RagPipeline(CORPUS, reranker_path=RERANKER)
        result = pipeline.answer_extractive(args.question, method=args.method, generator=args.generator)
        print(result)


if __name__ == "__main__":
    main()
