import re

import ollama

from src.config import LLM_MODEL, LLM_SEED, OLLAMA_HOST


def _strip_think(text: str) -> str:
    # deepseek-r1 wraps its reply in <think>...</think> — strip that out before returning.
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()


def generate(prompt: str, system: str | None = None, model: str | None = None) -> str:
    client = ollama.Client(host=OLLAMA_HOST)
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    response = client.chat(model=model or LLM_MODEL, messages=messages, options={"seed": LLM_SEED})
    return _strip_think(response["message"]["content"])
