from __future__ import annotations

from app.core.config import Settings
from app.schemas.documents import DOCUMENT_FILE_NAMES
from app.schemas.requests import GenerateDocsRequest
from app.services.generate_docs import GenerateDocsService
from app.storage.filesystem import FileSystemRunStore
from app.workflow.graph import build_workflow


def test_generate_docs_writes_twelve_markdown_files(tmp_path) -> None:
    service = GenerateDocsService(
        settings=Settings(output_root=tmp_path),
        workflow=build_workflow(),
        storage=FileSystemRunStore(tmp_path),
    )

    response = service.generate(
        GenerateDocsRequest(
            idea="我想使用 Go 语言做一个课程签到后端系统，学生扫码签到，老师可以查看统计。",
            output_dir=str(tmp_path / "course-checkin"),
        )
    )

    assert response.status == "completed"
    assert response.files == list(DOCUMENT_FILE_NAMES)
    for file_name in DOCUMENT_FILE_NAMES:
        content = (tmp_path / "course-checkin" / file_name).read_text(encoding="utf-8")
        assert content.startswith("# ")
