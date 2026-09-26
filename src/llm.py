import ollama

from src.config import LLM_MODEL, OLLAMA_HOST


def generate(prompt: str, system: str | None = None) -> str:
    client = ollama.Client(host=OLLAMA_HOST)
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    response = client.chat(model=LLM_MODEL, messages=messages)
    return response["message"]["content"]
