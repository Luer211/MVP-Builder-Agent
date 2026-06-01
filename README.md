# MVP Builder Agent

> 从一个粗略想法，生成一套可开发的 MVP 产品工程文档。

MVP Builder Agent 是一个 AI 产品工程助手，用来把早期产品想法整理成清晰、克制、可落地的 MVP 开发方案。

它不会一上来直接生成代码，而是先生成开发前最重要的工程上下文：产品总览、核心闭环、范围边界、领域模型、数据模型、架构边界、API 契约、项目骨架、实施计划、技术债、迭代路线和验收标准。

这些文档可以交给开发者阅读，也可以交给 Codex 这类 coding agent 去快速搭建项目骨架。

## 为什么做这个项目

很多 MVP 不是写代码时才出问题，而是在写代码之前就已经埋下问题：

- 产品范围不断膨胀。
- 核心业务闭环没有说清楚。
- 领域模型和数据模型混在一起。
- 架构边界太晚才决定。
- Coding agent 拿到的上下文太模糊，只能靠猜。

MVP Builder Agent 要解决的是第一步：在开始开发前，先把想法变成一套结构稳定、边界清楚、能指导开发的文档。

## 核心思路

第一版会非常克制：

```text
用户输入产品想法
-> AI 产品工程工作流
-> 生成 12 个结构化 Markdown 文档
-> Codex / 开发者基于 docs 搭建项目骨架
```

这个项目第一阶段不是做一个完整的产品管理平台，也不是直接生成完整代码，而是稳定生成一个高质量的 `docs/` 文件夹。

## 目标输出

系统第一版会稳定生成 12 个 Markdown 文件：

```text
docs/
├── 00_overview.md
├── 01_core_flow.md
├── 02_scope.md
├── 03_domain_model.md
├── 04_data_model.md
├── 05_architecture.md
├── 06_api_contract.md
├── 07_project_skeleton.md
├── 08_implementation_plan.md
├── 09_technical_debt.md
├── 10_iteration_roadmap.md
└── 11_acceptance_criteria.md
```

这套文档要回答这些问题：

- 这个 MVP 到底是什么？
- 为谁解决什么问题？
- 核心用户闭环是什么？
- 第一版必须做什么，明确不做什么？
- 核心领域对象有哪些？
- 数据模型如何支撑核心业务流？
- 架构边界在哪里？
- 第一版需要哪些 API？
- 项目目录和基础设施应该怎么放？
- 哪些技术债可以接受，哪些不能接受？
- codex生成代码骨架时应该遵循哪些预设前提？
- 后续怎么迭代？
- 怎么判断第一版真的完成了？

## 计划技术栈

- Python
- FastAPI
- LangGraph
- Pydantic
- Markdown 渲染
- 第一版使用本地文件系统输出

第一版预期是一个本地可运行的后端工具。数据库、队列、多用户账号、Web UI 都会先延后。

## MVP 范围

### 第一版必须有

- FastAPI 服务入口。
- 一条直线式 LangGraph 生成流程。
- 清晰的 workflow state。
- 请求、响应和阶段输出的 Pydantic schema。
- 固定的 12 个文档清单。
- Markdown 渲染器。
- 本地文件输出。

### 第一版不做

- 直接生成业务代码。
- Web UI。
- 用户登录。
- 数据库任务历史。
- HITL 人工审批流。
- checker 自动回退。
- 多模型路由。
- token 成本统计。

## 当前状态

项目目前处于产品工程设计和 MVP 文档阶段。

当前已经先整理出项目自身的 12 个设计文档，位于 [`docs/`](./docs/) 目录。

第一阶段实现目标是跑通这条正向链路：

```text
Idea Intake
-> Core Understanding
-> Modeling
-> Architecture
-> Planning
-> Validation
-> Docs Generator
```

checker 节点、HITL 节点、自动回退和更复杂的质量校验会放到后续迭代。第一版先把“输入想法 -> 稳定生成 docs”这件事做好。

## 当前项目骨架

当前仓库已经按设计文档落出第一版后端骨架：

```text
app/
├── main.py                 # FastAPI app 初始化、健康检查、错误处理
├── api/routes.py           # /api/v1/doc-runs 路由
├── core/                   # 配置、日志、LLM client 抽象、错误类型
├── schemas/                # 请求、响应、state、文档清单 schema
├── workflow/               # LangGraph 直线 workflow 和 12 个文档节点
├── rendering/markdown.py   # 集中 Markdown 渲染
├── services/generate_docs.py
└── storage/filesystem.py   # 本地文件写入和 manifest 读取
```

第一版生成逻辑先使用本地确定性实现，核心边界已经留好：后续可以把 `app/core/llm.py` 和 `app/workflow/nodes.py` 替换为真实模型调用，但 API、state、渲染和存储边界不需要重写。

默认输出根目录是 `test_docs/`；请求中传入 `output_dir` 时会写入指定目录。

## 本地运行

推荐使用 uv：

```bash
uv sync --extra dev
uv run uvicorn app.main:app --reload
```

如果当前 Python 环境已经装好依赖，也可以直接运行：

```bash
python -m uvicorn app.main:app --reload
```

健康检查：

```bash
curl http://127.0.0.1:8000/health
```

生成一次文档：

```bash
curl -X POST http://127.0.0.1:8000/api/v1/doc-runs \
  -H "Content-Type: application/json" \
  -d '{
    "idea": "我想使用 Go 语言做一个课程签到后端系统，学生扫码签到，老师可以查看统计。",
    "preferred_tech_stack": {
      "backend_language": "Go",
      "framework": "Gin",
      "database": "MySQL"
    },
    "output_dir": "test_docs/course-checkin",
    "overwrite": true
  }'
```

基础校验：

```bash
python -m compileall app tests
python -m pytest
```

## 文档入口

可以从这些文档开始看：

- [`docs/00_overview.md`](./docs/00_overview.md)
- [`docs/01_core_flow.md`](./docs/01_core_flow.md)
- [`docs/02_scope.md`](./docs/02_scope.md)
- [`docs/05_architecture.md`](./docs/05_architecture.md)
- [`docs/11_acceptance_criteria.md`](./docs/11_acceptance_criteria.md)

## 设计原则

这个项目的原则是：**克制，但不牺牲关键边界。**

可以暂时不做高级功能，但不能牺牲：

- MVP 范围边界。
- 核心业务闭环。
- 领域模型。
- 数据模型。
- 架构边界。
- 稳定的文档输出。

先生成高质量 docs，再让 Codex 基于明确上下文去写代码。
