from __future__ import annotations

import math
import os
from collections import Counter, defaultdict

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

from .schema import Chunk, SearchResult
from .text import tokenize


class BM25Retriever:
    def __init__(self, chunks: list[Chunk], k1: float = 1.5, b: float = 0.75):
        self.chunks = chunks
        self.k1 = k1
        self.b = b
        self.docs = [tokenize(c.text + " " + c.title) for c in chunks]
        self.avgdl = sum(len(d) for d in self.docs) / max(len(self.docs), 1)
        self.df: Counter[str] = Counter()
        for doc in self.docs:
            self.df.update(set(doc))

    def search(self, query: str, top_k: int = 5) -> list[SearchResult]:
        q = tokenize(query)
        scores = []
        n = len(self.docs)
        for idx, doc in enumerate(self.docs):
            tf = Counter(doc)
            score = 0.0
            dl = len(doc)
            for term in q:
                if term not in tf:
                    continue
                idf = math.log(1 + (n - self.df[term] + 0.5) / (self.df[term] + 0.5))
                denom = tf[term] + self.k1 * (1 - self.b + self.b * dl / max(self.avgdl, 1))
                score += idf * tf[term] * (self.k1 + 1) / denom
            scores.append(score)
        return _top_results(self.chunks, scores, "bm25", top_k)


class DenseRetriever:
    def __init__(self, chunks: list[Chunk], backend: str | None = None, model_name: str | None = None):
        self.chunks = chunks
        self.texts = [c.title + " " + c.text for c in chunks]
        requested_backend = backend or os.getenv("CS_RAG_DENSE_BACKEND", "tfidf")
        self.model_name = model_name or os.getenv("CS_RAG_EMBEDDING_MODEL", "BAAI/bge-small-zh-v1.5")
        self.backend = "tfidf"
        self.vectorizer: TfidfVectorizer | None = None
        self.embedding_model = None
        self.matrix = None

        if requested_backend in {"sentence-transformers", "sentence_transformers", "embedding", "auto"}:
            try:
                from sentence_transformers import SentenceTransformer

                self.embedding_model = SentenceTransformer(self.model_name)
                self.matrix = self.embedding_model.encode(
                    self.texts,
                    normalize_embeddings=True,
                    convert_to_numpy=True,
                    show_progress_bar=False,
                )
                self.backend = "sentence_transformers"
                return
            except Exception as exc:
                if requested_backend != "auto":
                    print(f"Falling back to TF-IDF dense retriever: {exc}")

        self.vectorizer = TfidfVectorizer(tokenizer=tokenize, token_pattern=None, ngram_range=(1, 2))
        self.matrix = self.vectorizer.fit_transform(self.texts)

    def search(self, query: str, top_k: int = 5) -> list[SearchResult]:
        if self.backend == "sentence_transformers":
            qv = self.embedding_model.encode(
                [query],
                normalize_embeddings=True,
                convert_to_numpy=True,
                show_progress_bar=False,
            )[0]
            scores = self.matrix @ qv
            return _top_results(self.chunks, scores.tolist(), f"dense_embedding:{self.model_name}", top_k)

        assert self.vectorizer is not None
        qv = self.vectorizer.transform([query])
        scores = (self.matrix @ qv.T).toarray().ravel()
        return _top_results(self.chunks, scores.tolist(), "dense_tfidf", top_k)


def rrf_fuse(result_sets: list[list[SearchResult]], top_k: int = 5, c: int = 60) -> list[SearchResult]:
    scores: dict[str, float] = defaultdict(float)
    chunks: dict[str, Chunk] = {}
    sources: dict[str, list[str]] = defaultdict(list)
    for results in result_sets:
        for rank, result in enumerate(results, start=1):
            scores[result.chunk.id] += 1 / (c + rank)
            chunks[result.chunk.id] = result.chunk
            sources[result.chunk.id].append(result.source)
    ranked = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)[:top_k]
    return [SearchResult(chunks[cid], score, "+".join(sorted(set(sources[cid])))) for cid, score in ranked]


def _top_results(chunks: list[Chunk], scores: list[float], source: str, top_k: int) -> list[SearchResult]:
    order = np.argsort(scores)[::-1][:top_k]
    return [SearchResult(chunks[i], float(scores[i]), source) for i in order if scores[i] > 0]
