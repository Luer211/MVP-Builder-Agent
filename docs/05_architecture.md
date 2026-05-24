# Architecture

## Architecture Style

第一版采用轻量分层架构：

```text
API Layer
-> Application / Workflow Layer
-> Agent Node Layer
-> Rendering / Storage Layer
```

LangGraph 负责编排生成流程，FastAPI 只负责接收请求和返回结果。

## Layer Responsibilities

### API Layer

职责：

- 接收生成请求。
- 校验请求参数。
- 调用应用服务。
- 返回生成结果或错误。

不负责：

- 拼 prompt。
- 写 Markdown。
- 直接操作 LangGraph state 内部细节。

### Application / Workflow Layer

职责：

- 初始化 `MVPilotState`。
- 调用 LangGraph workflow。
- 管理 run 生命周期。
- 汇总生成结果。

### Agent Node Layer

职责：

- 每个节点处理一个明确阶段。
- 根据前序 state 生成结构化输出。
- 返回 Pydantic schema 对象或可校验 dict。

第一版节点：

- overview_node
- core_flow_node
- scope_node
- domain_model_node
- data_model_node
- architecture_node
- api_contract_node
- project_skeleton_node
- implementation_plan_node
- technical_debt_node
- iteration_roadmap_node
- acceptance_criteria_node

### Rendering / Storage Layer

职责：

- 将结构化输出渲染为 Markdown。
- 按固定文件名写入本地文件系统。
- 生成 manifest。

## Dependency Direction

```text
app/api
  depends on app/services

app/services
  depends on app/workflow, app/storage

app/workflow
  depends on app/schemas, app/prompts

app/storage
  depends on app/schemas
```

底层模块不能反向依赖 API。

## Module Boundaries

- `api`：HTTP 路由和请求响应模型。
- `services`：用例服务，例如 `GenerateDocsService`。
- `workflow`：LangGraph 图、节点、状态定义。
- `schemas`：Pydantic 数据结构。
- `prompts`：提示词模板。
- `rendering`：Markdown 渲染。
- `storage`：文件写入和 manifest。
- `core`：配置、日志、模型客户端初始化。

## Initialization and Infrastructure

启动时初始化：

- FastAPI app。
- 配置对象。
- LLM client。
- LangGraph workflow。
- 输出根目录。

第一版可以不初始化：

- 数据库连接。
- Redis。
- MQ。
- 后台 worker。

## Non-negotiable Architecture Rules

- API handler 不能直接写文件。
- API handler 不能直接拼 prompt。
- 每个节点必须有明确输入和输出。
- 文件名必须由固定文档清单控制。
- Markdown 渲染必须集中处理。
- LLM 调用必须可替换，不能散落在业务代码里。
- checker 和 HITL 只能作为后续可插拔节点加入，不能污染第一版主链路。
