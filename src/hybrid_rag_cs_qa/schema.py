from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Chunk:
    id: str
    course: str
    title: str
    text: str
    concepts: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class QAItem:
    id: str
    question: str
    answer: str
    evidence_ids: tuple[str, ...]
    difficulty: str
    question_type: str


@dataclass(frozen=True)
class SearchResult:
    chunk: Chunk
    score: float
    source: str
