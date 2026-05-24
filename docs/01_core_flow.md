# Core Flow

## Core User Loop

用户的核心闭环是：

```text
输入产品想法
-> 系统理解核心需求
-> 系统生成 MVP 文档集
-> 用户或 Codex 阅读 docs
-> 开始搭建项目骨架
```

这个闭环的重点是“先生成可开发文档”，不是“直接生成完整代码”。

## Primary Actors

- User：输入产品想法，指定少量偏好，例如语言、框架、数据库。
- MVP Builder Agent：负责理解需求、拆分阶段、生成文档内容。
- Codex：后续读取生成的 docs，并基于 docs 搭建项目骨架。

第一版中 User 和 Codex 不需要复杂账号体系或权限区分。

## Main Scenario

1. 用户提交一段自然语言需求。
2. 系统保存一次生成任务的输入。
3. Core Understanding Stage 生成项目总览、核心业务闭环和 MVP 范围。
4. Modeling Stage 生成领域模型和数据模型。
5. Architecture Stage 生成架构边界、API 契约和项目骨架。
6. Planning Stage 生成实施计划、技术债说明和后续迭代路线。
7. Validation Stage 生成验收标准。
8. Docs Generator 将结构化结果渲染为 12 个 Markdown 文件。
9. 用户在 `docs/` 或指定输出目录中查看结果。

## Alternative Scenarios

- 用户输入过短：系统仍生成文档，但在文档中明确列出假设。
- 用户指定技术栈：系统优先使用用户指定技术栈，不再自动推荐冲突方案。
- 用户没有指定技术栈：系统根据项目类型推荐保守技术栈。
- 生成失败：API 返回错误信息，不写出半成品文档，或写出带失败标记的 run 目录。

## Out of Core Flow

第一版不做这些能力：

- 代码生成。
- 自动创建 GitHub 仓库。
- 多用户协作。
- 文档在线编辑器。
- 复杂 HITL 审批流。
- 自动重试和多轮自修复。
- 持久化任务历史数据库。
- 多模型路由和成本优化系统。

这些能力可以在正向生成闭环稳定后再迭代。
