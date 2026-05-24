from __future__ import annotations

from app.schemas.documents import DocumentStageOutput, GeneratedDocument


def render_markdown(output: DocumentStageOutput) -> str:
    lines: list[str] = [f"# {output.title}", "", output.summary, ""]

    if output.assumptions:
        lines.extend(["## Assumptions", ""])
        for assumption in output.assumptions:
            lines.append(f"- {assumption}")
        lines.append("")

    for section in output.sections:
        lines.extend([f"## {section.heading}", ""])
        lines.extend(section.body or ["- TBD"])
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def render_documents(outputs: list[DocumentStageOutput]) -> list[GeneratedDocument]:
    return [
        GeneratedDocument(
            file_name=output.file_name,
            title=output.title,
            content=render_markdown(output),
            source_stage=output.source_stage,
        )
        for output in outputs
    ]
