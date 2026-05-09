from hybrid_rag_cs_qa.evaluate import context_precision, mrr, ndcg, recall_at_k
from hybrid_rag_cs_qa.generation import citation_accuracy, citation_recall, generate_answer
from hybrid_rag_cs_qa.schema import Chunk, SearchResult


def test_retrieval_metrics():
    retrieved = ["a", "b", "c"]
    gold = {"b", "d"}
    assert recall_at_k(retrieved, gold) == 0.5
    assert mrr(retrieved, gold) == 0.5
    assert round(ndcg(retrieved, gold), 4) == 0.3869
    assert context_precision(retrieved, gold) == 1 / 3


def test_generation_citation_metrics():
    citations = ["a", "b", "c"]
    gold = {"b", "d"}
    assert citation_accuracy(citations, gold) == 0.3333
    assert citation_recall(citations, gold) == 0.5


def test_llm_generator_falls_back_to_extractive_without_endpoint(monkeypatch):
    monkeypatch.delenv("CS_RAG_LLM_BASE_URL", raising=False)
    chunk = Chunk(
        id="test-chunk",
        course="测试课程",
        title="测试标题",
        text="这是一个测试证据。它用于验证生成器回退逻辑。",
        concepts=("测试",),
    )
    answer, generator = generate_answer(
        "测试证据有什么作用？",
        [SearchResult(chunk=chunk, score=1.0, source="test")],
        generator="openai-compatible",
    )
    assert generator == "extractive"
    assert "[test-chunk]" in answer
