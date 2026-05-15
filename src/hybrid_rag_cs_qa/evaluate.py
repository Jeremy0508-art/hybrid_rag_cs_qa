from __future__ import annotations

import json
import math
from collections import defaultdict
from pathlib import Path

from .data import load_qa
from .pipeline import RagPipeline


METHODS = (
    "naive",
    "hybrid",
    "hybrid_rerank",
    "graph_reflect",
    "graph_pruned",
    "raptor",
    "raptor_topdown",
    "hybrid_raptor",
    "graph_raptor_pruned",
)


def evaluate(corpus_path: Path, qa_path: Path, reranker_path: Path, out_path: Path, top_k: int = 5) -> dict:
    pipeline = RagPipeline(corpus_path, reranker_path=reranker_path)
    qa_items = load_qa(qa_path)
    report: dict[str, dict] = {}
    for method in METHODS:
        rows = []
        for item in qa_items:
            results = pipeline.search(item.question, method=method, top_k=top_k)
            retrieved = [r.chunk.id for r in results]
            gold_ids = list(item.evidence_ids)
            gold = set(gold_ids)
            rows.append(
                {
                    "id": item.id,
                    "question": item.question,
                    "topic": item.topic,
                    "subtopic": item.subtopic,
                    "difficulty": item.difficulty,
                    "type": item.question_type,
                    "requires_multi_hop": item.requires_multi_hop,
                    "expected_concepts": list(item.expected_concepts),
                    "answer_style": item.answer_style,
                    "retrieved": retrieved,
                    "gold": gold_ids,
                    "recall": recall_at_k(retrieved, gold),
                    "mrr": mrr(retrieved, gold),
                    "ndcg": ndcg(retrieved, gold),
                    "context_precision": context_precision(retrieved, gold),
                }
            )
        report[method] = summarize(rows)
        report[method]["groups"] = summarize_groups(rows)
        report[method]["examples"] = rows[:3]
        report[method]["rows"] = rows
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    write_markdown_report(report, out_path.with_suffix(".md"))
    write_error_analysis(report, out_path.with_name("error_analysis.md"))
    return report


def recall_at_k(retrieved: list[str], gold: set[str]) -> float:
    return len(set(retrieved) & gold) / len(gold) if gold else 0.0


def mrr(retrieved: list[str], gold: set[str]) -> float:
    for idx, cid in enumerate(retrieved, start=1):
        if cid in gold:
            return 1 / idx
    return 0.0


def ndcg(retrieved: list[str], gold: set[str]) -> float:
    dcg = sum((1 / math.log2(i + 2)) for i, cid in enumerate(retrieved) if cid in gold)
    ideal = sum(1 / math.log2(i + 2) for i in range(min(len(gold), len(retrieved))))
    return dcg / ideal if ideal else 0.0


def context_precision(retrieved: list[str], gold: set[str]) -> float:
    if not retrieved:
        return 0.0
    return len(set(retrieved) & gold) / len(retrieved)


def summarize(rows: list[dict]) -> dict:
    if not rows:
        return {"recall": 0.0, "mrr": 0.0, "ndcg": 0.0, "context_precision": 0.0, "num_questions": 0}
    keys = ("recall", "mrr", "ndcg", "context_precision")
    return {
        key: round(sum(row[key] for row in rows) / len(rows), 4)
        for key in keys
    } | {"num_questions": len(rows)}


def summarize_groups(rows: list[dict]) -> dict[str, dict[str, dict]]:
    return {
        "by_topic": _summarize_by(rows, "topic"),
        "by_difficulty": _summarize_by(rows, "difficulty"),
        "by_type": _summarize_by(rows, "type"),
        "by_multi_hop": _summarize_by(rows, "requires_multi_hop"),
        "by_answer_style": _summarize_by(rows, "answer_style"),
    }


def _summarize_by(rows: list[dict], key: str) -> dict[str, dict]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        grouped[str(row.get(key, "unknown"))].append(row)
    return {
        group: summarize(group_rows)
        for group, group_rows in sorted(grouped.items(), key=lambda item: item[0])
    }


