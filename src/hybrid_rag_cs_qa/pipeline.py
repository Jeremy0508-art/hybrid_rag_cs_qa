from __future__ import annotations

from pathlib import Path

from .data import extract_concepts, load_chunks
from .graph_rag import GraphExpander
from .generation import generate_answer
from .reranker import FeatureReranker
from .retrievers import BM25Retriever, DenseRetriever, rrf_fuse
from .schema import SearchResult


class RagPipeline:
    def __init__(self, corpus_path: Path, reranker_path: Path | None = None):
        self.chunks = load_chunks(corpus_path)
        self.bm25 = BM25Retriever(self.chunks)
        self.dense = DenseRetriever(self.chunks)
        self.graph = GraphExpander(self.chunks)
        self.reranker = FeatureReranker.load(reranker_path) if reranker_path and reranker_path.exists() else None

    def search(self, question: str, method: str, top_k: int = 5) -> list[SearchResult]:
        candidate_k = max(top_k * 4, 10)
        if method == "naive":
            return self.dense.search(question, top_k)
        if method == "hybrid":
            return rrf_fuse(
                [self.bm25.search(question, candidate_k), self.dense.search(question, candidate_k)],
                top_k=top_k,
            )
        if method == "hybrid_rerank":
            candidates = rrf_fuse(
                [self.bm25.search(question, candidate_k), self.dense.search(question, candidate_k)],
                top_k=candidate_k,
            )
            return self.reranker.rerank(question, candidates, top_k) if self.reranker else candidates[:top_k]
        if method == "graph_reflect":
            candidates = self._graph_candidates(question, candidate_k)
            return self.reranker.rerank(question, candidates, top_k) if self.reranker else candidates[:top_k]
        if method == "graph_pruned":
            candidates = self._graph_candidates(question, candidate_k)
            reranked = self.reranker.rerank(question, candidates, candidate_k) if self.reranker else candidates
            return self._compress_evidence(question, reranked, max_results=min(3, top_k))
        raise ValueError(f"Unknown method: {method}")

    def answer_extractive(
        self,
        question: str,
        method: str = "graph_pruned",
        generator: str = "extractive",
    ) -> dict[str, object]:
        results = self.search(question, method=method, top_k=3)
        answer, used_generator = generate_answer(question, results, generator=generator)
        return {
            "question": question,
            "answer": answer,
            "citations": [r.chunk.id for r in results],
            "method": method,
            "generator": used_generator,
        }

    @staticmethod
    def _needs_more_evidence(question: str, candidates: list[SearchResult]) -> bool:
        if not candidates:
            return True
        concept_hits = sum(bool(set(extract_concepts(question)) & set(r.chunk.concepts)) for r in candidates[:3])
        return concept_hits == 0

    def _graph_candidates(self, question: str, candidate_k: int) -> list[SearchResult]:
        candidates = rrf_fuse(
            [
                self.bm25.search(question, candidate_k),
                self.dense.search(question, candidate_k),
                self.graph.expand(question, candidate_k),
            ],
            top_k=candidate_k,
        )
        if self._needs_more_evidence(question, candidates):
            expanded_question = question + " " + " ".join(extract_concepts(question))
            candidates = rrf_fuse(
                [candidates, self.graph.expand(expanded_question, candidate_k)],
                top_k=candidate_k,
            )
        return candidates

    @staticmethod
    def _compress_evidence(
        question: str,
        results: list[SearchResult],
        max_results: int = 3,
        min_relative_score: float = 0.35,
    ) -> list[SearchResult]:
        if not results:
            return []
        query_concepts = set(extract_concepts(question))
        best_score = max(results[0].score, 1e-9)
        compressed: list[SearchResult] = []
        seen_courses: set[str] = set()

        for result in results:
            if len(compressed) >= max_results:
                break
            concept_overlap = bool(query_concepts & set(result.chunk.concepts))
            same_course_as_existing = result.chunk.course in seen_courses
            high_confidence = result.score >= best_score * min_relative_score
            if not compressed or concept_overlap or high_confidence or not same_course_as_existing:
                compressed.append(result)
                seen_courses.add(result.chunk.course)
        return compressed
