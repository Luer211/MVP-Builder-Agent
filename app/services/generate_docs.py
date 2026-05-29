from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

from app.core.config import Settings, get_settings
from app.core.llm import get_llm_client
from app.rendering.markdown import render_documents
from app.schemas.documents import DOCUMENT_FILE_NAMES, DocumentStageOutput
from app.schemas.requests import GenerateDocsRequest
from app.schemas.responses import FileListResponse, GenerateDocsResponse, RunSummaryResponse
from app.schemas.state import MVPilotState, UserInput
from app.storage.filesystem import FileSystemRunStore
from app.workflow.graph import Workflow, build_workflow


class GenerateDocsService:
    """文档生成服务类"""

    def __init__(self, settings: Settings, workflow: Workflow, storage: FileSystemRunStore) -> None:
        self.settings = settings
        self.workflow = workflow
        self.storage = storage

    def generate(self, request: GenerateDocsRequest) -> GenerateDocsResponse:
        run_id = self._new_run_id()
        created_at = datetime.now(timezone.utc)

        user_input = UserInput(**request.model_dump())
        output_dir = self.storage.resolve_output_dir(run_id, user_input.output_dir)

        initial_state: MVPilotState = {
            "run_id": run_id,
            "user_input": user_input,
        }

        completed_state = self.workflow.invoke(initial_state)
        stage_outputs = self._collect_stage_outputs(completed_state)
        documents = render_documents(stage_outputs)

        manifest = self.storage.write_run(
            run_id=run_id,
            input_summary=self._input_summary(request.idea),
            output_dir=output_dir,
            documents=documents,
            overwrite=request.overwrite,
            created_at=created_at,
        )

        return GenerateDocsResponse(
            run_id=manifest.run_id,
            status=manifest.status,
            output_dir=manifest.output_dir,
            files=manifest.files,
            errors=manifest.errors,
        )

    def get_run(self, run_id: str) -> RunSummaryResponse:
        manifest = self.storage.read_manifest(run_id)
        return RunSummaryResponse(**manifest.model_dump())

    def list_files(self, run_id: str) -> FileListResponse:
        return FileListResponse(run_id=run_id, files=self.storage.list_files(run_id))

    def get_file(self, run_id: str, file_name: str) -> str:
        return self.storage.read_file(run_id, file_name)

    def _collect_stage_outputs(self, state: MVPilotState) -> list[DocumentStageOutput]:
        """从 state 中收集出 12 个 DocumentStageOutput"""
        outputs_by_file: dict[str, DocumentStageOutput] = {}

        for stage_key in (
            "core_understanding_stage",
            "modeling_stage",
            "architecture_stage",
            "planning_stage",
            "validation_stage",
        ):
            outputs_by_file.update(state.get(stage_key, {}))

        return [outputs_by_file[file_name] for file_name in DOCUMENT_FILE_NAMES]

    def _input_summary(self, idea: str) -> str:
        normalized = " ".join(idea.split())
        return normalized[:120]

    def _new_run_id(self) -> str:
        stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        return f"run_{stamp}_{uuid4().hex[:8]}"


# 单例懒加载
_service: Optional[GenerateDocsService] = None


def get_generate_docs_service() -> GenerateDocsService:
    """FastAPI 依赖注入使用"""
    global _service

    if _service is None:
        settings = get_settings()
        llm = get_llm_client(settings)

        _service = GenerateDocsService(
            settings=settings,
            workflow=build_workflow(llm),
            storage=FileSystemRunStore(settings.output_root),
        )

    return _service
