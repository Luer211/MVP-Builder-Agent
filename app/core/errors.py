from __future__ import annotations

from typing import Optional


class AppError(Exception):
    def __init__(
        self,
        code: str,
        message: str,
        *,
        status_code: int = 400,
        detail: Optional[dict] = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.status_code = status_code
        self.detail = detail


def invalid_input(message: str, detail: Optional[dict] = None) -> AppError:
    return AppError("INVALID_INPUT", message, status_code=400, detail=detail)


def output_exists(path: str) -> AppError:
    return AppError(
        "OUTPUT_EXISTS",
        "Output directory already contains files. Use overwrite=true or choose another directory.",
        status_code=409,
        detail={"output_dir": path},
    )


def run_not_found(run_id: str) -> AppError:
    return AppError("RUN_NOT_FOUND", "Run was not found.", status_code=404, detail={"run_id": run_id})


def file_not_found(run_id: str, file_name: str) -> AppError:
    return AppError(
        "FILE_NOT_FOUND",
        "Run file was not found.",
        status_code=404,
        detail={"run_id": run_id, "file_name": file_name},
    )
