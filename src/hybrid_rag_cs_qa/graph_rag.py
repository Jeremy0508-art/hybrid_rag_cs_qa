from __future__ import annotations

from collections import Counter

import networkx as nx

from .data import extract_concepts
from .schema import Chunk, SearchResult


def build_concept_graph(chunks: list[Chunk]) -> nx.Graph:
    graph = nx.Graph()
    for chunk in chunks:
        for concept in chunk.concepts:
            graph.add_node(concept, kind="concept")
            graph.add_edge(concept, chunk.id, kind="mentions", weight=1.0)
        for i, left in enumerate(chunk.concepts):
            for right in chunk.concepts[i + 1 :]:
                weight = graph.get_edge_data(left, right, default={}).get("weight", 0.0) + 1.0
                graph.add_edge(left, right, kind="co_occurs", weight=weight)
    return graph


class GraphExpander:
    def __init__(self, chunks: list[Chunk]):
        self.chunks = {chunk.id: chunk for chunk in chunks}
        self.graph = build_concept_graph(chunks)

    def expand(self, query: str, top_k: int = 5) -> list[SearchResult]:
        query_concepts = extract_concepts(query)
        votes: Counter[str] = Counter()
        for concept in query_concepts:
            if concept not in self.graph:
                continue
            for neighbor in self.graph.neighbors(concept):
                if neighbor in self.chunks:
                    votes[neighbor] += 2
                else:
                    for second_hop in self.graph.neighbors(neighbor):
                        if second_hop in self.chunks:
                            votes[second_hop] += 1
        return [
            SearchResult(self.chunks[cid], float(score), "graph")
            for cid, score in votes.most_common(top_k)
        ]
