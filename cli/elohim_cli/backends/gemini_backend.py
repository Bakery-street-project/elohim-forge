import httpx
from .base import BaseBackend

# Uses Google's OpenAI-compatible endpoint so the schema is identical to NIM/OpenAI.
_GEMINI_COMPAT_URL = "https://generativelanguage.googleapis.com/v1beta/openai"


class GeminiBackend(BaseBackend):
    def __init__(self, api_key: str, model: str = "gemini-2.0-flash"):
        self.api_key = api_key
        self.model = model

    @property
    def name(self) -> str:
        return f"Gemini ({self.model})"

    def chat(self, messages: list[dict], system: str = "") -> str:
        payload_messages = []
        if system:
            payload_messages.append({"role": "system", "content": system})
        payload_messages.extend(messages)

        resp = httpx.post(
            f"{_GEMINI_COMPAT_URL}/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json={"model": self.model, "messages": payload_messages, "max_tokens": 2048},
            timeout=60.0,
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]
