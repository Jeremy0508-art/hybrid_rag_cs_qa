from pathlib import Path

from hybrid_rag_cs_qa.data import load_chunks, load_qa


def test_qa_evidence_ids_exist_and_ids_are_unique():
    chunks = load_chunks(Path("data/raw/cs_courses.md"))
    qa_items = load_qa(Path("data/qa/eval_qa.jsonl"))
    chunk_ids = {chunk.id for chunk in chunks}
    qa_ids = [item.id for item in qa_items]

    assert len(qa_items) >= 100
    assert len(qa_ids) == len(set(qa_ids))

    missing = {
        item.id: sorted(set(item.evidence_ids) - chunk_ids)
        for item in qa_items
        if set(item.evidence_ids) - chunk_ids
    }
    assert missing == {}
