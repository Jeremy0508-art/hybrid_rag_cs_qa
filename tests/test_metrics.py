from hybrid_rag_cs_qa.evaluate import context_precision, mrr, ndcg, recall_at_k, summarize_groups
from hybrid_rag_cs_qa.generation import (
    citation_accuracy,
    citation_recall,
    choose_generation_top_k,
    generate_answer,
    score_answer,
    summarize_generation,
    summarize_generation_groups,
)
from hybrid_rag_cs_qa.schema import Chunk, QAItem, SearchResult


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


def test_grouped_generation_metrics():
    rows = [
        {
            "answer_style": "paraphrase",
            "type": "multi_hop",
            "requires_multi_hop": True,
            "difficulty": "hard",
            "topic": "RAG",
            "faithfulness": 1.0,
            "answer_coverage": 0.5,
            "citation_accuracy": 0.5,
            "citation_recall": 1.0,
        },
        {
            "answer_style": "paraphrase",
            "type": "multi_hop",
            "requires_multi_hop": True,
            "difficulty": "hard",
            "topic": "RAG",
            "faithfulness": 0.5,
            "answer_coverage": 0.25,
            "citation_accuracy": 0.0,
            "citation_recall": 0.0,
        },
    ]

    assert summarize_generation([])["faithfulness"] == 0.0
    grouped = summarize_generation_groups(rows)

    assert grouped["by_answer_style"]["paraphrase"]["num_questions"] == 2
    assert grouped["by_answer_style"]["paraphrase"]["faithfulness"] == 0.75
    assert grouped["by_multi_hop"]["True"]["citation_recall"] == 0.5


def test_score_answer_preserves_qa_metadata():
    item = QAItem(
        id="q",
        question="What is TCP?",
        answer="TCP is reliable transport.",
        evidence_ids=("tcp",),
        difficulty="easy",
        question_type="definition",
        topic="Computer Networks",
        subtopic="TCP",
        expected_concepts=("TCP",),
        requires_multi_hop=False,
        answer_style="citation-grounded",
    )
    chunk = Chunk(
        id="tcp",
        course="Computer Networks",
        title="TCP",
        text="TCP is reliable transport.",
        concepts=("TCP",),
    )

    row = score_answer(item, "TCP is reliable transport. [tcp]", [SearchResult(chunk, 1.0, "test")])

    assert row["topic"] == "Computer Networks"
    assert row["type"] == "definition"
    assert row["answer_style"] == "citation-grounded"
    assert row["top_k"] == 1


def test_choose_generation_top_k_adapts_for_multi_hop():
    single = QAItem(
        id="single",
        question="What is TCP?",
        answer="TCP is reliable transport.",
        evidence_ids=("tcp",),
        difficulty="easy",
        question_type="definition",
    )
    multi = QAItem(
        id="multi",
        question="Why combine TCP and DNS evidence?",
        answer="Both are needed.",
        evidence_ids=("tcp", "dns"),
        difficulty="hard",
        question_type="multi_hop",
        requires_multi_hop=True,
    )

    assert choose_generation_top_k(single, top_k=3, adaptive_top_k=True) == 3
    assert choose_generation_top_k(multi, top_k=3, adaptive_top_k=True) == 4
    assert choose_generation_top_k(multi, top_k=3, adaptive_top_k=True, multi_hop_top_k=5) == 5


def test_grouped_retrieval_metrics():
    rows = [
        {
            "topic": "OS",
            "difficulty": "easy",
            "type": "definition",
            "requires_multi_hop": False,
            "recall": 1.0,
            "mrr": 1.0,
            "ndcg": 1.0,
            "context_precision": 0.5,
        },
        {
            "topic": "OS",
            "difficulty": "hard",
            "type": "multi_hop",
            "requires_multi_hop": True,
            "recall": 0.5,
            "mrr": 0.25,
            "ndcg": 0.4,
            "context_precision": 0.2,
        },
        {
            "topic": "RAG",
            "difficulty": "hard",
            "type": "multi_hop",
            "requires_multi_hop": True,
            "recall": 0.0,
            "mrr": 0.0,
            "ndcg": 0.0,
            "context_precision": 0.0,
        },
    ]

    grouped = summarize_groups(rows)

    assert grouped["by_topic"]["OS"]["num_questions"] == 2
    assert grouped["by_topic"]["OS"]["recall"] == 0.75
    assert grouped["by_difficulty"]["hard"]["num_questions"] == 2
    assert grouped["by_multi_hop"]["True"]["recall"] == 0.25


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
