from hybrid_rag_cs_qa.reranker import FeatureReranker, is_multi_hop_question, topic_key
from hybrid_rag_cs_qa.schema import Chunk


def test_topic_key_strips_known_aspect_suffix():
    assert topic_key("TCP and UDP Transport Foundations") == "TCP and UDP Transport"
    assert topic_key("TCP and UDP Transport Mechanisms") == "TCP and UDP Transport"
    assert topic_key("TCP and UDP Transport") == "TCP and UDP Transport"


def test_multi_hop_question_detection():
    assert is_multi_hop_question("Why should these concepts be combined?")
    assert is_multi_hop_question("Why do both pieces of evidence matter?")
    assert not is_multi_hop_question("What is TCP?")


def test_reranker_features_include_candidate_context():
    chunk = Chunk(
        id="net-tcp-foundations",
        course="Computer Networks",
        title="TCP and UDP Transport Foundations",
        text="TCP provides reliable transport while UDP is lightweight.",
        concepts=("TCP", "UDP", "reliability"),
    )
    sibling = Chunk(
        id="net-tcp-mechanisms",
        course="Computer Networks",
        title="TCP and UDP Transport Mechanisms",
        text="TCP uses acknowledgments and retransmission.",
        concepts=("TCP", "ACK", "reliability"),
    )

    features_without_sibling = FeatureReranker().featurize(
        "Why do TCP and reliability need to be combined?",
        chunk,
        candidate_chunks=[chunk],
    )
    features_with_sibling = FeatureReranker().featurize(
        "Why do TCP and reliability need to be combined?",
        chunk,
        candidate_chunks=[chunk, sibling],
    )

    assert len(features_with_sibling) > 9
    assert features_with_sibling[-3] == 1.0
    assert features_with_sibling[-2] == 1.0
    assert features_with_sibling[-1] == 1.0
    assert features_with_sibling[-3] > features_without_sibling[-3]
