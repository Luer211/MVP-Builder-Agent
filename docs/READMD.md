# MVP Builder Agent：从想法到可开发 MVP 的 AI 产品工程助手

技术栈：Langgraph、FastAPI



## 项目的目标

让用户输入一个需求，然后可以快速产出一个文档，然后让codex去扫描浏览完能快速建立起一个项目的骨架。
分清楚什么是可以妥协的，什么是绝对不能妥协的？我们一个核心的原则就是说，我们尽可能快地写出第一版的MVP docs/，然后可以让codex读完快速建立起一个项目骨架。
克制但不妥协，保留最精最简、但是易拓展、架构良好的设计。

```text
1. 不能妥协：架构边界、领域模型、核心数据模型、核心业务流、各种初始化连接
2. 可以简化：更详细的数据模型字段、功能实现细节、交互体验、性能优化、复杂异常处理
3. 可以延后：复杂权限系统、高级功能、扩展能力、自动化能力、复杂状态机、观测系统
```



## 项目使用场景
输入一段需求：
“我想使用Go语言做一个课程签到后端系统，学生扫码签到，老师可以查看统计。”
系统输出一个文件夹：

```text
docs/
├── 00_overview.md               # 项目总览
├── 01_core_flow.md              # 核心业务闭环链路
├── 02_scope.md                  # 克制原则
├── 03_domain_model.md           # 核心领域对象
├── 04_data_model.md             # 核心数据模型
├── 05_architecture.md           # MVP 的最小架构边界
├── 06_api_contract.md           # API 契约文档
├── 07_project_skeleton.md       # 项目目录设计
├── 08_implementation_plan.md    # 开发步骤计划
├── 09_technical_debt.md         # 项目技术债
├── 10_iteration_roadmap.md      # 后续迭代路线
└── 11_acceptance_criteria.md    # 验收标准
```

## 00_overview.md
这个文档是项目总览，用于让人快速看懂项目
这是项目总览，它要回答：
1. 这个项目是什么？
2. 为谁解决什么问题？
3. MVP 第一版要交付什么？
4. 不解决什么？
5. 技术栈是什么？
建议格式：

```text
# Overview

## Product Idea
用户原始想法的整理版。

## One-line MVP
一句话描述 MVP。

## Target Users
目标用户。

## Core Problem
核心问题。

## MVP Goal
第一版目标。

## Recommended Tech Stack
后端语言、框架、数据库、缓存、部署方式（docker起数据库、MQ、Redis等等，然后代码在本地跑）

## Output Summary
本次生成的文档索引。
```

## 01_core_flow.md
这个文档用于约束后续所有的设计，凡是不服务于核心闭环的功能都默认延后。
它要回答：这个产品的核心业务闭环是什么？
比如说课程签到系统：老师创建课程 → 老师发起签到 → 学生扫码签到 → 老师查看统计
建议格式：

```text
# Core Flow

## Core User Loop
核心用户闭环。

## Primary Actors
主要角色。

## Main Scenario
主路径。

## Alternative Scenarios
少量分支路径。

## Out of Core Flow
不属于 MVP 核心闭环的东西。
```

## 02_scope.md
这是 MVP 克制的核心文档，要求不牺牲架构边界和核心模型，只延后复杂能力和非核心功能。
建议格式：

```text
# MVP Scope

## Must Have
必须做。没有这些，核心闭环无法成立。

## Should Have
可以做，但不是第一优先级。（可空）

## Won't Have in MVP
明确不做。避免用户不断加功能。

## Scope Rationale
为什么这么裁剪。
```

示例：

```text
## Must Have:
-用户基础身份区分：老师 / 学生
-老师创建课程
-老师发起签到
-学生提交签到
-老师查看签到结果

## Won't Have:
-人脸识别
- GPS 防作弊
- Excel 导出
-多租户组织架构
-复杂权限系统

## Scope Rationale
MVP 阶段不牺牲架构边界和核心模型，只延后复杂能力和非核心功能。
```

## 03_domain_model.md
这是领域模型核心文档，回答该系统里有哪些核心领域对象？他们是什么关系？业务规则应该放在哪里？
建议格式：

