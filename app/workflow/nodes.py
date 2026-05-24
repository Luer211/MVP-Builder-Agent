from __future__ import annotations

from collections.abc import Callable
from typing import Optional

from app.schemas.documents import DocumentSpec, DocumentStageOutput, GeneratedDocument, MarkdownSection
from app.schemas.requests import TechStackPreference
from app.schemas.state import MVPilotState, ProjectAssumption


def _tech_stack_text(preference: Optional[TechStackPreference]) -> str:
    if preference is None:
        return "Python, FastAPI, LangGraph, Pydantic, local filesystem storage"

    parts = [
        preference.backend_language,
        preference.framework,
        preference.database,
        preference.cache,
        preference.deployment,
    ]
    selected = [part for part in parts if part]
    return ", ".join(selected) if selected else "Python, FastAPI, LangGraph, Pydantic"


def _assumption_text(state: MVPilotState) -> list[str]:
    return [item.assumption for item in state.get("assumptions", [])]


def _stage_key(spec: DocumentSpec) -> str:
    return f"{spec.source_stage}_stage"


def _section_body(spec: DocumentSpec, heading: str, idea: str, tech_stack: str) -> list[str]:
    if heading == "Recommended Tech Stack":
        return [f"- Preferred stack: {tech_stack}."]
    if heading == "Output Summary":
        return ["- Generate the fixed 12 Markdown files from the document registry."]
    if heading == "Directory Structure":
        return [
            "- Keep API, services, workflow, schemas, rendering, and storage in separate packages.",
            "- Keep generated docs under the configured output directory.",
        ]
    if heading == "Core Endpoints":
        return [
            "- POST /api/v1/doc-runs",
            "- GET /api/v1/doc-runs/{run_id}",
            "- GET /api/v1/doc-runs/{run_id}/files",
            "- GET /api/v1/doc-runs/{run_id}/files/{file_name}",
        ]
    if heading.startswith("Milestone"):
        return [f"- Build the {heading.split(':', 1)[-1].strip().lower()} needed for the MVP docs loop."]
    if heading.startswith("V"):
        return [f"- Use this phase to evolve the project after the stable docs generation loop works."]
    return [
        f"- Draft this section for the product idea: {idea}",
        f"- Keep the content aligned with {spec.title} and the MVP docs generation boundary.",
    ]


def build_document_output(state: MVPilotState, spec: DocumentSpec) -> DocumentStageOutput:
    user_input = state["user_input"]
    idea = user_input.idea
    tech_stack = _tech_stack_text(user_input.preferred_tech_stack)
    sections = [
        MarkdownSection(heading=heading, body=_section_body(spec, heading, idea, tech_stack))
        for heading in spec.section_headings
    ]
    return DocumentStageOutput(
        file_name=spec.file_name,
        title=spec.title,
        source_stage=spec.source_stage,
        summary=f"{spec.title} for: {idea}",
        assumptions=_assumption_text(state),
        sections=sections,
    )


def build_document_node(spec: DocumentSpec) -> Callable[[MVPilotState], MVPilotState]:
    def node(state: MVPilotState) -> MVPilotState:
        output = build_document_output(state, spec)
        stage_key = _stage_key(spec)
        stage_outputs = dict(state.get(stage_key, {}))
        stage_outputs[spec.file_name] = output

        documents = list(state.get("documents", []))
        documents.append(
            GeneratedDocument(
                file_name=output.file_name,
                title=output.title,
                content="",
                source_stage=output.source_stage,
            )
        )

        return {stage_key: stage_outputs, "documents": documents}

    node.__name__ = spec.node_name
    return node


def initial_assumptions(state: MVPilotState) -> list[ProjectAssumption]:
    user_input = state["user_input"]
    assumptions: list[ProjectAssumption] = []
    if user_input.preferred_tech_stack is None:
        assumptions.append(
            ProjectAssumption(
                assumption="No explicit technology stack was provided, so the generator uses the default Python/FastAPI/LangGraph stack.",
                reason="The MVP docs need a concrete engineering baseline.",
                impact="Generated architecture and project skeleton will reference the default stack.",
            )
        )
    return assumptions


def idea_intake_node(state: MVPilotState) -> MVPilotState:
    return {
        "assumptions": initial_assumptions(state),
        "core_understanding_stage": {},
        "modeling_stage": {},
        "architecture_stage": {},
        "planning_stage": {},
        "validation_stage": {},
        "documents": [],
        "errors": [],
    }
