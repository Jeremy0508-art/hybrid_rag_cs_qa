from hybrid_rag_cs_qa.evidence_selector import EvidenceSetSelector
from hybrid_rag_cs_qa.schema import Chunk, SearchResult


def _result(chunk: Chunk, score: float = 1.0) -> SearchResult:
    return SearchResult(chunk=chunk, score=score, source="test")


def test_evidence_selector_covers_multiple_query_concepts():
    tcp = Chunk(
        id="tcp",
        course="Computer Networks",
        title="TCP and UDP Transport Foundations",
        text="TCP provides reliable transport.",
        concepts=("TCP", "reliability"),
    )
    dns = Chunk(
        id="dns",
        course="Computer Networks",
        title="DNS Resolution Foundations",
        text="DNS resolves names using caches.",
        concepts=("DNS", "cache"),
    )
    noise = Chunk(
        id="noise",
        course="Databases",
        title="Transactions and ACID Foundations",
        text="Transactions preserve atomicity.",
        concepts=("transaction", "ACID"),
    )

    selected = EvidenceSetSelector().select(
        "Why would TCP and DNS evidence need to be combined?",
        [_result(noise, 1.0), _result(tcp, 0.9), _result(dns, 0.8)],
        max_results=2,
    )

    assert {result.chunk.id for result in selected} == {"tcp", "dns"}


def test_evidence_selector_rewards_sibling_candidates():
    foundations = Chunk(
        id="tcp-foundations",
        course="Computer Networks",
        title="TCP and UDP Transport Foundations",
        text="TCP provides reliability.",
        concepts=("TCP", "reliability"),
    )
    mechanisms = Chunk(
        id="tcp-mechanisms",
        course="Computer Networks",
        title="TCP and UDP Transport Mechanisms",
        text="TCP uses acknowledgments.",
        concepts=("TCP", "ACK"),
    )
    unrelated = Chunk(
        id="routing",
        course="Computer Networks",
        title="Routing NAT and Subnetting Foundations",
        text="Routers forward packets.",
        concepts=("routing", "NAT"),
    )

    selected = EvidenceSetSelector().select(
        "Why would TCP reliability evidence need to be combined?",
        [_result(foundations, 1.0), _result(unrelated, 0.95), _result(mechanisms, 0.9)],
        max_results=2,
    )

    assert {result.chunk.id for result in selected} == {"tcp-foundations", "tcp-mechanisms"}