```text
# Domain Model

## Core Concepts
核心领域概念。

## Entities
实体。

## Value Objects
值对象，可选。

## Domain Relationships
领域对象关系。

## Business Rules
核心业务规则。

## Non-negotiable Domain Constraints
不能破坏的领域约束。
```

## 04_data_model.md
克制的数据模型文档，只求最小最核心的字段设计，保证：表边界正确，关系正确，主键外键方向正确，能支撑后续扩展。可以允许字段简单，但不能允许模型混乱。
建议格式：

```text
# Data Model

## Database Choice
数据库选择。

## Core Tables
核心表。

## Relationships
表关系。

## Minimal Fields
MVP 必需字段。

## Deferred Fields
后续可以补充的字段。

## Constraints and Indexes
必要约束和索引。

## Migration Notes
迁移建议。
```

## 05_architecture.md
设计该 MVP 的最小架构边界
建议格式：

```text
# Architecture

## Architecture Style
比如三层架构 / Clean Architecture lite / MVC。

## Layer Responsibilities
每一层负责什么。

## Dependency Direction
依赖方向。

## Module Boundaries
模块边界。

## Initialization and Infrastructure
配置、数据库连接、日志、路由初始化等。

## Non-negotiable Architecture Rules
不能破坏的架构规则。
```

## 06_api_contract.md
API 契约文档，克制，只生成核心闭环所需要的 API。
建议格式：

```text
# API Contract

## API Design Principles
资源命名、鉴权、错误格式。

## Core Endpoints
核心接口。

## Request / Response Schema
请求响应结构。

## Error Codes
错误码。

## Auth Boundary
哪些接口需要登录，哪些角色可访问。

## Deferred APIs
后续迭代接口。
```

## 07_project_skeleton.md
项目目录应该是怎么样的？哪些基础设施一开始就要放好？实现可以粗糙，但骨架不能乱。
建议格式：

```text
# Project Skeleton

## Directory Structure
项目目录结构。

## Configuration
配置管理。

## Database Initialization
数据库连接初始化。

## Router Initialization
路由注册。

## Dependency Injection
依赖注入方式，简单即可。

## Error Handling Baseline
基础错误处理。

## Local Development
本地启动方式。
```

## 08_implementation_plan.md
个人开发者的大概开工计划和步骤：骨架 → 模型 → 核心用例 → API → 核心测试 → Demo。
建议格式：

```text
# Implementation Plan

## Milestone 0: Project Skeleton
初始化项目结构、配置、数据库连接。

## Milestone 1: Core Domain and Data Model
实现核心实体和迁移。

## Milestone 2: Core Use Cases
实现核心业务流。

## Milestone 3: API Layer
暴露核心接口。

## Milestone 4: Basic Validation and Tests
基础校验和核心测试。

## Milestone 5: First Demo
跑通完整闭环。
```

## 09_technical_debt.md
技术债说明文档：分为两类，可以忍受的技术债和不可忍受的技术债。
建议格式：

```text
# Technical Debt

## Principle
原则

## Acceptable Technical Debt
MVP 阶段可以接受的技术债。

## Dangerous Technical Debt
不能接受的技术债。

## Debt Review Rules
如何判断一项技术债是否危险。

## Refactoring Triggers
什么时候必须还债。
```

原则

```text
可接受技术债：
-实现方式暂时粗糙
-没有做性能优化
-异常处理不够完整
-没有复杂权限系统
-没有观测系统

危险技术债：
-核心数据模型错误
-架构层级混乱
-业务规则散落在接口层
-模块边界不清
- API 契约无法稳定演化
```

## 10_iteration_roadmap.md
后续迭代路线。它负责承接可以延后的东西。
建议格式：

```text
# Iteration Roadmap

## V0.1 MVP
第一版核心闭环。

## V0.2 Usability
交互体验、错误提示、基础管理功能。

## V0.3 Reliability
复杂异常处理、失败恢复、状态机。

## V0.4 Scale
性能优化、缓存、队列、观测系统。

## V1.0 Productization
复杂权限、高级功能、自动化能力。
```

