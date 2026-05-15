from pathlib import Path

from hybrid_rag_cs_qa.pipeline import RagPipeline


def test_pipeline_methods_return_results():
    pipeline = RagPipeline(Path("data/raw/cs_courses_expanded.md"))
    question = "GraphRAG 为什么可能提高召回率但降低 Context Precision？"

    for method in (
        "naive",
        "hybrid",
        "hybrid_rerank",
        "graph_reflect",
        "graph_pruned",
        "raptor",
        "raptor_topdown",
        "hybrid_raptor",
        "graph_raptor_pruned",
    ):
        results = pipeline.search(question, method=method, top_k=5)
        assert len(results) > 0
        assert all(result.chunk.id for result in results)


def test_graph_pruned_returns_no_more_than_three_results():
    pipeline = RagPipeline(Path("data/raw/cs_courses_expanded.md"))
    results = pipeline.search("hard negative 如何降低 GraphRAG 噪声？", method="graph_pruned", top_k=5)
    assert 0 < len(results) <= 3


def test_graph_raptor_pruned_allows_four_results_for_multi_hop():
    pipeline = RagPipeline(Path("data/raw/cs_courses_expanded.md"))
    results = pipeline.search(
        "Why would evidence about TCP and reliability need to be combined for a grounded systems answer?",
        method="graph_raptor_pruned",
        top_k=5,
    )
    assert 0 < len(results) <= 4


def test_pipeline_default_search_uses_graph_raptor_pruned():
    pipeline = RagPipeline(Path("data/raw/cs_courses_expanded.md"))
    explicit = pipeline.search(
        "Why can GraphRAG improve recall but reduce context precision?",
        method="graph_raptor_pruned",
        top_k=5,
    )
    default = pipeline.search(
        "Why can GraphRAG improve recall but reduce context precision?",
        top_k=5,
    )

    assert [result.chunk.id for result in default] == [result.chunk.id for result in explicit]
