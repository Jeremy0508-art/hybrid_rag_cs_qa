from pathlib import Path

from hybrid_rag_cs_qa.data import load_chunks, load_qa


def test_qa_evidence_ids_exist_and_ids_are_unique():
    chunks = load_chunks(Path("data/raw/cs_courses_expanded.md"))
    qa_items = load_qa(Path("data/qa/eval_qa_expanded.jsonl"))
    chunk_ids = {chunk.id for chunk in chunks}
    qa_ids = [item.id for item in qa_items]

    assert len(chunks) >= 120
    assert len(qa_items) >= 500
    assert len(qa_ids) == len(set(qa_ids))
    assert {item.topic for item in qa_items} - {"unknown"}
    assert any(item.requires_multi_hop for item in qa_items)
    assert all(item.expected_concepts for item in qa_items)
    assert any(item.answer_style == "paraphrase" for item in qa_items)
    assert any(item.question_type == "multi_hop_paraphrase" for item in qa_items)

    missing = {
        item.id: sorted(set(item.evidence_ids) - chunk_ids)
        for item in qa_items
        if set(item.evidence_ids) - chunk_ids
    }
    assert missing == {}
