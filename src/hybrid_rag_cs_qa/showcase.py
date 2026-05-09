from __future__ import annotations

import json
from pathlib import Path


RETRIEVAL_METRICS = ("recall", "mrr", "ndcg", "context_precision")
GENERATION_METRICS = ("faithfulness", "answer_coverage", "citation_accuracy", "citation_recall")


def build_showcase(retrieval_path: Path, generation_path: Path, reports_dir: Path) -> dict[str, Path]:
    retrieval = json.loads(retrieval_path.read_text(encoding="utf-8"))
    generation = json.loads(generation_path.read_text(encoding="utf-8"))
    figures_dir = reports_dir / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)

    retrieval_svg = figures_dir / "retrieval_metrics.svg"
    generation_svg = figures_dir / "generation_metrics.svg"
    write_grouped_bar_svg(
        retrieval_svg,
        "Retrieval Metrics on 100 QA",
        {method: {metric: retrieval[method][metric] for metric in RETRIEVAL_METRICS} for method in retrieval},
        metric_labels={
            "recall": "Recall@5",
            "mrr": "MRR",
            "ndcg": "NDCG",
            "context_precision": "Context Precision",
        },
    )
    write_single_bar_svg(
        generation_svg,
        "Generation Metrics with Graph + Pruning",
        {metric: generation[metric] for metric in GENERATION_METRICS},
        labels={
            "faithfulness": "Faithfulness",
            "answer_coverage": "Answer Coverage",
            "citation_accuracy": "Citation Accuracy",
            "citation_recall": "Citation Recall",
        },
    )

    final_summary = reports_dir / "final_showcase.md"
    interview = reports_dir / "interview_cheatsheet.md"
    write_final_showcase(final_summary)
    write_interview_cheatsheet(interview)
    return {
        "retrieval_svg": retrieval_svg,
        "generation_svg": generation_svg,
        "final_showcase": final_summary,
        "interview_cheatsheet": interview,
    }


def write_grouped_bar_svg(
    path: Path,
    title: str,
    data: dict[str, dict[str, float]],
    metric_labels: dict[str, str],
) -> None:
    width, height = 980, 520
    left, top, chart_w, chart_h = 80, 80, 840, 330
    methods = list(data)
    metrics = list(metric_labels)
    colors = {
        "naive": "#4b5563",
        "hybrid": "#2563eb",
        "hybrid_rerank": "#0891b2",
        "graph_reflect": "#dc2626",
        "graph_pruned": "#16a34a",
    }
    lines = svg_header(width, height, title)
    lines.extend(axis_lines(left, top, chart_w, chart_h))

    group_w = chart_w / len(metrics)
    bar_w = min(26, group_w / (len(methods) + 1))
    for mi, metric in enumerate(metrics):
        gx = left + mi * group_w + group_w * 0.12
        for si, method in enumerate(methods):
            value = data[method][metric]
            bar_h = value * chart_h
            x = gx + si * bar_w * 1.15
            y = top + chart_h - bar_h
            lines.append(rect(x, y, bar_w, bar_h, colors.get(method, "#64748b")))
            lines.append(text(x + bar_w / 2, y - 8, f"{value:.2f}", 11, "middle", "#334155"))
        lines.append(text(left + mi * group_w + group_w / 2, top + chart_h + 38, metric_labels[metric], 14, "middle"))

    legend_x = left
    legend_y = height - 55
    for idx, method in enumerate(methods):
        x = legend_x + idx * 170
        lines.append(rect(x, legend_y - 12, 14, 14, colors.get(method, "#64748b")))
        lines.append(text(x + 22, legend_y, method, 13, "start"))
    lines.append("</svg>")
    path.write_text("\n".join(lines), encoding="utf-8")


def write_single_bar_svg(path: Path, title: str, data: dict[str, float], labels: dict[str, str]) -> None:
    width, height = 760, 460
    left, top, chart_w, chart_h = 80, 80, 600, 280
    colors = ["#2563eb", "#0891b2", "#16a34a", "#9333ea"]
    lines = svg_header(width, height, title)
    lines.extend(axis_lines(left, top, chart_w, chart_h))
    bar_gap = 34
    bar_w = (chart_w - bar_gap * (len(data) - 1)) / len(data)
    for idx, (metric, value) in enumerate(data.items()):
        bar_h = value * chart_h
        x = left + idx * (bar_w + bar_gap)
        y = top + chart_h - bar_h
        lines.append(rect(x, y, bar_w, bar_h, colors[idx % len(colors)]))
        lines.append(text(x + bar_w / 2, y - 10, f"{value:.4f}", 13, "middle", "#334155"))
        lines.append(text(x + bar_w / 2, top + chart_h + 38, labels[metric], 14, "middle"))
    lines.append("</svg>")
    path.write_text("\n".join(lines), encoding="utf-8")


def svg_header(width: int, height: int, title: str) -> list[str]:
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        text(width / 2, 36, title, 22, "middle", "#0f172a", weight="700"),
        text(42, 85, "1.0", 12, "middle", "#64748b"),
        text(42, height - 105, "0.0", 12, "middle", "#64748b"),
    ]


def axis_lines(left: int, top: int, chart_w: int, chart_h: int) -> list[str]:
    lines = []
    for i in range(6):
        y = top + chart_h - chart_h * i / 5
        lines.append(f'<line x1="{left}" y1="{y:.1f}" x2="{left + chart_w}" y2="{y:.1f}" stroke="#e2e8f0"/>')
    lines.append(f'<line x1="{left}" y1="{top}" x2="{left}" y2="{top + chart_h}" stroke="#334155" stroke-width="1.2"/>')
    lines.append(f'<line x1="{left}" y1="{top + chart_h}" x2="{left + chart_w}" y2="{top + chart_h}" stroke="#334155" stroke-width="1.2"/>')
    return lines


def rect(x: float, y: float, w: float, h: float, fill: str) -> str:
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{fill}" rx="3"/>'


def text(
    x: float,
    y: float,
    value: str,
    size: int,
    anchor: str = "start",
    fill: str = "#0f172a",
    weight: str = "400",
) -> str:
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-family="Arial, sans-serif" '
        f'font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" fill="{fill}">{value}</text>'
    )


def write_final_showcase(path: Path) -> None:
    path.write_text(
        """# Project Showcase

## 项目一句话

面向计算机课程问答，构建 Hybrid Self-Reflective GraphRAG 系统，通过混合检索、图扩展、hard-negative 重排序和证据压缩提升证据召回与引用准确率。

## 核心结果

![Retrieval Metrics](figures/retrieval_metrics.svg)

![Generation Metrics](figures/generation_metrics.svg)

## 关键发现

- Naive RAG 在 100 条 QA 上 Recall@5 为 0.7500，说明普通检索会漏掉部分多跳和概念关联问题。
- Graph + Reflection RAG 将 Recall@5 提升到 0.9400，但 Context Precision 下降到 0.4140，说明图扩展带来噪声。
- Graph + Pruning RAG 将 Context Precision 提升到 0.6450，同时保持 0.9367 的 Recall@5。
- 生成评测中 Citation Accuracy 达到 0.6450，Citation Recall 达到 0.9367。

## 可复现命令

```powershell
cs-rag train-reranker
cs-rag evaluate
cs-rag evaluate-generation
cs-rag build-showcase
```
""",
        encoding="utf-8",
    )


def write_interview_cheatsheet(path: Path) -> None:
    path.write_text(
        """# Interview Cheatsheet

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
""",
        encoding="utf-8",
    )
