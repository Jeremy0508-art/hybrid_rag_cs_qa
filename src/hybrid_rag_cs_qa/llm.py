from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass

from .schema import SearchResult


@dataclass(frozen=True)
class LlmStatus:
    ok: bool
    message: str
    models: tuple[str, ...] = ()


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


def check_ollama(base_api_url: str = "http://localhost:11434/api/tags") -> LlmStatus:
    try:
        with urllib.request.urlopen(base_api_url, timeout=5) as response:
            obj = json.loads(response.read().decode("utf-8"))
    except urllib.error.URLError as exc:
        return LlmStatus(False, f"Ollama API is not reachable: {exc}")
    except (TimeoutError, json.JSONDecodeError) as exc:
        return LlmStatus(False, f"Ollama API responded unexpectedly: {exc}")

    models = tuple(model.get("name", "") for model in obj.get("models", []) if model.get("name"))
    if not models:
        return LlmStatus(False, "Ollama is running, but no local models were found.")
    return LlmStatus(True, "Ollama is running.", models)


def print_llm_status() -> None:
    status = check_ollama()
    print(status.message)
    if status.models:
        print("Models:")
        for model in status.models:
            print(f"- {model}")
    print("\nExpected environment for generation:")
    print('$env:CS_RAG_LLM_BASE_URL="http://localhost:11434/v1/chat/completions"')
    if status.models:
        print(f'$env:CS_RAG_LLM_MODEL="{status.models[0]}"')
    else:
        print('$env:CS_RAG_LLM_MODEL="qwen2.5:7b-instruct"')
