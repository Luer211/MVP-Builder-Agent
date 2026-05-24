from __future__ import annotations

from app.schemas.documents import DOCUMENT_FILE_NAMES, DOCUMENT_SPECS


def test_document_registry_has_fixed_twelve_files() -> None:
    assert len(DOCUMENT_SPECS) == 12
    assert DOCUMENT_FILE_NAMES == (
        "00_overview.md",
        "01_core_flow.md",
        "02_scope.md",
        "03_domain_model.md",
        "04_data_model.md",
        "05_architecture.md",
        "06_api_contract.md",
        "07_project_skeleton.md",
        "08_implementation_plan.md",
        "09_technical_debt.md",
        "10_iteration_roadmap.md",
        "11_acceptance_criteria.md",
    )
