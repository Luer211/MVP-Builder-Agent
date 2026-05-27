from __future__ import annotations

from functools import lru_cache
import os
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class Settings(BaseModel):
    app_name: str = Field(default="MVP Builder Agent", alias="APP_NAME")
    env: str = Field(default="local", alias="ENV")
    output_root: Path = Field(default=Path("test_docs"), alias="OUTPUT_ROOT")
    base_url: Optional[str] = Field(default=None, alias="BASE_URL")
    api_key: Optional[str] = Field(default=None, alias="API_KEY")
    model_name: str = Field(default=None, alias="MODEL_NAME")
    request_timeout_seconds: int = Field(default=120, alias="REQUEST_TIMEOUT_SECONDS")


@lru_cache
def get_settings() -> Settings:
    return Settings(
        app_name=os.getenv("APP_NAME", "MVP Builder Agent"),
        env=os.getenv("ENV", "local"),
        output_root=Path(os.getenv("OUTPUT_ROOT", "test_docs")),
        base_url=os.getenv("BASE_URL"),
        api_key=os.getenv("API_KEY"),
        model_name=os.getenv("MODEL_NAME"),
        request_timeout_seconds=int(os.getenv("REQUEST_TIMEOUT_SECONDS", "120")),
    )
