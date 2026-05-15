from pathlib import Path

from hybrid_rag_cs_qa.data import load_chunks
from hybrid_rag_cs_qa.raptor_builder import RaptorBuildConfig, RaptorTreeBuilder
from hybrid_rag_cs_qa.raptor_retriever import RaptorRetriever
from hybrid_rag_cs_qa.raptor_store import load_raptor_tree, save_raptor_tree


def test_raptor_tree_builds_summary_layers():
    chunks = load_chunks(Path("data/raw/cs_courses_expanded.md"))
    tree = RaptorTreeBuilder(
        config=RaptorBuildConfig(max_layers=3, max_cluster_size=5, max_summary_tokens=80)
    ).build(chunks)

    assert len(tree.leaf_ids) == len(chunks)
    assert len(tree.nodes) > len(chunks)
    assert tree.root_ids
    assert max(tree.layer_to_node_ids) >= 1


def test_raptor_tree_can_roundtrip_json(tmp_path):
    chunks = load_chunks(Path("data/raw/cs_courses_expanded.md"))
    tree = RaptorTreeBuilder(
        config=RaptorBuildConfig(max_layers=2, max_cluster_size=6, max_summary_tokens=80)
    ).build(chunks)
    path = tmp_path / "raptor_tree.json"

    save_raptor_tree(tree, path)
    loaded = load_raptor_tree(path)

    assert loaded.root_ids == tree.root_ids
    assert loaded.leaf_ids == tree.leaf_ids
    assert set(loaded.nodes) == set(tree.nodes)


def test_raptor_retriever_returns_original_chunks():
    chunks = load_chunks(Path("data/raw/cs_courses_expanded.md"))
    tree = RaptorTreeBuilder(
        config=RaptorBuildConfig(max_layers=2, max_cluster_size=6, max_summary_tokens=80)
    ).build(chunks)
    retriever = RaptorRetriever(chunks, tree)

    results = retriever.search("GraphRAG RRF Recall", top_k=3)

    assert results
    assert all(result.chunk.id for result in results)
    assert all("raptor:" in result.source for result in results)


def test_raptor_topdown_uses_summary_tree_to_reach_relevant_leaves():
    chunks = load_chunks(Path("data/raw/cs_courses_expanded.md"))
    tree = RaptorTreeBuilder(
        config=RaptorBuildConfig(max_layers=3, max_cluster_size=6, max_summary_tokens=100)
    ).build(chunks)
    retriever = RaptorRetriever(chunks, tree)

    results = retriever.search("How does RAPTOR tree retrieval use summary nodes?", top_k=5, mode="topdown")
    retrieved_ids = {result.chunk.id for result in results}

    assert results
    assert any("raptor-tree-retrieval" in chunk_id for chunk_id in retrieved_ids)


def test_raptor_topdown_handles_multi_hop_titles():
    chunks = load_chunks(Path("data/raw/cs_courses_expanded.md"))
    tree = RaptorTreeBuilder(
        config=RaptorBuildConfig(max_layers=3, max_cluster_size=6, max_summary_tokens=100)
    ).build(chunks)
    retriever = RaptorRetriever(chunks, tree)

    results = retriever.search(
        "Why might TCP and UDP Transport Foundations and TCP and UDP Transport Mechanisms both matter?",
        top_k=5,
        mode="topdown",
    )
    retrieved_ids = {result.chunk.id for result in results}

    assert "computer-networks-tcp-and-udp-transport-foundations" in retrieved_ids
    assert "computer-networks-tcp-and-udp-transport-mechanisms" in retrieved_ids


def test_raptor_topdown_expands_sibling_evidence_for_paraphrase_multi_hop():
    chunks = load_chunks(Path("data/raw/cs_courses_expanded.md"))
    tree = RaptorTreeBuilder(
        config=RaptorBuildConfig(max_layers=3, max_cluster_size=6, max_summary_tokens=100)
    ).build(chunks)
    retriever = RaptorRetriever(chunks, tree)

    results = retriever.search(
        "Why would evidence about TCP and reliability need to be combined for a grounded systems answer?",
        top_k=5,
        mode="topdown",
    )
    retrieved_ids = {result.chunk.id for result in results}

    assert len(
        {
            chunk_id
            for chunk_id in retrieved_ids
            if chunk_id.startswith("computer-networks-tcp-and-udp-transport")
        }
    ) >= 2