def write_markdown_report(report: dict, path: Path) -> None:
    lines = [
        "# Hybrid RAG Experiment Report",
        "",
        "## Metrics",
        "",
        "| Method | Recall@5 | MRR | NDCG | Context Precision |",
        "|---|---:|---:|---:|---:|",
    ]
    for method, metrics in report.items():
        lines.append(
            f"| {method} | {metrics['recall']:.4f} | {metrics['mrr']:.4f} | "
            f"{metrics['ndcg']:.4f} | {metrics['context_precision']:.4f} |"
        )
    lines.extend(["", "## Grouped Metrics", ""])
    lines.extend(_group_table(report, "by_topic", "Topic"))
    lines.extend(["", ""])
    lines.extend(_group_table(report, "by_type", "Question Type"))
    lines.extend(["", ""])
    lines.extend(_group_table(report, "by_difficulty", "Difficulty"))
    lines.extend(["", ""])
    lines.extend(_group_table(report, "by_multi_hop", "Requires Multi-hop"))
    lines.extend(["", ""])
    lines.extend(_group_table(report, "by_answer_style", "Answer Style"))
    lines.extend(
        [
            "",
            "## Preliminary Conclusion",
            "",
            "GraphRAG-style expansion is expected to improve recall on concept-related or multi-hop questions, "
            "but may reduce context precision when graph neighbors introduce noisy evidence. "
            "The error analysis file lists concrete cases for follow-up refinement.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _group_table(report: dict, group_key: str, label: str) -> list[str]:
    lines = [
        f"### {label}",
        "",
        f"| {label} | Method | Questions | Recall@5 | MRR | NDCG | Context Precision |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for method, metrics in report.items():
        groups = metrics.get("groups", {}).get(group_key, {})
        for group, group_metrics in groups.items():
            lines.append(
                f"| {group} | {method} | {group_metrics['num_questions']} | "
                f"{group_metrics['recall']:.4f} | {group_metrics['mrr']:.4f} | "
                f"{group_metrics['ndcg']:.4f} | {group_metrics['context_precision']:.4f} |"
            )
    return lines


def write_error_analysis(report: dict, path: Path) -> None:
    naive_rows = {row["id"]: row for row in report.get("naive", {}).get("rows", [])}
    hybrid_rows = {row["id"]: row for row in report.get("hybrid", {}).get("rows", [])}
    rerank_rows = {row["id"]: row for row in report.get("hybrid_rerank", {}).get("rows", [])}
    graph_rows = {row["id"]: row for row in report.get("graph_reflect", {}).get("rows", [])}
    pruned_rows = {row["id"]: row for row in report.get("graph_pruned", {}).get("rows", [])}

    improvements = []
    regressions = []
    noisy_graph = []
    reranker_wins = []
    pruned_precision_wins = []
    misses = []

    for qid, graph in graph_rows.items():
        naive = naive_rows.get(qid)
        hybrid = hybrid_rows.get(qid)
        rerank = rerank_rows.get(qid)
        if naive and graph["recall"] > naive["recall"]:
            improvements.append((qid, naive, graph))
        if naive and graph["recall"] < naive["recall"]:
            regressions.append((qid, naive, graph))
        if graph["recall"] >= 1.0 and graph["context_precision"] < 0.4:
            noisy_graph.append((qid, graph))
        if hybrid and rerank and rerank["mrr"] > hybrid["mrr"]:
            reranker_wins.append((qid, hybrid, rerank))
        pruned = pruned_rows.get(qid)
        if pruned and pruned["recall"] >= graph["recall"] and pruned["context_precision"] > graph["context_precision"]:
            pruned_precision_wins.append((qid, graph, pruned))
        if graph["recall"] < 1.0:
            misses.append((qid, graph))

    lines = [
        "# Error Analysis",
        "",
        "This analysis compares per-question retrieval behavior across methods.",
        "",
        "## GraphRAG Improvements Over Naive",
        "",
    ]
    lines.extend(_case_lines(improvements[:10], "naive", "graph"))
    lines.extend(["", "## GraphRAG Regressions", ""])
    lines.extend(_case_lines(regressions[:10], "naive", "graph"))
    lines.extend(["", "## Noisy Graph Expansions", ""])
    for qid, row in noisy_graph[:10]:
        lines.extend(
            [
                f"- `{qid}` {row['question']}",
                f"  - gold: {', '.join(row['gold'])}",
                f"  - retrieved: {', '.join(row['retrieved'])}",
                f"  - context_precision: {row['context_precision']:.4f}",
            ]
        )
    lines.extend(["", "## Reranker Wins Over Hybrid", ""])
    lines.extend(_case_lines(reranker_wins[:10], "hybrid", "rerank"))
    lines.extend(["", "## Pruned GraphRAG Precision Wins", ""])
    lines.extend(_case_lines(pruned_precision_wins[:10], "graph", "pruned"))
    lines.extend(["", "## Remaining Misses", ""])
    for qid, row in misses[:10]:
        lines.extend(
            [
                f"- `{qid}` {row['question']}",
                f"  - gold: {', '.join(row['gold'])}",
                f"  - retrieved: {', '.join(row['retrieved'])}",
                f"  - recall: {row['recall']:.4f}",
            ]
        )
    path.write_text("\n".join(lines), encoding="utf-8")


def _case_lines(cases: list[tuple], left_name: str, right_name: str) -> list[str]:
    if not cases:
        return ["No cases found."]
    lines: list[str] = []
    for qid, left, right in cases:
        lines.extend(
            [
                f"- `{qid}` {right['question']}",
                f"  - gold: {', '.join(right['gold'])}",
                f"  - {left_name}: recall={left['recall']:.4f}, mrr={left['mrr']:.4f}, retrieved={', '.join(left['retrieved'])}",
                f"  - {right_name}: recall={right['recall']:.4f}, mrr={right['mrr']:.4f}, retrieved={', '.join(right['retrieved'])}",
            ]
        )
    return lines
