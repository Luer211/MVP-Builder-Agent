from __future__ import annotations

from openai import OpenAI

from app.core.config import Settings


# Todo: 目前只实现了OpenAI的接入，后续应该支持更多模型公司的API
class LLMClient:
    def __init__(self, api_key: str, base_url: str, model_name: str, timeout_seconds: int):
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout_seconds,
        )
        self.model_name = model_name

    def generate(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            response_format={"type": "json_object"},
        )

        content = response.choices[0].message.content

        return content


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


def get_llm_client(settings: Settings) -> LLMClient:
    """创建 LLMClient 实例"""
    return LLMClient(
        api_key=settings.api_key,
        base_url=settings.base_url,
        model_name=settings.model_name,
        timeout_seconds=settings.request_timeout_seconds,
    )
