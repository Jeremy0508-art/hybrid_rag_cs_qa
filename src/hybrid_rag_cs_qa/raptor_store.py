from __future__ import annotations

import json
from pathlib import Path

from .raptor_schema import RaptorNode, RaptorTree


def save_raptor_tree(tree: RaptorTree, path: Path) -> None:
    payload = {
        "source": tree.source,
        "root_ids": list(tree.root_ids),
        "leaf_ids": list(tree.leaf_ids),
        "layer_to_node_ids": {
            str(level): list(node_ids)
            for level, node_ids in tree.layer_to_node_ids.items()
        },
        "nodes": [
            {
                "id": node.id,
                "level": node.level,
                "text": node.text,
                "children": list(node.children),
                "source_chunk_ids": list(node.source_chunk_ids),
                "kind": node.kind,
            }
            for node in tree.nodes.values()
        ],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def load_raptor_tree(path: Path) -> RaptorTree:
    payload = json.loads(path.read_text(encoding="utf-8"))
    nodes = {
        obj["id"]: RaptorNode(
            id=obj["id"],
            level=int(obj["level"]),
            text=obj["text"],
            children=tuple(obj.get("children", [])),
            source_chunk_ids=tuple(obj.get("source_chunk_ids", [])),
            kind=obj.get("kind", "summary"),
        )
        for obj in payload.get("nodes", [])
    }
    return RaptorTree(
        nodes=nodes,
        root_ids=tuple(payload.get("root_ids", [])),
        leaf_ids=tuple(payload.get("leaf_ids", [])),
        layer_to_node_ids={
            int(level): tuple(node_ids)
            for level, node_ids in payload.get("layer_to_node_ids", {}).items()
        },
        source=payload.get("source", "hybrid_rag_cs_qa"),
    )
