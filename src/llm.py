import re

import httpx

from src.config import LLM_MODEL, LLM_SEED, OLLAMA_HOST


def _strip_think(text: str) -> str:
    # deepseek-r1 wraps its reply in <think>...</think> — strip that out before returning.
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()


# Ollama exposes an OpenAI-compatible /v1/chat/completions endpoint
def generate(prompt: str, system: str | None = None, model: str | None = None) -> str:
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    response = httpx.post(
        f"{OLLAMA_HOST}/v1/chat/completions",
        json={"model": model or LLM_MODEL, "messages": messages, "seed": LLM_SEED},
        timeout=None,
    )
    response.raise_for_status()
    text = response.json()["choices"][0]["message"]["content"]
    return _strip_think(text)