## 11_acceptance_criteria.md
验收检验文档。检验 MVP 都完成哪些东西了。
建议格式：

```text
# Acceptance Criteria

## Functional Acceptance
核心功能验收。

## Architecture Acceptance
架构验收。

## Data Model Acceptance
数据模型验收。

## API Acceptance
接口验收。

## Non-goals
明确不验收的内容。
```

## 核心 LangGraph 链路
先跑通这条核心链路，check节点和HITL节点是可以无痛接入的，先可以不加入。

```text
Idea Intake
  ↓
Core Understanding Stage                # 核心业务理解模块
  ├── Overview gen
  ├── Core flow gen
  └── Scope gen
  ↓
Modeling Stage                          # 数据模型设计模块
  ├── Domain Modeler
  └── Data Model Designer
  ↓
Architecture Stage                      # 架构设计模块
  ├── Architecture Planner
  ├── API Contract Designer
  └── Project Skeleton Planner
  ↓
Planning Stage                          # 项目计划模块
  ├── Implementation Planner
  ├── Technical Debt Classifier
  └── Roadmap Planner
  ↓
Validation Stage                        # 复查验收模块
  └── Acceptance Checker
  ↓
Docs Generator
```

## State设计

```text
class MVPilotState(State):
    user_input: dict

    core_understanding_stage: dict

    modeling_stage: dict

    architecture_stage: dict

    planning_stage: dict

    validation_stage: dict
```

举例：

```text
core_understanding_stage: {
    overview: {
        "product_idea": str,
        "oneline_mvp": str,
        "target_users": str,
        "core_problem": str,
        "mvp_goal": str,
        "recommended_tech_stack": {
            "backend_language": str,
            ...
        }
        "output_summary": str,
    },
    core_flow: {}...
}
```

## 校验节点的设计
要做几个核心模块的checker。这里我们应该嗯用的是另一套提示词和API。为了就是说，能尽可能命中缓存以及尽可能保持连贯性。
比如就是说：
Architecture Boundary Checker
检查：
1. 是否有三层结构？
2. 核心业务规则是否在 service/usecase 层？
3. handler 是否直接访问数据库？
4. repository 是否包含业务判断？
5. 依赖方向是否正确？
6. 初始化连接是否有明确位置？
如果不通过的话，回退到 Architecture Stage。
Domain/Data Consistency Checker
检查：
1. 领域实体和数据表是否对应？
2. 核心业务规则是否能被数据模型表达？
3. 是否缺少关键关系表？
4. 是否把多个领域概念混成一张表？
5. 是否能支撑核心业务闭环？
如果不通过的话，回退到 Modeling Stage。
Scope Consistency Checker
检查：
1. Must Have 是否真的支撑核心闭环？
2. Defer 里是否误放了核心功能？
3. Must Have 是否包含太多高级功能？
4. Won't Have 是否影响 MVP 成立？
如果不通过的话，回退到 Core Understanding Stage。
API/Data Consistency Checker
检查：
1. API 是否覆盖核心业务流？
2. API 是否能映射到数据模型？
3. 是否有明显缺失的创建/查询接口？
4. 是否暴露了不该暴露的内部字段？
如果不通过的话，回退到 API Contract Designer 和 Data Model Designer。
## HITL节点的设计
要做几个核心模块的HITL，用户查看大概的信息和内容，决定是要：继续/重试/手动修改。
## 高缓存命中率的设计
由于我们这是一个连贯性的动作，所以我在想就是说，我们可以不断增加，每一步都增加，然后尽可能保持一个较高的缓存命中，这样子的话，连贯生成的内容也会比较稳定。

```text
[固定区]
系统提示词
工具定义
agent 行为规则

[稳定任务区]
用户原始任务
项目背景
已确认约束

[稳定代码区]
相关文件内容，顺序固定
仓库结构，顺序固定

[累积历史区]
之前工具调用和结果，按固定格式追加

[动态区]
最新工具结果
当前观察
本轮要决策的问题
```
