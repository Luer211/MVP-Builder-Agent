from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """从环境变量或.env文件读取配置；若不存在，则使用 default"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = Field(default="MVP Builder Agent", alias="APP_NAME")
    env: str = Field(default="local", alias="ENV")
    output_root: Path = Field(default=Path("test_docs"), alias="OUTPUT_ROOT")
    base_url: Optional[str] = Field(default=None, alias="BASE_URL")
    api_key: Optional[str] = Field(default=None, alias="API_KEY")
    model_name: Optional[str] = Field(default=None, alias="MODEL_NAME")
    request_timeout_seconds: int = Field(default=120, alias="REQUEST_TIMEOUT_SECONDS")


@lru_cache
def get_settings() -> Settings:
    return Settings()
