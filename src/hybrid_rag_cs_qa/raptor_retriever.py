from __future__ import annotations

from collections import defaultdict
import re

from sklearn.feature_extraction.text import TfidfVectorizer

from .raptor_schema import RaptorNode, RaptorTree
from .schema import Chunk, SearchResult
from .text import tokenize


class RaptorRetriever:
    ASPECT_ORDER = ("Foundations", "Mechanisms", "Tradeoffs", "Applications", "Evaluation")

    def __init__(self, chunks: list[Chunk], tree: RaptorTree):
        self.chunks = {chunk.id: chunk for chunk in chunks}
        self.sibling_chunks = self._build_sibling_chunks(chunks)
        self.tree = tree
        self.parent_by_child = {
            child_id: node.id
            for node in tree.nodes.values()
            for child_id in node.children
        }
        self.leaf_id_by_chunk_id = {
            node.source_chunk_ids[0]: node.id
            for node in tree.nodes.values()
            if node.kind == "leaf" and node.source_chunk_ids
        }
        self.node_ids = sorted(tree.nodes, key=lambda node_id: (tree.nodes[node_id].level, node_id))
        self.node_positions = {node_id: idx for idx, node_id in enumerate(self.node_ids)}
        self.vectorizer = TfidfVectorizer(tokenizer=tokenize, token_pattern=None, ngram_range=(1, 2))
        texts = [self._retrieval_text(tree.nodes[node_id]) for node_id in self.node_ids]
        self.matrix = self.vectorizer.fit_transform(texts) if texts else None

    def search(
        self,
        query: str,
        top_k: int = 5,
        node_top_k: int | None = None,
        mode: str = "collapsed",
    ) -> list[SearchResult]:
        if not self.node_ids or self.matrix is None:
            return []
        if mode == "topdown":
            return self._search_topdown(query, top_k=top_k, beam_width=node_top_k or max(top_k, 3))
        if mode != "collapsed":
            raise ValueError(f"Unknown RAPTOR retrieval mode: {mode}")
        return self._search_collapsed(query, top_k=top_k, node_top_k=node_top_k or max(top_k * 3, 10))

    def _search_collapsed(self, query: str, top_k: int, node_top_k: int) -> list[SearchResult]:
        node_scores = self._score_nodes(query, self.node_ids)
        ranked = sorted(node_scores.items(), key=lambda item: item[1], reverse=True)[:node_top_k]
        leaf_ranked = self._rank_nodes(query, list(self.tree.leaf_ids), limit=max(top_k * 2, 10))
        title_seed = self._title_seed_nodes(query)
        blended = title_seed + [(node_id, score * 1.15) for node_id, score in leaf_ranked] + ranked
        return self._expand_ranked_nodes(query, blended, top_k=top_k, summary_weight=0.8)

    def _search_topdown(self, query: str, top_k: int, beam_width: int) -> list[SearchResult]:
        query_variants = self._query_variants(query)
        title_seed = self._title_seed_nodes(query)
        collapsed_seed = title_seed + self._rank_nodes_multi(query_variants, self.node_ids, limit=max(beam_width * 4, top_k * 4))
        current_ids = self._seed_roots(collapsed_seed, beam_width)
        selected: list[tuple[str, float]] = []
        path_scores = {node_id: 1.0 for node_id in current_ids}
        while current_ids:
            scores = self._score_nodes_multi(query_variants, current_ids)
            ranked = sorted(
                (
                    (node_id, score + 0.15 * path_scores.get(node_id, 0.0))
                    for node_id, score in scores.items()
                ),
                key=lambda item: item[1],
                reverse=True,
            )[:beam_width]
            if not ranked:
                break
            selected.extend(ranked)
            next_ids: list[str] = []
            next_path_scores: dict[str, float] = {}
            for node_id, score in ranked:
                for child_id in self.tree.nodes[node_id].children:
                    next_ids.append(child_id)
                    next_path_scores[child_id] = max(next_path_scores.get(child_id, 0.0), score)
            if not next_ids:
                break
            current_ids = list(dict.fromkeys(next_ids))
            path_scores = next_path_scores
        if not selected:
            return self._search_collapsed(query, top_k=top_k, node_top_k=max(beam_width * 2, top_k))
        blended = [(node_id, score * 0.9) for node_id, score in collapsed_seed[: max(top_k * 2, beam_width)]] + selected
        return self._expand_ranked_nodes(query, blended, top_k=top_k, summary_weight=0.45)

    def _score_nodes(self, query: str, node_ids: list[str]) -> dict[str, float]:
        return dict(self._rank_nodes(query, node_ids, limit=len(node_ids)))

    def _score_nodes_multi(self, queries: list[str], node_ids: list[str]) -> dict[str, float]:
        return dict(self._rank_nodes_multi(queries, node_ids, limit=len(node_ids)))

    def _rank_nodes_multi(self, queries: list[str], node_ids: list[str], limit: int) -> list[tuple[str, float]]:
        scores: dict[str, float] = defaultdict(float)
        for query_idx, query in enumerate(queries):
            weight = 1.0 if query_idx == 0 else 0.85
            for node_id, score in self._rank_nodes(query, node_ids, limit=limit):
                scores[node_id] = max(scores[node_id], score * weight)
        return sorted(scores.items(), key=lambda item: item[1], reverse=True)[:limit]

    def _rank_nodes(self, query: str, node_ids: list[str], limit: int) -> list[tuple[str, float]]:
        qv = self.vectorizer.transform([query])
        node_positions = [self.node_positions[node_id] for node_id in node_ids]
        scores = (self.matrix[node_positions] @ qv.T).toarray().ravel()
        ranked = [
            (node_id, float(score))
            for node_id, score in zip(node_ids, scores)
            if score > 0
        ]
        return sorted(ranked, key=lambda item: item[1], reverse=True)[:limit]

    @staticmethod
    def _query_variants(query: str) -> list[str]:
        normalized = " ".join(query.split())
        variants = [normalized]
        for part in re.split(r"\s+(?:and|with|versus|vs\.?)\s+", normalized, flags=re.IGNORECASE):
            part = part.strip(" ?.,;:")
            if len(part.split()) >= 2 and part.lower() not in {v.lower() for v in variants}:
                variants.append(part)
        return variants[:4]

    def _title_seed_nodes(self, query: str) -> list[tuple[str, float]]:
        lower_query = query.lower()
        seeds: list[tuple[str, float]] = []
        for chunk in self.chunks.values():
            if chunk.title.lower() in lower_query:
                leaf_id = self.leaf_id_by_chunk_id.get(chunk.id)
                if leaf_id:
                    seeds.append((leaf_id, 2.0))
        return seeds


    def _seed_roots(self, ranked_nodes: list[tuple[str, float]], beam_width: int) -> list[str]:
        root_ids: list[str] = []
        for node_id, _ in ranked_nodes:
            root_id = self._root_for(node_id)
            if root_id not in root_ids:
                root_ids.append(root_id)
            if len(root_ids) >= beam_width:
                break
        if root_ids:
            return root_ids
        return list(self.tree.root_ids)[:beam_width]

    def _root_for(self, node_id: str) -> str:
        current_id = node_id
        while True:
            parent_id = self._parent_of(current_id)
            if parent_id is None:
                return current_id
            current_id = parent_id

    def _parent_of(self, node_id: str) -> str | None:
        return self.parent_by_child.get(node_id)

    def _expand_ranked_nodes(
        self,
        query: str,
        ranked_nodes: list[tuple[str, float]],
        top_k: int,
        summary_weight: float,
    ) -> list[SearchResult]:
        chunk_scores: dict[str, float] = defaultdict(float)
        chunk_sources: dict[str, list[str]] = defaultdict(list)
        for rank, (node_id, score) in enumerate(ranked_nodes, start=1):
            if score <= 0:
                continue
            rank_weight = 1.0 / rank
            node = self.tree.nodes[node_id]
            node_weight = 1.0 if node.kind == "leaf" else summary_weight
            for chunk_id in self.tree.leaves_for(node_id):
                if chunk_id not in self.chunks:
                    continue
                chunk_scores[chunk_id] = max(chunk_scores[chunk_id], score * rank_weight * node_weight)
                chunk_sources[chunk_id].append(f"raptor:{node_id}")

        if self._is_multi_hop_query(query):
            self._add_sibling_evidence(chunk_scores, chunk_sources)

        ranked_chunks = sorted(chunk_scores.items(), key=lambda item: item[1], reverse=True)[:top_k]
        return [
            SearchResult(
                chunk=self.chunks[chunk_id],
                score=float(score),
                source="+".join(dict.fromkeys(chunk_sources[chunk_id])),
            )
            for chunk_id, score in ranked_chunks
        ]

    @staticmethod
    def _retrieval_text(node: RaptorNode) -> str:
        source_hint = " ".join(node.source_chunk_ids)
        return f"{node.text} {source_hint}"

    @classmethod
    def _build_sibling_chunks(cls, chunks: list[Chunk]) -> dict[str, tuple[str, ...]]:
        groups: dict[tuple[str, str], list[tuple[int, str]]] = defaultdict(list)
        for chunk in chunks:
            base_title, aspect_index = cls._split_aspect(chunk.title)
            groups[(chunk.course, base_title)].append((aspect_index, chunk.id))

        siblings: dict[str, tuple[str, ...]] = {}
        for entries in groups.values():
            ordered_ids = [chunk_id for _, chunk_id in sorted(entries)]
            for idx, chunk_id in enumerate(ordered_ids):
                neighbors = []
                if idx > 0:
                    neighbors.append(ordered_ids[idx - 1])
                if idx + 1 < len(ordered_ids):
                    neighbors.append(ordered_ids[idx + 1])
                siblings[chunk_id] = tuple(neighbors)
        return siblings

    @classmethod
    def _split_aspect(cls, title: str) -> tuple[str, int]:
        for idx, aspect in enumerate(cls.ASPECT_ORDER):
            suffix = f" {aspect}"
            if title.endswith(suffix):
                return title[: -len(suffix)], idx
        return title, len(cls.ASPECT_ORDER)

    @staticmethod
    def _is_multi_hop_query(query: str) -> bool:
        lower = query.lower()
        return any(marker in lower for marker in (" combine", "combined", " both ", "multi-hop", "together"))

    def _add_sibling_evidence(
        self,
        chunk_scores: dict[str, float],
        chunk_sources: dict[str, list[str]],
        boost: float = 0.96,
    ) -> None:
        ranked = sorted(chunk_scores.items(), key=lambda item: item[1], reverse=True)
        for chunk_id, score in ranked[:8]:
            for sibling_id in self.sibling_chunks.get(chunk_id, ()):
                if sibling_id not in self.chunks:
                    continue
                sibling_score = score * boost
                if sibling_score > chunk_scores.get(sibling_id, 0.0):
                    chunk_scores[sibling_id] = sibling_score
                    chunk_sources[sibling_id].append(f"raptor:sibling:{chunk_id}")
