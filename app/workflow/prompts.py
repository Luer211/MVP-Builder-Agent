from __future__ import annotations

import json
from typing import Any

from app.schemas.documents import DocumentSpec
from app.schemas.state import MVPilotState


STAGE_STATE_KEYS = (
    "core_understanding_stage",
    "modeling_stage",
    "architecture_stage",
    "planning_stage",
    "validation_stage",
)


def build_document_prompt(*, state: MVPilotState, spec: DocumentSpec) -> str:
    context = {
        "user_input": _user_input_payload(state),
        "assumptions": _assumptions_payload(state),
        "previous_outputs": _previous_outputs_payload(state),
        "target_document": spec.model_dump(mode="json"),
        "required_output": _required_output_shape(spec),
    }

    return f"""You are an MVP product-engineering documentation node.

Generate exactly one structured document for the target_document.

Input context:
{_to_json(context)}

Hard rules:
- Return strict JSON only.
- Do not wrap the JSON in Markdown fences.
- Do not output a Markdown document.
- Do not add fields outside the required_output shape.
- file_name, title, and source_stage must exactly match target_document.
- sections must use exactly the target_document.section_headings.
- sections must keep the same order as target_document.section_headings.
- Every section body must be a non-empty list of Markdown-compatible strings.
- Do not silently invent missing product facts.
- If an assumption is necessary, include it in the assumptions list.
- Use previous_outputs as context only; keep this document focused on its own title.
- Keep section headings exactly as specified, but write section body content in the user's language when possible.
"""


def _user_input_payload(state: MVPilotState) -> dict[str, Any]:
    return state["user_input"].model_dump(mode="json", exclude_none=True)


def _assumptions_payload(state: MVPilotState) -> list[dict[str, Any]]:
    return [
        assumption.model_dump(mode="json", exclude_none=True)
        for assumption in state.get("assumptions", [])
    ]


def _previous_outputs_payload(state: MVPilotState) -> dict[str, dict[str, Any]]:
    payload: dict[str, dict[str, Any]] = {}

    for stage_key in STAGE_STATE_KEYS:
        stage_outputs = state.get(stage_key, {})
        if not stage_outputs:
            continue

        payload[stage_key] = {
            file_name: output.model_dump(mode="json", exclude_none=True)
            for file_name, output in stage_outputs.items()
        }

    return payload


def _required_output_shape(spec: DocumentSpec) -> dict[str, Any]:
    return {
        "file_name": spec.file_name,
        "title": spec.title,
        "source_stage": spec.source_stage,
        "summary": "string",
        "assumptions": ["string"],
        "sections": [
            {
                "heading": heading,
                "body": ["string"],
            }
            for heading in spec.section_headings
        ],
    }


def _to_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2)
