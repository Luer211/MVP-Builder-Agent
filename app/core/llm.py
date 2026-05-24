from __future__ import annotations

from typing import Protocol


class LLMClient(Protocol):
    def generate(self, prompt: str) -> str:
        """Generate text for a prompt."""


class LocalDeterministicLLM:
    """Placeholder LLM client for the first skeleton.

    The workflow is wired so this can be swapped for a real model client later.
    """

    def generate(self, prompt: str) -> str:
        return prompt


def get_llm_client() -> LLMClient:
    return LocalDeterministicLLM()
