# Implementation Plan

## Milestone 0: Project Skeleton

目标：搭出可运行的 FastAPI 项目骨架。

任务：

- 创建 `app/` 基础目录。
- 创建 `pyproject.toml`。
- 创建 `app/main.py`。
- 创建 `/health` 接口。
- 创建配置模块。
- 创建基础测试或 smoke check。

验收：

- 本地服务能启动。
- `/health` 返回正常。

## Milestone 1: Schemas and Document Registry

目标：先固定数据结构和 12 个目标文档清单。

任务：

- 定义 `GenerateDocsRequest`。
- 定义 `GenerateDocsResponse`。
- 定义 `MVPilotState`。
- 定义 `GeneratedDocument`。
- 定义固定文档清单。

验收：

- 文档文件名不能由节点自由发挥。
- state 能覆盖所有阶段输出。

## Milestone 2: LangGraph Straight-line Workflow

目标：跑通无 checker、无 HITL 的正向链路。

任务：

- 创建 `graph.py`。
- 创建 12 个生成节点。
- 每个节点读取 state 并写入对应 stage output。
- 串联为直线图。

验收：

- 输入一个 idea 后，workflow 能返回完整 state。

## Milestone 3: Markdown Rendering and File Writing

目标：把结构化输出写成 Markdown 文件。

任务：

- 实现 Markdown 渲染器。
- 实现文件系统 writer。
- 写出 12 个 Markdown 文件。
- 写出可选 manifest。

验收：

- 输出目录中稳定出现 12 个目标文件。
- 文件名和清单一致。
- 文件编码为 UTF-8。

## Milestone 4: API Integration

目标：通过 HTTP API 触发生成。

任务：

- 实现 `POST /api/v1/doc-runs`。
- 实现 run 查询和文件查询接口。
- 接入错误处理。

验收：

- curl 或 API client 能触发一次生成。
- 响应包含 run_id、status、output_dir、files。

## Milestone 5: Basic Validation and Tests

目标：避免明显不稳定。

任务：

- 测试空输入。
- 测试输出目录已存在。
- 测试文档数量。
- 测试文件名白名单。
- 测试 Markdown 非空。

验收：

- 核心 happy path 有测试。
- 常见错误路径有测试。

## Milestone 6: First Demo

目标：跑通一次真实产品想法。

Demo 输入：

```text
我想使用 Go 语言做一个课程签到后端系统，学生扫码签到，老师可以查看统计。
```

验收：

- 生成 12 个文档。
- 文档之间技术栈一致。
- 核心闭环清楚。
- 数据模型和 API 契约能对应。
- Codex 读完 docs 后可以开始搭建项目骨架。
