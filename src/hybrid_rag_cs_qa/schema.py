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
    topic: str = "unknown"
    subtopic: str = "unknown"
    expected_concepts: tuple[str, ...] = field(default_factory=tuple)
    requires_multi_hop: bool = False
    answer_style: str = "unknown"


@dataclass(frozen=True)
class SearchResult:
    chunk: Chunk
    score: float
    source: str
