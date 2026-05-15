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
        "Retrieval Metrics on 750 QA",
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
        "Adaptive Generation with Graph RAPTOR Pruning",
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
    width, height = 1280, 600
    left, top, chart_w, chart_h = 80, 80, 1120, 350
    methods = list(data)
    metrics = list(metric_labels)
    colors = {
        "naive": "#4b5563",
        "hybrid": "#2563eb",
        "hybrid_rerank": "#0891b2",
        "graph_reflect": "#dc2626",
        "graph_pruned": "#16a34a",
        "raptor": "#7c3aed",
        "raptor_topdown": "#a855f7",
        "hybrid_raptor": "#ea580c",
        "graph_raptor_pruned": "#0f766e",
    }
    lines = svg_header(width, height, title)
    lines.extend(axis_lines(left, top, chart_w, chart_h))

    group_w = chart_w / len(metrics)
    bar_w = min(20, group_w / (len(methods) + 1))
    for mi, metric in enumerate(metrics):
        gx = left + mi * group_w + group_w * 0.08
        for si, method in enumerate(methods):
            value = data[method][metric]
            bar_h = value * chart_h
            x = gx + si * bar_w * 1.12
            y = top + chart_h - bar_h
            lines.append(rect(x, y, bar_w, bar_h, colors.get(method, "#64748b")))
            lines.append(text(x + bar_w / 2, y - 8, f"{value:.2f}", 10, "middle", "#334155"))
        lines.append(text(left + mi * group_w + group_w / 2, top + chart_h + 38, metric_labels[metric], 14, "middle"))

    legend_x = left
    legend_y = height - 105
    per_row = 3
    item_w = 350
    row_h = 32
    for idx, method in enumerate(methods):
        x = legend_x + (idx % per_row) * item_w
        y = legend_y + (idx // per_row) * row_h
        lines.append(rect(x, y - 12, 14, 14, colors.get(method, "#64748b")))
        lines.append(text(x + 22, y, method, 13, "start"))
    lines.append("</svg>")
    path.write_text("\n".join(lines), encoding="utf-8")


def write_single_bar_svg(path: Path, title: str, data: dict[str, float], labels: dict[str, str]) -> None:
    width, height = 820, 460
    left, top, chart_w, chart_h = 80, 80, 660, 280
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
        text(42, height - 125, "0.0", 12, "middle", "#64748b"),
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

面向计算机课程问答，将原来的基础 RAG 小实验升级为可复现的成熟 RAG 研究型项目：系统支持扩展数据集、BM25 + dense 混合检索、GraphRAG、RAPTOR summary tree、Hybrid RAPTOR 融合检索、证据压缩、自适应生成预算、分组检索评估和分组生成评估。

## 核心结果

![Retrieval Metrics](figures/retrieval_metrics.svg)

![Generation Metrics](figures/generation_metrics.svg)

## 关键发现

- 数据集已从 34 个知识块和 100 条 QA 扩展到 150 个课程文档和 750 条标注 QA，并覆盖 citation-grounded、title-explicit、paraphrase 和 multi-hop paraphrase 问题。
- `hybrid_raptor` 在整体检索上表现最好：Recall@5 = 0.9813，MRR = 0.9822，NDCG = 0.9723。
- `graph_raptor_pruned` 更偏向高质量上下文：Recall@5 = 0.9667，MRR = 0.9833，Context Precision = 0.5353，高于未压缩融合检索的 0.2725。
- 在更难的 paraphrase 子集上，`graph_raptor_pruned` 的 Context Precision = 0.4433，说明证据压缩对低噪声引用更有价值。
- 生成评估采用 `graph_raptor_pruned` + adaptive top-k：Faithfulness = 0.9909，Answer Coverage = 0.9814，Citation Recall = 0.9687。
- RAPTOR 的 summary node 目前采用本地确定性摘要器，保证测试和实验可复现；后续可切换为 LLM summarizer 或更强 embedding backend。

## 当前推荐命令

```powershell
cs-rag build-expanded-dataset
cs-rag prepare
cs-rag train-reranker
cs-rag build-raptor-tree
cs-rag evaluate
cs-rag evaluate-generation --method graph_raptor_pruned --top-k 3 --adaptive-top-k --multi-hop-top-k 4
cs-rag build-showcase
pytest -q
```

## 推荐展示口径

这个项目的重点不是把一个 demo 包装成复杂系统，而是把 RAG 中常见的三类矛盾拆开验证：召回更多证据、控制上下文噪声、让生成答案保持可引用。扩展数据集之后，RAPTOR 负责提供层次化语义摘要和跨 chunk 线索，GraphRAG 负责补充概念邻接关系，证据压缩负责把最终上下文收紧到更适合生成的证据集合。
""",
        encoding="utf-8",
    )


def write_interview_cheatsheet(path: Path) -> None:
    path.write_text(
        """# Interview Cheatsheet

## 30 秒介绍

我做了一个面向计算机课程问答的成熟 RAG 实验系统。项目从原来的基础 RAG 扩展到 150 个课程文档和 750 条标注 QA，覆盖普通事实问答、改写问法和多跳问题。系统实现了 BM25 + dense 混合检索、GraphRAG 概念扩展、RAPTOR summary tree、Hybrid RAPTOR 融合检索、证据压缩和自适应生成预算。当前最强整体检索方法 `hybrid_raptor` 的 Recall@5 达到 0.9813；面向生成的 `graph_raptor_pruned` 在保持 0.9667 Recall@5 的同时提供更高 Context Precision，并在生成评估中达到 0.9909 Faithfulness 和 0.9687 Citation Recall。

## 为什么不是普通 RAG

普通 RAG 主要依赖 chunk 级相似度，面对课程问答里的概念改写、多跳线索和跨章节关联时容易漏召回。这个项目同时引入三类补充信号：BM25 保留术语精确匹配，RAPTOR summary tree 提供层次化语义摘要，GraphRAG 提供概念邻接扩展。最后再用证据压缩控制噪声，避免把召回提升直接转化为低质量上下文。

## 最重要实验结论

`hybrid_raptor` 是整体检索最强方法：Recall@5 = 0.9813，MRR = 0.9822，NDCG = 0.9723。`graph_raptor_pruned` 是更适合生成的折中方案：Recall@5 = 0.9667，MRR = 0.9833，Context Precision = 0.5353。生成侧使用 `graph_raptor_pruned` + adaptive top-k 后，Faithfulness = 0.9909，Answer Coverage = 0.9814，Citation Recall = 0.9687。

## 可被追问的问题

Q: 为什么要引入 RAPTOR？
A: GraphRAG 擅长沿概念关系扩展，但它本身不生成层次化摘要。RAPTOR 可以把底层 chunk 聚类成 summary node，让检索先看到更高层的主题线索，再回落到底层证据，因此更适合处理改写问法和跨 chunk 问题。

Q: 为什么还需要 GraphRAG？
A: RAPTOR 解决的是层次化语义组织，GraphRAG 解决的是显式概念关系。课程问答里很多问题不是同义改写，而是概念之间的依赖或并列关系，所以两者互补。

Q: 为什么 `graph_raptor_pruned` 的 Recall 不如 `hybrid_raptor`？
A: 它是面向生成优化的方法，会主动压缩候选证据，牺牲少量召回换取更干净的上下文。对于最终问答系统，低噪声证据通常比单纯返回更多 chunk 更重要。

Q: RAPTOR 代码是否直接复制参考项目？
A: 没有直接照搬。参考项目用于理解聚类、summary 和树构建思想；主项目重新实现了适配本项目 schema、chunk metadata、评估闭环和 CLI 的版本。这样更容易维护，也不会把参考项目的实验假设硬塞进主项目。

## 简历 bullet

独立构建面向计算机课程问答的 Hybrid GraphRAG + RAPTOR 系统，将数据集扩展到 150 个课程文档和 750 条标注 QA；实现 BM25 + dense RRF 融合检索、GraphRAG 概念扩展、RAPTOR summary tree、Hybrid RAPTOR 检索、证据压缩和自适应生成评估，使整体检索 Recall@5 达到 0.9813，并在生成侧达到 0.9909 Faithfulness、0.9814 Answer Coverage 和 0.9687 Citation Recall。
""",
        encoding="utf-8",
    )
