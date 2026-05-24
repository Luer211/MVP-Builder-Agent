from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class TechStackPreference(BaseModel):
    backend_language: Optional[str] = None
    framework: Optional[str] = None
    database: Optional[str] = None
    cache: Optional[str] = None
    deployment: Optional[str] = None


class GenerateDocsRequest(BaseModel):
    idea: str = Field(description="Raw product idea or business requirement.")
    preferred_tech_stack: Optional[TechStackPreference] = None
    output_dir: Optional[str] = None
    overwrite: bool = False
