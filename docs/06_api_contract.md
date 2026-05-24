# API Contract

## API Design Principles

第一版 API 只服务于本地生成场景。

原则：

- 接口少。
- 请求结构明确。
- 返回固定文件清单。
- 错误格式稳定。
- 不做鉴权。
- 不暴露内部 prompt。

## Core Endpoints

### Create Doc Run

```text
POST /api/v1/doc-runs
```

用途：提交产品想法并生成 12 个 Markdown 文档。

请求：

```text
{
  "idea": "我想使用 Go 语言做一个课程签到后端系统...",
  "preferred_tech_stack": {
    "backend_language": "Go",
    "framework": "Gin",
    "database": "MySQL"
  },
  "output_dir": "outputs/course-checkin",
  "overwrite": false
}
```

响应：

```text
{
  "run_id": "run_20260524_001",
  "status": "completed",
  "output_dir": "outputs/course-checkin",
  "files": [
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
    "11_acceptance_criteria.md"
  ]
}
```

### Get Doc Run

```text
GET /api/v1/doc-runs/{run_id}
```

用途：查看一次生成任务的摘要。

第一版如果没有数据库，可以只支持当前进程内 run 或从 manifest 文件读取。

### List Run Files

```text
GET /api/v1/doc-runs/{run_id}/files
```

用途：返回某次 run 的文件清单。

### Get Run File

```text
GET /api/v1/doc-runs/{run_id}/files/{file_name}
```

用途：读取某个生成的 Markdown 文件。

## Request / Response Schema

### GenerateDocsRequest

```text
idea: str
preferred_tech_stack: dict | None
output_dir: str | None
overwrite: bool = false
```

### GenerateDocsResponse

```text
run_id: str
status: "completed" | "failed"
output_dir: str
files: list[str]
errors: list[ApiError] | None
```

### ApiError

```text
code: str
message: str
detail: dict | None
```

## Error Codes

- `INVALID_INPUT`：用户输入为空或过短。
- `OUTPUT_EXISTS`：目标目录已存在且不允许覆盖。
- `GENERATION_FAILED`：模型或工作流生成失败。
- `RENDER_FAILED`：Markdown 渲染失败。
- `WRITE_FAILED`：文件写入失败。
- `RUN_NOT_FOUND`：找不到指定 run。
- `FILE_NOT_FOUND`：找不到指定生成文件。

## Auth Boundary

第一版不做登录鉴权。

原因：

- 目标是本地开发工具。
- 用户和系统默认在可信环境中运行。
- 权限系统会显著扩大范围。

后续如果部署为多人服务，再引入用户、组织和项目权限。

## Deferred APIs

后续可以增加：

- `POST /api/v1/doc-runs/{run_id}/retry`
- `POST /api/v1/doc-runs/{run_id}/approve`
- `POST /api/v1/doc-runs/{run_id}/feedback`
- `GET /api/v1/doc-runs`
- `GET /api/v1/prompt-versions`
- `POST /api/v1/doc-runs/{run_id}/export`
