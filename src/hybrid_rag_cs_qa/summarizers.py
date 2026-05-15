from __future__ import annotations

from abc import ABC, abstractmethod

from .data import extract_concepts
from .text import tokenize


class BaseSummarizer(ABC):
    @abstractmethod
    def summarize(self, texts: list[str], max_tokens: int = 120) -> str:
        pass


class ExtractiveSummarizer(BaseSummarizer):
    def summarize(self, texts: list[str], max_tokens: int = 120) -> str:
        candidates = _sentence_candidates(texts)
        if not candidates:
            return ""

        all_text = " ".join(texts)
        global_tokens = set(tokenize(all_text))
        concepts = set(extract_concepts(all_text))

        scored: list[tuple[float, int, str]] = []
        for idx, sentence in enumerate(candidates):
            sentence_tokens = set(tokenize(sentence))
            overlap = len(sentence_tokens & global_tokens)
            concept_hits = sum(1 for concept in concepts if concept in sentence)
            score = overlap + 3.0 * concept_hits + 1.0 / (idx + 1)
            scored.append((score, idx, sentence))

        picked = sorted(scored, key=lambda item: (-item[0], item[1]))
        summary_parts: list[str] = []
        used_tokens = 0
        for _, _, sentence in picked:
            sentence_len = max(1, len(tokenize(sentence)))
            if summary_parts and used_tokens + sentence_len > max_tokens:
                continue
            summary_parts.append(sentence)
            used_tokens += sentence_len
            if used_tokens >= max_tokens:
                break

        summary = " ".join(summary_parts)
        return summary or candidates[0]


def _sentence_candidates(texts: list[str]) -> list[str]:
    candidates: list[str] = []
    for text in texts:
        for sentence in text.replace("\n", " ").split("。"):
            sentence = sentence.strip()
            if sentence:
                candidates.append(sentence + ("。" if any("\u4e00" <= ch <= "\u9fff" for ch in sentence) else ""))
    return candidates
