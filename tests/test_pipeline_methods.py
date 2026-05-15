from pathlib import Path

from hybrid_rag_cs_qa.pipeline import RagPipeline
from hybrid_rag_cs_qa.schema import Chunk, SearchResult


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


def test_adaptive_evidence_compression_stops_after_dominant_top_result():
    top = Chunk("top", "RAG", "GraphRAG", "GraphRAG improves recall.", ("GraphRAG",))
    weak = Chunk("weak", "RAG", "Dense Retrieval", "Dense retrieval uses embeddings.", ("Embedding",))
    results = [
        SearchResult(top, 1.0, "test"),
        SearchResult(weak, 0.5, "test"),
    ]

    compressed = RagPipeline._compress_evidence_adaptive("Why does GraphRAG improve recall?", results, max_results=3)

    assert [result.chunk.id for result in compressed] == ["top"]


def test_adaptive_evidence_compression_keeps_close_second_result():
    top = Chunk("top", "RAG", "GraphRAG", "GraphRAG improves recall.", ("GraphRAG",))
    second = Chunk("second", "RAG", "GraphRAG Tradeoffs", "GraphRAG can reduce context precision.", ("GraphRAG",))
    third = Chunk("third", "RAG", "Dense Retrieval", "Dense retrieval uses embeddings.", ("Embedding",))
    results = [
        SearchResult(top, 1.0, "test"),
        SearchResult(second, 0.8, "test"),
        SearchResult(third, 0.7, "test"),
    ]

    compressed = RagPipeline._compress_evidence_adaptive("Why does GraphRAG improve recall?", results, max_results=3)

    assert [result.chunk.id for result in compressed] == ["top", "second"]
