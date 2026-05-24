# Project Skeleton

## Directory Structure

建议第一版项目结构：

```text
.
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── logging.py
│   │   └── llm.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── requests.py
│   │   ├── responses.py
│   │   ├── state.py
│   │   └── documents.py
│   ├── workflow/
│   │   ├── __init__.py
│   │   ├── graph.py
│   │   ├── nodes.py
│   │   └── prompts.py
│   ├── rendering/
│   │   ├── __init__.py
│   │   └── markdown.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── generate_docs.py
│   └── storage/
│       ├── __init__.py
│       └── filesystem.py
├── docs/
├── outputs/
├── tests/
├── README.md
└── pyproject.toml
```

## Configuration

配置项：

```text
APP_NAME
ENV
OUTPUT_ROOT
OPENAI_API_KEY
MODEL_NAME
REQUEST_TIMEOUT_SECONDS
```

第一版可以使用 `.env` 或环境变量读取。

## Database Initialization

第一版不初始化数据库。

如果后续需要任务历史，新增数据库初始化模块，不要把数据库逻辑塞进 API handler。

## Router Initialization

`app/main.py` 负责：

- 创建 FastAPI app。
- 注册 `/api/v1` 路由。
- 注册健康检查。
- 初始化配置和日志。

建议路由：

```text
GET /health
POST /api/v1/doc-runs
GET /api/v1/doc-runs/{run_id}
GET /api/v1/doc-runs/{run_id}/files
GET /api/v1/doc-runs/{run_id}/files/{file_name}
```

## Dependency Injection

第一版使用简单依赖注入即可：

- `get_settings()`
- `get_llm_client()`
- `get_generate_docs_service()`

不要引入复杂容器。

## Error Handling Baseline

基础错误处理：

- 输入错误返回 400。
- run 或文件不存在返回 404。
- 生成失败返回 500。
- 所有错误返回统一 `ApiError` 结构。

## Local Development

建议本地启动方式：

```text
uv sync
uv run fastapi dev app/main.py
```

或：

```text
pip install -e .
uvicorn app.main:app --reload
```

第一版验收时，只需要能通过 API 触发生成并在本地输出目录看到 12 个 Markdown 文件。
