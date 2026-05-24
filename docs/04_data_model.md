# Data Model

## Database Choice

第一版不引入业务数据库。

原因：

- 核心目标是生成 12 个 Markdown 文件。
- 单机本地运行即可验证闭环。
- 引入数据库会增加初始化、迁移和部署复杂度。

第一版持久化方式：

- 生成结果写入本地文件系统，统一写到该项目的 test_docs/ 文件夹下面。
- 可选写出 `manifest.json` 记录 run 元数据。
- 运行时 state 使用 Pydantic model 或 TypedDict 承载。

## Core Data Structures

### MVPilotState

LangGraph 主状态。

```text
MVPilotState
├── run_id
├── user_input
├── assumptions
├── core_understanding_stage
├── modeling_stage
├── architecture_stage
├── planning_stage
├── validation_stage
├── documents
└── errors
```

### UserInput

```text
UserInput
├── idea: str
├── preferred_tech_stack: dict | None
├── output_dir: str | None
└── overwrite: bool
```

### GeneratedDocument

```text
GeneratedDocument
├── file_name: str
├── title: str
├── content: str
└── source_stage: str
```

### RunManifest

```text
RunManifest
├── run_id: str
├── status: str
├── input_summary: str
├── output_dir: str
├── files: list[str]
├── created_at: str
└── completed_at: str | None
```

## Relationships

- `UserInput` 启动一个 `MVPilotState`。
- `MVPilotState` 聚合所有 stage output。
- `GeneratedDocument` 从 stage output 渲染生成。
- `RunManifest` 记录一次 run 的结果摘要。

## Minimal Fields

第一版最小字段：

- run_id
- idea
- output_dir
- stage outputs
- generated documents
- status
- errors

## Deferred Fields

后续可以补充：

- user_id
- organization_id
- model_name
- token_usage
- cost
- retry_count
- checker_findings
- hitl_decisions
- prompt_version

## Constraints and Indexes

第一版没有数据库索引。

文件系统约束：

- 每次 run 必须有唯一 `run_id`。
- 输出目录默认不覆盖已有文件，除非 `overwrite=true`。
- 目标文档文件名必须来自固定白名单。
- 文档写入必须使用 UTF-8。

## Migration Notes

如果后续引入数据库，优先使用 SQLite 或 Postgres。

建议迁移路径：

1. 保留文件系统作为 artifact 存储。
2. 新增 `runs` 表记录任务元数据。
3. 新增 `documents` 表记录文件索引，不把大段 Markdown 强行塞入核心表。
4. checker 和 HITL 成熟后再新增相关表。
