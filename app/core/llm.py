from __future__ import annotations

from typing import Protocol


class LLMClient(Protocol):
    def generate(self, prompt: str) -> str:
        """Generate text for a prompt."""


class OpenAILLM:
    def __init__(self, base_url: str, api_key: str, model_name: str) -> None:
        pass

    def generate(self, prompt: str) -> str:
        pass


class DeepSeekLLM:
    def __init__(self, base_url: str, api_key: str, model_name: str) -> None:
        pass

    def generate(self, prompt: str) -> str:
        pass    


def get_llm_client() -> LLMClient:
    # return OpenAILLM(...)
    # return DeepSeekLLM(...)
    pass
