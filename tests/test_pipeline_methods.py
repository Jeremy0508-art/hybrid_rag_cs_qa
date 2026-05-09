from pathlib import Path

from hybrid_rag_cs_qa.pipeline import RagPipeline


def test_pipeline_methods_return_results():
    pipeline = RagPipeline(Path("data/raw/cs_courses.md"))
    question = "GraphRAG 为什么可能提高召回率但降低 Context Precision？"

    for method in ("naive", "hybrid", "hybrid_rerank", "graph_reflect", "graph_pruned"):
        results = pipeline.search(question, method=method, top_k=5)
        assert len(results) > 0
        assert all(result.chunk.id for result in results)


def test_graph_pruned_returns_no_more_than_three_results():
    pipeline = RagPipeline(Path("data/raw/cs_courses.md"))
    results = pipeline.search("hard negative 如何降低 GraphRAG 噪声？", method="graph_pruned", top_k=5)
    assert 0 < len(results) <= 3
