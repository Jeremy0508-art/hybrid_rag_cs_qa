from hybrid_rag_cs_qa.evaluate import context_precision, mrr, ndcg, recall_at_k
from hybrid_rag_cs_qa.generation import citation_accuracy, citation_recall


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
