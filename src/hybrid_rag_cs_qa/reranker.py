from __future__ import annotations

from collections import Counter
from pathlib import Path
import re

import joblib
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from .data import extract_concepts
from .schema import Chunk, QAItem, SearchResult
from .text import cosine_from_counters, jaccard, tokenize


class FeatureReranker:
    def __init__(self):
        self.model = make_pipeline(
            StandardScaler(),
            LogisticRegression(max_iter=1000, class_weight="balanced"),
        )

    ASPECTS = ("Foundations", "Mechanisms", "Tradeoffs", "Applications", "Evaluation")

    def featurize(
        self,
        question: str,
        chunk: Chunk,
        base_score: float = 0.0,
        candidate_chunks: list[Chunk] | None = None,
    ) -> list[float]:
        q_tokens = tokenize(question)
        title_tokens = tokenize(chunk.title)
        c_tokens = tokenize(chunk.title + " " + chunk.text)
        q_counter = Counter(q_tokens)
        c_counter = Counter(c_tokens)
        q_concepts = set(extract_concepts(question))
        overlap = set(q_tokens) & set(c_tokens)
        candidate_chunks = candidate_chunks or []
        same_course_candidates = sum(1 for candidate in candidate_chunks if candidate.course == chunk.course)
        same_topic_candidates = sum(
            1
            for candidate in candidate_chunks
            if candidate.course == chunk.course and topic_key(candidate.title) == topic_key(chunk.title)
        )
        sibling_present = any(
            candidate.id != chunk.id
            and candidate.course == chunk.course
            and topic_key(candidate.title) == topic_key(chunk.title)
            for candidate in candidate_chunks
        )
        multi_hop_query = is_multi_hop_question(question)
        return [
            base_score,
            cosine_from_counters(q_counter, c_counter),
            jaccard(q_tokens, c_tokens),
            jaccard(q_tokens, title_tokens),
            len(overlap),
            len(set(q_tokens) & set(title_tokens)),
            len(chunk.concepts),
            len(set(chunk.concepts) & q_concepts),
            1.0 if chunk.course in question else 0.0,
            len(set(chunk.concepts) & q_concepts) / max(len(q_concepts), 1),
            same_course_candidates / max(len(candidate_chunks), 1),
            same_topic_candidates / max(len(candidate_chunks), 1),
            1.0 if sibling_present else 0.0,
            1.0 if multi_hop_query and sibling_present else 0.0,
            1.0 if multi_hop_query and same_topic_candidates >= 2 else 0.0,
        ]

    def fit(self, qa_items: list[QAItem], chunks: list[Chunk]) -> "FeatureReranker":
        x, y = [], []
        for item in qa_items:
            positives = set(item.evidence_ids)
            for chunk in chunks:
                x.append(self.featurize(item.question, chunk, candidate_chunks=chunks))
                y.append(1 if chunk.id in positives else 0)
        self.model.fit(np.array(x), np.array(y))
        return self

    def fit_from_candidates(
        self,
        qa_items: list[QAItem],
        candidate_sets: dict[str, list[SearchResult]],
        chunks: list[Chunk],
    ) -> "FeatureReranker":
        chunk_by_id = {chunk.id: chunk for chunk in chunks}
        x, y, weights = [], [], []
        for item in qa_items:
            positives = set(item.evidence_ids)
            seen: set[str] = set()
            item_candidates = candidate_sets.get(item.id, [])
            candidate_chunks = [result.chunk for result in item_candidates]
            for result in item_candidates:
                seen.add(result.chunk.id)
                x.append(self.featurize(item.question, result.chunk, result.score, candidate_chunks))
                y.append(1 if result.chunk.id in positives else 0)
                weights.append(5.0 if result.chunk.id in positives else 1.0)

            # Include missed positives so the model still sees the ideal evidence.
            for cid in positives - seen:
                if cid in chunk_by_id:
                    x.append(self.featurize(item.question, chunk_by_id[cid], 0.0, candidate_chunks))
                    y.append(1)
                    weights.append(5.0)

        self.model.fit(np.array(x), np.array(y), logisticregression__sample_weight=np.array(weights))
        return self

    def rerank(self, question: str, results: list[SearchResult], top_k: int = 5) -> list[SearchResult]:
        if not results:
            return []
        candidate_chunks = [result.chunk for result in results]
        features = np.array([self.featurize(question, r.chunk, r.score, candidate_chunks) for r in results])
        probs = self.model.predict_proba(features)[:, 1]
        reranked = [
            SearchResult(result.chunk, float(prob), result.source + "+rerank")
            for result, prob in zip(results, probs)
        ]
        return sorted(reranked, key=lambda r: r.score, reverse=True)[:top_k]

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self, path)

    @staticmethod
    def load(path: Path) -> "FeatureReranker":
        return joblib.load(path)


def topic_key(title: str) -> str:
    for aspect in FeatureReranker.ASPECTS:
        suffix = f" {aspect}"
        if title.endswith(suffix):
            return title[: -len(suffix)]
    return title


def is_multi_hop_question(question: str) -> bool:
    lower = question.lower()
    return bool(re.search(r"\b(combine|combined|both|multi-hop|together)\b", lower))
