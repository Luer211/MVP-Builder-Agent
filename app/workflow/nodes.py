from __future__ import annotations

from collections.abc import Callable

from app.core.llm import LLMClient
from app.schemas.documents import DocumentSpec, DocumentStageOutput, GeneratedDocument, MarkdownSection
from app.schemas.requests import TechStackPreference
from app.schemas.state import MVPilotState
from app.workflow.prompts import build_document_prompt


STAGE_KEY_BY_SOURCE_STAGE = {
    "core_understanding": "core_understanding_stage",
    "modeling": "modeling_stage",
    "architecture": "architecture_stage",
    "planning": "planning_stage",
    "validation": "validation_stage",
}


def idea_intake_node(state: MVPilotState) -> MVPilotState:
    return {
        "assumptions": [],
        "core_understanding_stage": {},
        "modeling_stage": {},
        "architecture_stage": {},
        "planning_stage": {},
        "validation_stage": {},
        "errors": [],
    }


def build_document_node(
    spec: DocumentSpec,
    llm: LLMClient,
) -> Callable[[MVPilotState], MVPilotState]:
    def node(state: MVPilotState) -> MVPilotState:
        prompt = build_document_prompt(state=state, spec=spec)
        raw_output = llm.generate(prompt)

        output = DocumentStageOutput.model_validate_json(raw_output)
        validate_output_matches_spec(output, spec)

        stage_key = stage_key_for(spec)
        stage_outputs = dict(state.get(stage_key, {}))
        stage_outputs[spec.file_name] = output

        return {stage_key: stage_outputs}

    node.__name__ = spec.node_name
    return node


def validate_output_matches_spec(output: DocumentStageOutput, spec: DocumentSpec) -> None:
    """检验输出是否符合规范"""
    
    if output.file_name != spec.file_name:
        raise ValueError(
            f"LLM output file_name mismatch: expected {spec.file_name}, got {output.file_name}."
        )

    if output.title != spec.title:
        raise ValueError(
            f"LLM output title mismatch: expected {spec.title}, got {output.title}."
        )

    if output.source_stage != spec.source_stage:
        raise ValueError(
            f"LLM output source_stage mismatch: expected {spec.source_stage}, got {output.source_stage}."
        )

    actual_headings = [section.heading for section in output.sections]
    expected_headings = spec.section_headings
    if actual_headings != expected_headings:
        raise ValueError(
            "LLM output section headings mismatch: "
            f"expected {expected_headings}, got {actual_headings}."
        )


def stage_key_for(spec: DocumentSpec) -> str:
    return STAGE_KEY_BY_SOURCE_STAGE[spec.source_stage]
