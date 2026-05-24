from __future__ import annotations

from fastapi import APIRouter, Depends, Response

from app.schemas.requests import GenerateDocsRequest
from app.schemas.responses import FileListResponse, GenerateDocsResponse, RunSummaryResponse
from app.services.generate_docs import GenerateDocsService, get_generate_docs_service


router = APIRouter(prefix="/api/v1", tags=["doc-runs"])


@router.post("/doc-runs", response_model=GenerateDocsResponse)
def create_doc_run(
    request: GenerateDocsRequest,
    service: GenerateDocsService = Depends(get_generate_docs_service),
) -> GenerateDocsResponse:
    return service.generate(request)


@router.get("/doc-runs/{run_id}", response_model=RunSummaryResponse)
def get_doc_run(
    run_id: str,
    service: GenerateDocsService = Depends(get_generate_docs_service),
) -> RunSummaryResponse:
    return service.get_run(run_id)


@router.get("/doc-runs/{run_id}/files", response_model=FileListResponse)
def list_run_files(
    run_id: str,
    service: GenerateDocsService = Depends(get_generate_docs_service),
) -> FileListResponse:
    return service.list_files(run_id)


@router.get("/doc-runs/{run_id}/files/{file_name}", response_class=Response)
def get_run_file(
    run_id: str,
    file_name: str,
    service: GenerateDocsService = Depends(get_generate_docs_service),
) -> Response:
    content = service.get_file(run_id, file_name)
    return Response(content=content, media_type="text/markdown; charset=utf-8")
