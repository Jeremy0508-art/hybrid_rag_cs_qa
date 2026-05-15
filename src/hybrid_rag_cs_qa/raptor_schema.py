from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class RaptorNode:
    id: str
    level: int
    text: str
    children: tuple[str, ...] = field(default_factory=tuple)
    source_chunk_ids: tuple[str, ...] = field(default_factory=tuple)
    kind: str = "summary"


@dataclass(frozen=True)
class RaptorTree:
    nodes: dict[str, RaptorNode]
    root_ids: tuple[str, ...]
    leaf_ids: tuple[str, ...]
    layer_to_node_ids: dict[int, tuple[str, ...]]
    source: str = "hybrid_rag_cs_qa"

    def leaves_for(self, node_id: str) -> tuple[str, ...]:
        node = self.nodes[node_id]
        if node.kind == "leaf":
            return node.source_chunk_ids
        leaf_ids: list[str] = []
        stack = list(node.children)
        while stack:
            current_id = stack.pop()
            current = self.nodes[current_id]
            if current.kind == "leaf":
                leaf_ids.extend(current.source_chunk_ids)
            else:
                stack.extend(current.children)
        return tuple(dict.fromkeys(leaf_ids))
