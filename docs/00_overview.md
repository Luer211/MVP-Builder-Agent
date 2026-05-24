# Overview

## Product Idea

MVP Builder Agent 是一个面向个人开发者和小团队的 AI 产品工程助手。

用户输入一段产品想法或业务需求后，系统不会直接生成代码，而是先生成一套可供 Codex 或开发者阅读的 MVP 工程文档。文档需要把需求拆成清晰的产品目标、核心闭环、范围边界、领域模型、数据模型、架构边界、API 契约、项目骨架、实施计划、技术债和验收标准。

第一版重点不是做一个完整产品管理平台，而是把“想法 -> 可开发 MVP 文档集”这条链路跑通。

## One-line MVP

输入一个产品想法，稳定生成 12 个结构化 Markdown 文档，让 Codex 能据此快速搭建项目骨架。

## Target Users

- 个人开发者：有产品想法，但需要快速整理成可实现的工程方案。
- 小型创业团队：需要在早期快速对齐 MVP 范围和工程边界。
- 使用 Codex 类 coding agent 的用户：希望先生成高质量 docs，再让 coding agent 基于 docs 开发。

## Core Problem

很多产品想法直接进入编码会产生三个问题：

- 需求边界模糊，MVP 越做越大。
- 领域模型和数据模型一开始就混乱，后续返工成本高。
- Codex 读到的信息不完整，只能凭局部上下文猜测架构。

MVP Builder Agent 要解决的是：在写代码前，先把最小但关键的产品工程上下文写清楚。

## MVP Goal

第一版只交付一个克制的文档生成闭环：

1. 接收用户原始需求。
2. 按固定阶段生成结构化中间结果。
3. 渲染并写出 12 个 Markdown 文档。
4. 保证文档之间的基本一致性。
5. 让后续 Codex 可以直接读取这些文档并开始搭建项目。

## Recommended Tech Stack

- 后端语言：Python
- API 框架：FastAPI
- Agent 编排：LangGraph
- 数据校验：Pydantic
- 文档渲染：Markdown 模板或轻量字符串模板
- 持久化：第一版使用本地文件系统，不引入业务数据库
- 本地运行：uv 或 pip + FastAPI dev server

## Output Summary

第一版生成 12 个文档：

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

`docs/READMD.md` 是当前项目的原始设计稿，不属于系统第一版稳定输出的 12 个目标文档。
