from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class ApiError(BaseModel):
    code: str
    message: str
    detail: Optional[dict] = None


class GenerateDocsResponse(BaseModel):
    run_id: str
    status: str
    output_dir: str
    files: list[str] = Field(default_factory=list)
    errors: Optional[list[ApiError]] = None


class RunSummaryResponse(BaseModel):
    run_id: str
    status: str
    input_summary: str
    output_dir: str
    files: list[str] = Field(default_factory=list)
    created_at: str
    completed_at: Optional[str] = None
    errors: Optional[list[ApiError]] = None


class FileListResponse(BaseModel):
    run_id: str
    files: list[str]
