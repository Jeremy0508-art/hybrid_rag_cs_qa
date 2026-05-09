from __future__ import annotations

import json
import os
import urllib.error
import urllib.request

from .schema import SearchResult


def generate_openai_compatible_answer(question: str, results: list[SearchResult]) -> str | None:
    """Generate an answer through an OpenAI-compatible chat completions endpoint.

    Expected environment variables:
    - CS_RAG_LLM_BASE_URL, for example http://localhost:11434/v1/chat/completions
    - CS_RAG_LLM_MODEL, for example qwen2.5:7b-instruct
    - CS_RAG_LLM_API_KEY, optional for local endpoints
    """

    base_url = os.getenv("CS_RAG_LLM_BASE_URL")
    model = os.getenv("CS_RAG_LLM_MODEL", "qwen2.5:7b-instruct")
    api_key = os.getenv("CS_RAG_LLM_API_KEY", "local")
    if not base_url:
        return None

    context = format_context(results)
    payload = {
        "model": model,
        "temperature": 0.1,
        "messages": [
            {
                "role": "system",
                "content": (
                    "你是严谨的计算机课程问答助手。只能依据给定证据回答。"
                    "每个关键结论后必须引用对应证据 ID，格式如 [chunk-id]。"
                    "如果证据不足，请明确说明证据不足。"
                ),
            },
            {
                "role": "user",
                "content": f"问题：{question}\n\n证据：\n{context}\n\n请给出简洁中文答案。",
            },
        ],
    }
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        base_url,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            obj = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        return None

    choices = obj.get("choices", [])
    if not choices:
        return None
    message = choices[0].get("message", {})
    content = message.get("content")
    return content.strip() if isinstance(content, str) and content.strip() else None


def format_context(results: list[SearchResult]) -> str:
    lines = []
    for result in results:
        lines.append(
            f"[{result.chunk.id}] 课程：{result.chunk.course}；标题：{result.chunk.title}\n{result.chunk.text}"
        )
    return "\n\n".join(lines)
