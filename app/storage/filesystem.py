from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from app.core.errors import file_not_found, output_exists, run_not_found
from app.schemas.documents import DOCUMENT_FILE_NAMES, GeneratedDocument
from app.schemas.state import RunManifest


class FileSystemRunStore:
    def __init__(self, output_root: Path) -> None:
        self.output_root = output_root
        self._run_dirs: dict[str, Path] = {}

    def resolve_output_dir(self, run_id: str, requested_output_dir: Optional[str]) -> Path:
        if requested_output_dir:
            path = Path(requested_output_dir)
            target = path if path.is_absolute() else Path.cwd() / path
        else:
            target = Path.cwd() / self.output_root / run_id
        return target.resolve()

    def write_run(
        self,
        *,
        run_id: str,
        input_summary: str,
        output_dir: Path,
        documents: list[GeneratedDocument],
        overwrite: bool,
        created_at: datetime,
    ) -> RunManifest:
        if output_dir.exists() and not overwrite and any(output_dir.iterdir()):
            raise output_exists(str(output_dir))

        output_dir.mkdir(parents=True, exist_ok=True)
        files: list[str] = []
        for document in documents:
            if document.file_name not in DOCUMENT_FILE_NAMES:
                continue
            path = output_dir / document.file_name
            path.write_text(document.content, encoding="utf-8")
            files.append(document.file_name)

        completed_at = datetime.now(timezone.utc)
        manifest = RunManifest(
            run_id=run_id,
            status="completed",
            input_summary=input_summary,
            output_dir=str(output_dir),
            files=files,
            created_at=created_at.isoformat(),
            completed_at=completed_at.isoformat(),
            errors=None,
        )
        (output_dir / "manifest.json").write_text(
            json.dumps(manifest.model_dump(), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        self._run_dirs[run_id] = output_dir
        return manifest

    def read_manifest(self, run_id: str) -> RunManifest:
        run_dir = self._run_dirs.get(run_id)
        if run_dir is not None:
            manifest_path = run_dir / "manifest.json"
            if manifest_path.exists():
                return RunManifest.model_validate_json(manifest_path.read_text(encoding="utf-8"))

        for manifest_path in (Path.cwd() / self.output_root).glob("**/manifest.json"):
            manifest = RunManifest.model_validate_json(manifest_path.read_text(encoding="utf-8"))
            if manifest.run_id == run_id:
                self._run_dirs[run_id] = manifest_path.parent
                return manifest

        raise run_not_found(run_id)

    def list_files(self, run_id: str) -> list[str]:
        return self.read_manifest(run_id).files

    def read_file(self, run_id: str, file_name: str) -> str:
        if file_name not in DOCUMENT_FILE_NAMES:
            raise file_not_found(run_id, file_name)

        manifest = self.read_manifest(run_id)
        path = Path(manifest.output_dir) / file_name
        if not path.exists():
            raise file_not_found(run_id, file_name)
        return path.read_text(encoding="utf-8")
