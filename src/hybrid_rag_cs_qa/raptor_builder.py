from __future__ import annotations

import math
import warnings
from dataclasses import dataclass

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.mixture import GaussianMixture

from .raptor_schema import RaptorNode, RaptorTree
from .schema import Chunk
from .summarizers import BaseSummarizer, ExtractiveSummarizer
from .text import tokenize


@dataclass(frozen=True)
class RaptorBuildConfig:
    max_layers: int = 4
    max_cluster_size: int = 8
    min_cluster_size: int = 2
    max_summary_tokens: int = 120
    max_gmm_clusters: int = 12
    random_state: int = 224


class RaptorTreeBuilder:
    def __init__(
        self,
        summarizer: BaseSummarizer | None = None,
        config: RaptorBuildConfig | None = None,
    ):
        self.summarizer = summarizer or ExtractiveSummarizer()
        self.config = config or RaptorBuildConfig()

    def build(self, chunks: list[Chunk]) -> RaptorTree:
        if not chunks:
            return RaptorTree(nodes={}, root_ids=(), leaf_ids=(), layer_to_node_ids={})

        nodes: dict[str, RaptorNode] = {}
        chunk_by_id = {chunk.id: chunk for chunk in chunks}
        current_ids: list[str] = []
        layer_to_node_ids: dict[int, tuple[str, ...]] = {}

        for chunk in chunks:
            node = RaptorNode(
                id=f"leaf:{chunk.id}",
                level=0,
                text=f"{chunk.title}\n{chunk.text}",
                children=(),
                source_chunk_ids=(chunk.id,),
                kind="leaf",
            )
            nodes[node.id] = node
            current_ids.append(node.id)

        leaf_ids = tuple(current_ids)
        layer_to_node_ids[0] = leaf_ids

        for level in range(1, self.config.max_layers + 1):
            if len(current_ids) < self.config.min_cluster_size:
                break

            current_nodes = [nodes[node_id] for node_id in current_ids]
            clusters = self._cluster(current_nodes)
            if len(clusters) <= 1 and len(current_ids) <= self.config.max_cluster_size:
                break

            next_ids: list[str] = []
            for cluster_idx, cluster in enumerate(clusters):
                if not cluster:
                    continue
                child_ids = tuple(node.id for node in cluster)
                source_ids = tuple(
                    dict.fromkeys(
                        source_id
                        for node in cluster
                        for source_id in node.source_chunk_ids
                    )
                )
                summary = self.summarizer.summarize(
                    [node.text for node in cluster],
                    max_tokens=self.config.max_summary_tokens,
                )
                summary = self._summary_with_retrieval_hints(summary, source_ids, chunk_by_id)
                node_id = f"summary:l{level}:{cluster_idx:03d}"
                nodes[node_id] = RaptorNode(
                    id=node_id,
                    level=level,
                    text=summary,
                    children=child_ids,
                    source_chunk_ids=source_ids,
                    kind="summary",
                )
                next_ids.append(node_id)

            if not next_ids or tuple(next_ids) == tuple(current_ids):
                break

            layer_to_node_ids[level] = tuple(next_ids)
            current_ids = next_ids

        return RaptorTree(
            nodes=nodes,
            root_ids=tuple(current_ids),
            leaf_ids=leaf_ids,
            layer_to_node_ids=layer_to_node_ids,
        )

    @staticmethod
    def _summary_with_retrieval_hints(
        summary: str,
        source_ids: tuple[str, ...],
        chunks: dict[str, Chunk],
    ) -> str:
        source_chunks = [chunks[chunk_id] for chunk_id in source_ids if chunk_id in chunks]
        courses = sorted({chunk.course for chunk in source_chunks})
        titles = [chunk.title for chunk in source_chunks[:8]]
        concepts = sorted(
            {
                concept
                for chunk in source_chunks
                for concept in chunk.concepts
            },
            key=str.lower,
        )[:20]
        hints = [
            f"Courses: {', '.join(courses)}" if courses else "",
            f"Topics: {', '.join(titles)}" if titles else "",
            f"Concepts: {', '.join(concepts)}" if concepts else "",
            f"Source chunks: {', '.join(source_ids[:12])}",
        ]
        return "\n".join(part for part in hints + [f"Summary: {summary}"] if part)

    def _cluster(self, nodes: list[RaptorNode]) -> list[list[RaptorNode]]:
        if len(nodes) <= self.config.max_cluster_size:
            return [nodes]

        texts = [node.text for node in nodes]
        vectorizer = TfidfVectorizer(tokenizer=tokenize, token_pattern=None, ngram_range=(1, 2))
        matrix = vectorizer.fit_transform(texts).toarray()
        if matrix.shape[0] <= self.config.min_cluster_size:
            return [nodes]

        n_clusters = self._optimal_cluster_count(matrix)
        if n_clusters <= 1:
            n_clusters = max(2, math.ceil(len(nodes) / self.config.max_cluster_size))

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            model = GaussianMixture(
                n_components=min(n_clusters, len(nodes)),
                covariance_type="diag",
                random_state=self.config.random_state,
            )
            labels = model.fit_predict(matrix)

        clusters: list[list[RaptorNode]] = []
        for label in sorted(set(labels)):
            cluster = [node for node, node_label in zip(nodes, labels) if node_label == label]
            clusters.extend(self._split_oversized_cluster(cluster))
        return [cluster for cluster in clusters if cluster]

    def _optimal_cluster_count(self, matrix: np.ndarray) -> int:
        max_clusters = min(self.config.max_gmm_clusters, len(matrix) - 1)
        if max_clusters < 2:
            return 1

        best_n = 1
        best_bic = float("inf")
        for n_clusters in range(2, max_clusters + 1):
            try:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    model = GaussianMixture(
                        n_components=n_clusters,
                        covariance_type="diag",
                        random_state=self.config.random_state,
                    )
                    model.fit(matrix)
                bic = model.bic(matrix)
            except ValueError:
                continue
            if bic < best_bic:
                best_bic = bic
                best_n = n_clusters
        return best_n

    def _split_oversized_cluster(self, cluster: list[RaptorNode]) -> list[list[RaptorNode]]:
        if len(cluster) <= self.config.max_cluster_size:
            return [cluster]
        split_count = math.ceil(len(cluster) / self.config.max_cluster_size)
        return [
            cluster[idx :: split_count]
            for idx in range(split_count)
            if cluster[idx :: split_count]
        ]
