from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


StageName = Literal["core_understanding", "modeling", "architecture", "planning", "validation"]


class DocumentSpec(BaseModel):
    file_name: str
    title: str
    source_stage: StageName
    node_name: str
    section_headings: list[str]


class MarkdownSection(BaseModel):
    heading: str
    body: list[str] = Field(default_factory=list)


class DocumentStageOutput(BaseModel):
    file_name: str
    title: str
    source_stage: StageName
    summary: str
    assumptions: list[str] = Field(default_factory=list)
    sections: list[MarkdownSection] = Field(default_factory=list)


class GeneratedDocument(BaseModel):
    file_name: str
    title: str
    content: str
    source_stage: StageName


DOCUMENT_SPECS: tuple[DocumentSpec, ...] = (
    DocumentSpec(
        file_name="00_overview.md",
        title="Overview",
        source_stage="core_understanding",
        node_name="overview_node",
        section_headings=[
            "Product Idea",
            "One-line MVP",
            "Target Users",
            "Core Problem",
            "MVP Goal",
            "Recommended Tech Stack",
            "Output Summary",
        ],
    ),
    DocumentSpec(
        file_name="01_core_flow.md",
        title="Core Flow",
        source_stage="core_understanding",
        node_name="core_flow_node",
        section_headings=[
            "Core User Loop",
            "Primary Actors",
            "Main Scenario",
            "Alternative Scenarios",
            "Out of Core Flow",
        ],
    ),
    DocumentSpec(
        file_name="02_scope.md",
        title="MVP Scope",
        source_stage="core_understanding",
        node_name="scope_node",
        section_headings=["Must Have", "Should Have", "Won't Have in MVP", "Scope Rationale"],
    ),
    DocumentSpec(
        file_name="03_domain_model.md",
        title="Domain Model",
        source_stage="modeling",
        node_name="domain_model_node",
        section_headings=[
            "Core Concepts",
            "Entities",
            "Value Objects",
            "Domain Relationships",
            "Business Rules",
            "Non-negotiable Domain Constraints",
        ],
    ),
    DocumentSpec(
        file_name="04_data_model.md",
        title="Data Model",
        source_stage="modeling",
        node_name="data_model_node",
        section_headings=[
            "Database Choice",
            "Core Data Structures",
            "Relationships",
            "Minimal Fields",
            "Deferred Fields",
            "Constraints and Indexes",
            "Migration Notes",
        ],
    ),
    DocumentSpec(
        file_name="05_architecture.md",
        title="Architecture",
        source_stage="architecture",
        node_name="architecture_node",
        section_headings=[
            "Architecture Style",
            "Layer Responsibilities",
            "Dependency Direction",
            "Module Boundaries",
            "Initialization and Infrastructure",
            "Non-negotiable Architecture Rules",
        ],
    ),
    DocumentSpec(
        file_name="06_api_contract.md",
        title="API Contract",
        source_stage="architecture",
        node_name="api_contract_node",
        section_headings=[
            "API Design Principles",
            "Core Endpoints",
            "Request / Response Schema",
            "Error Codes",
            "Auth Boundary",
            "Deferred APIs",
        ],
    ),
    DocumentSpec(
        file_name="07_project_skeleton.md",
        title="Project Skeleton",
        source_stage="architecture",
        node_name="project_skeleton_node",
        section_headings=[
            "Directory Structure",
            "Configuration",
            "Database Initialization",
            "Router Initialization",
            "Dependency Injection",
            "Error Handling Baseline",
            "Local Development",
        ],
    ),
    DocumentSpec(
        file_name="08_implementation_plan.md",
        title="Implementation Plan",
        source_stage="planning",
        node_name="implementation_plan_node",
        section_headings=[
            "Milestone 0: Project Skeleton",
            "Milestone 1: Schemas and Document Registry",
            "Milestone 2: LangGraph Straight-line Workflow",
            "Milestone 3: Markdown Rendering and File Writing",
            "Milestone 4: API Integration",
            "Milestone 5: Basic Validation and Tests",
            "Milestone 6: First Demo",
        ],
    ),
    DocumentSpec(
        file_name="09_technical_debt.md",
        title="Technical Debt",
        source_stage="planning",
        node_name="technical_debt_node",
        section_headings=[
            "Principle",
            "Acceptable Technical Debt",
            "Dangerous Technical Debt",
            "Debt Review Rules",
            "Refactoring Triggers",
            "Deferred Improvements",
        ],
    ),
    DocumentSpec(
        file_name="10_iteration_roadmap.md",
        title="Iteration Roadmap",
        source_stage="planning",
        node_name="iteration_roadmap_node",
        section_headings=[
            "V0.1 MVP",
            "V0.2 Usability",
            "V0.3 Validation",
            "V0.4 HITL",
            "V0.5 Reliability",
            "V1.0 Productization",
        ],
    ),
    DocumentSpec(
        file_name="11_acceptance_criteria.md",
        title="Acceptance Criteria",
        source_stage="validation",
        node_name="acceptance_criteria_node",
        section_headings=[
            "Functional Acceptance",
            "Architecture Acceptance",
            "Data Model Acceptance",
            "API Acceptance",
            "Document Quality Acceptance",
            "Non-goals",
        ],
    ),
)

DOCUMENT_FILE_NAMES: tuple[str, ...] = tuple(spec.file_name for spec in DOCUMENT_SPECS)
