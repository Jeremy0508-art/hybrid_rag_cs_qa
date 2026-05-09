from __future__ import annotations

import json
import re
from pathlib import Path

from .data import load_qa
from .llm import generate_openai_compatible_answer
from .schema import QAItem, SearchResult
from .text import tokenize


SENTENCE_RE = re.compile(r"(?<=[。！？!?])")


def generate_extractive_answer(question: str, results: list[SearchResult], max_sentences: int = 3) -> str:
    scored: list[tuple[float, int, str, str]] = []
    q_tokens = set(tokenize(question))

    for rank, result in enumerate(results):
        sentences = [s.strip() for s in SENTENCE_RE.split(result.chunk.text) if s.strip()]
        chunk_best: tuple[float, int, str, str] | None = None
        for sentence in sentences:
            s_tokens = set(tokenize(sentence))
            title_tokens = set(tokenize(result.chunk.title))
            overlap = len(q_tokens & s_tokens)
            title_bonus = len(q_tokens & title_tokens)
            concept_bonus = sum(1 for concept in result.chunk.concepts if concept in question)
            rank_bonus = 1 / (rank + 1)
            score = overlap + 2.0 * title_bonus + 1.5 * concept_bonus + rank_bonus
            candidate = (score, rank, sentence, result.chunk.id)
            if chunk_best is None or candidate[0] > chunk_best[0]:
                chunk_best = candidate
        if chunk_best is not None:
            scored.append(chunk_best)

    if not scored:
        return "未检索到足够证据，无法给出可靠回答。"

    picked = sorted(scored, key=lambda item: (-item[0], item[1]))[:max_sentences]
    answer_parts = []
    used_sentences: set[str] = set()
    for _, _, sentence, citation in picked:
        if sentence in used_sentences:
            continue
        used_sentences.add(sentence)
        answer_parts.append(f"{sentence} [{citation}]")
    return "".join(answer_parts)


def generate_answer(question: str, results: list[SearchResult], generator: str = "extractive") -> tuple[str, str]:
    if generator in {"openai-compatible", "llm"}:
        llm_answer = generate_openai_compatible_answer(question, results)
        if llm_answer:
            return llm_answer, "openai-compatible"
    return generate_extractive_answer(question, results), "extractive"


def evaluate_generation(
    corpus_path: Path,
    qa_path: Path,
    reranker_path: Path,
    out_path: Path,
    method: str = "graph_pruned",
    top_k: int = 3,
    generator: str = "extractive",
) -> dict:
    from .pipeline import RagPipeline

    pipeline = RagPipeline(corpus_path, reranker_path=reranker_path)
    qa_items = load_qa(qa_path)
    rows = []
    used_generators: set[str] = set()
    for item in qa_items:
        results = pipeline.search(item.question, method=method, top_k=top_k)
        answer, used_generator = generate_answer(item.question, results, generator=generator)
        used_generators.add(used_generator)
        rows.append(score_answer(item, answer, results))

    report = summarize_generation(rows) | {
        "method": method,
        "top_k": top_k,
        "generator": generator,
        "used_generators": sorted(used_generators),
        "num_questions": len(rows),
        "rows": rows,
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    write_generation_report(report, out_path.with_suffix(".md"))
    return report


def score_answer(item: QAItem, answer: str, results: list[SearchResult]) -> dict:
    context = " ".join(result.chunk.text for result in results)
    citations = [result.chunk.id for result in results]
    gold = set(item.evidence_ids)
    return {
        "id": item.id,
        "question": item.question,
        "gold_answer": item.answer,
        "generated_answer": answer,
        "citations": citations,
        "gold_citations": list(gold),
        "faithfulness": faithfulness(answer, context),
        "answer_coverage": answer_coverage(answer, item.answer),
        "citation_accuracy": citation_accuracy(citations, gold),
        "citation_recall": citation_recall(citations, gold),
    }


def faithfulness(answer: str, context: str) -> float:
    answer_tokens = content_tokens(answer)
    context_tokens = set(content_tokens(context))
    if not answer_tokens:
        return 0.0
    supported = [token for token in answer_tokens if token in context_tokens]
    return round(len(supported) / len(answer_tokens), 4)


def answer_coverage(answer: str, gold_answer: str) -> float:
    gold_tokens = content_tokens(gold_answer)
    answer_tokens = set(content_tokens(answer))
    if not gold_tokens:
        return 0.0
    covered = [token for token in gold_tokens if token in answer_tokens]
    return round(len(covered) / len(gold_tokens), 4)


def citation_accuracy(citations: list[str], gold: set[str]) -> float:
    if not citations:
        return 0.0
    return round(len(set(citations) & gold) / len(citations), 4)


def citation_recall(citations: list[str], gold: set[str]) -> float:
    if not gold:
        return 0.0
    return round(len(set(citations) & gold) / len(gold), 4)


def content_tokens(text: str) -> list[str]:
    stopwords = {
        "的", "了", "和", "与", "或", "在", "中", "是", "为", "可以", "通过", "因此",
        "什么", "为什么", "如何", "哪些", "通常", "主要", "分别",
    }
    return [token for token in tokenize(text) if token not in stopwords and len(token.strip()) > 0]


def summarize_generation(rows: list[dict]) -> dict:
    keys = ("faithfulness", "answer_coverage", "citation_accuracy", "citation_recall")
    return {
        key: round(sum(row[key] for row in rows) / len(rows), 4)
        for key in keys
    }


def write_generation_report(report: dict, path: Path) -> None:
    lines = [
        "# Generation Evaluation Report",
        "",
        f"- Method: `{report['method']}`",
        f"- Generator: `{report['generator']}`",
        f"- Used generators: `{', '.join(report['used_generators'])}`",
        f"- Top-k evidence: `{report['top_k']}`",
        f"- Questions: `{report['num_questions']}`",
        "",
        "## Metrics",
        "",
        "| Metric | Score |",
        "|---|---:|",
        f"| Faithfulness | {report['faithfulness']:.4f} |",
        f"| Answer Coverage | {report['answer_coverage']:.4f} |",
        f"| Citation Accuracy | {report['citation_accuracy']:.4f} |",
        f"| Citation Recall | {report['citation_recall']:.4f} |",
        "",
        "## Sample Outputs",
        "",
    ]
    for row in report["rows"][:5]:
        lines.extend(
            [
                f"### {row['id']}",
                "",
                f"- Question: {row['question']}",
                f"- Generated: {row['generated_answer']}",
                f"- Gold: {row['gold_answer']}",
                f"- Citations: {', '.join(row['citations'])}",
                f"- Scores: faithfulness={row['faithfulness']:.4f}, "
                f"coverage={row['answer_coverage']:.4f}, "
                f"citation_accuracy={row['citation_accuracy']:.4f}, "
                f"citation_recall={row['citation_recall']:.4f}",
                "",
            ]
        )
    path.write_text("\n".join(lines), encoding="utf-8")
