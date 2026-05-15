from __future__ import annotations

from dataclasses import dataclass

from .data import extract_concepts
from .reranker import topic_key
from .schema import SearchResult
from .text import tokenize


@dataclass(frozen=True)
class EvidenceSetConfig:
    max_results: int = 4
    rank_weight: float = 0.45
    token_weight: float = 0.25
    concept_weight: float = 0.9
    topic_diversity_weight: float = 0.2
    sibling_weight: float = 0.35


class EvidenceSetSelector:
    def __init__(self, config: EvidenceSetConfig | None = None):
        self.config = config or EvidenceSetConfig()

    def select(self, question: str, candidates: list[SearchResult], max_results: int | None = None) -> list[SearchResult]:
        if not candidates:
            return []

        limit = max_results or self.config.max_results
        query_tokens = set(tokenize(question))
        query_concepts = set(extract_concepts(question))
        selected: list[SearchResult] = []
        covered_tokens: set[str] = set()
        covered_concepts: set[str] = set()
        selected_topics: set[tuple[str, str]] = set()

        remaining = list(dict.fromkeys(candidates))
        while remaining and len(selected) < limit:
            best = max(
                remaining,
                key=lambda result: self._gain(
                    result,
                    candidates,
                    query_tokens,
                    query_concepts,
                    covered_tokens,
                    covered_concepts,
                    selected_topics,
                ),
            )
            selected.append(best)
            remaining.remove(best)
            covered_tokens.update(query_tokens & set(tokenize(best.chunk.title + " " + best.chunk.text)))
            covered_concepts.update(query_concepts & set(best.chunk.concepts))
            selected_topics.add((best.chunk.course, topic_key(best.chunk.title)))

        return selected

    def _gain(
        self,
        result: SearchResult,
        candidates: list[SearchResult],
        query_tokens: set[str],
        query_concepts: set[str],
        covered_tokens: set[str],
        covered_concepts: set[str],
        selected_topics: set[tuple[str, str]],
    ) -> float:
        chunk_tokens = set(tokenize(result.chunk.title + " " + result.chunk.text))
        chunk_concepts = set(result.chunk.concepts)
        topic = (result.chunk.course, topic_key(result.chunk.title))

        token_gain = len((query_tokens & chunk_tokens) - covered_tokens) / max(len(query_tokens), 1)
        concept_gain = len((query_concepts & chunk_concepts) - covered_concepts) / max(len(query_concepts), 1)
        rank_gain = 1.0 / (candidates.index(result) + 1)
        diversity_gain = 0.0 if topic in selected_topics else 1.0
        sibling_gain = 1.0 if self._has_sibling_candidate(result, candidates) else 0.0

        return (
            self.config.rank_weight * rank_gain
            + self.config.token_weight * token_gain
            + self.config.concept_weight * concept_gain
            + self.config.topic_diversity_weight * diversity_gain
            + self.config.sibling_weight * sibling_gain
        )

    @staticmethod
    def _has_sibling_candidate(result: SearchResult, candidates: list[SearchResult]) -> bool:
        result_topic = (result.chunk.course, topic_key(result.chunk.title))
        return any(
            candidate.chunk.id != result.chunk.id
            and (candidate.chunk.course, topic_key(candidate.chunk.title)) == result_topic
            for candidate in candidates
        )
