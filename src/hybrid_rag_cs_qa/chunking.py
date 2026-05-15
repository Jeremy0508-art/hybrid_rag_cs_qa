from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable

from .data import extract_concepts, slug
from .schema import Chunk
from .text import tokenize


class ChunkingStrategy(str, Enum):
    SECTION = "section"
    PARAGRAPH = "paragraph"
    SLIDING_WINDOW = "sliding_window"


@dataclass(frozen=True)
class ChunkDocument:
    id: str
    course: str
    title: str
    text: str
    concepts: tuple[str, ...] = field(default_factory=tuple)


def documents_from_markdown(raw: str) -> list[ChunkDocument]:
    sections = re.split(r"\n(?=## )", raw)
    documents: list[ChunkDocument] = []
    for section in sections:
        lines = [line.strip() for line in section.splitlines() if line.strip()]
        if not lines or not lines[0].startswith("## "):
            continue
        header = lines[0].removeprefix("## ").strip()
        course, _, title = header.partition(" / ")
        body = " ".join(lines[1:])
        doc_id = f"{slug(course)}-{slug(title or course)}"
        documents.append(
            ChunkDocument(
                id=doc_id,
                course=course,
                title=title or course,
                text=body,
                concepts=extract_concepts(f"{header} {body}"),
            )
        )
    return documents


def chunk_documents(
    documents: Iterable[ChunkDocument],
    strategy: ChunkingStrategy = ChunkingStrategy.SECTION,
    max_tokens: int = 120,
    overlap: int = 24,
) -> list[Chunk]:
    if max_tokens < 16:
        raise ValueError("max_tokens must be at least 16")
    if overlap < 0 or overlap >= max_tokens:
        raise ValueError("overlap must be non-negative and smaller than max_tokens")

    chunks: list[Chunk] = []
    for document in documents:
        if strategy == ChunkingStrategy.SECTION:
            chunks.append(_make_chunk(document, document.id, document.text))
        elif strategy == ChunkingStrategy.PARAGRAPH:
            chunks.extend(_paragraph_chunks(document))
        elif strategy == ChunkingStrategy.SLIDING_WINDOW:
            chunks.extend(_sliding_window_chunks(document, max_tokens=max_tokens, overlap=overlap))
        else:
            raise ValueError(f"Unknown chunking strategy: {strategy}")
    return chunks


def _paragraph_chunks(document: ChunkDocument) -> list[Chunk]:
    parts = [part.strip() for part in re.split(r"\n{2,}|(?<=[.!?;:])\s+", document.text) if part.strip()]
    if not parts:
        return [_make_chunk(document, f"{document.id}-p000", document.text)]
    return [
        _make_chunk(document, f"{document.id}-p{idx:03d}", part)
        for idx, part in enumerate(parts)
    ]


def _sliding_window_chunks(document: ChunkDocument, max_tokens: int, overlap: int) -> list[Chunk]:
    tokens = tokenize(document.text)
    if not tokens:
        return [_make_chunk(document, f"{document.id}-w000", document.text)]
    step = max_tokens - overlap
    chunks: list[Chunk] = []
    for idx, start in enumerate(range(0, len(tokens), step)):
        window = tokens[start : start + max_tokens]
        if not window:
            continue
        chunks.append(_make_chunk(document, f"{document.id}-w{idx:03d}", " ".join(window)))
        if start + max_tokens >= len(tokens):
            break
    return chunks


def _make_chunk(document: ChunkDocument, chunk_id: str, text: str) -> Chunk:
    concepts = extract_concepts(f"{document.course} {document.title} {text}")
    return Chunk(
        id=chunk_id,
        course=document.course,
        title=document.title,
        text=text,
        concepts=concepts or document.concepts,
    )
