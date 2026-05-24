from __future__ import annotations

from typing import Optional, TypedDict

from pydantic import BaseModel, Field

from app.schemas.documents import DocumentStageOutput, GeneratedDocument
from app.schemas.requests import TechStackPreference
from app.schemas.responses import ApiError


class UserInput(BaseModel):
    idea: str
    preferred_tech_stack: Optional[TechStackPreference] = None
    output_dir: Optional[str] = None
    overwrite: bool = False


class ProjectAssumption(BaseModel):
    assumption: str
    reason: str
    impact: str


class ValidationNote(BaseModel):
    target: str
    severity: str
    message: str
    suggested_fix: Optional[str] = None


class RunManifest(BaseModel):
    run_id: str
    status: str
    input_summary: str
    output_dir: str
    files: list[str] = Field(default_factory=list)
    created_at: str
    completed_at: Optional[str] = None
    errors: Optional[list[ApiError]] = None


class MVPilotState(TypedDict, total=False):
    run_id: str
    user_input: UserInput
    assumptions: list[ProjectAssumption]
    core_understanding_stage: dict[str, DocumentStageOutput]
    modeling_stage: dict[str, DocumentStageOutput]
    architecture_stage: dict[str, DocumentStageOutput]
    planning_stage: dict[str, DocumentStageOutput]
    validation_stage: dict[str, DocumentStageOutput]
    documents: list[GeneratedDocument]
    errors: list[ApiError]
