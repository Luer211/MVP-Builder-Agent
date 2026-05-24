from __future__ import annotations

from app.schemas.documents import DOCUMENT_SPECS, DocumentSpec


DOCUMENT_SPEC_BY_NODE: dict[str, DocumentSpec] = {spec.node_name: spec for spec in DOCUMENT_SPECS}
