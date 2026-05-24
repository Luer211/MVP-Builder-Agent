# Acceptance Criteria

## Functional Acceptance

第一版功能验收：

- 用户可以提交一段产品想法。
- 系统可以完成一次正向生成流程。
- 系统稳定生成 12 个 Markdown 文件。
- 12 个文件名固定且顺序稳定。
- 生成文件写入指定输出目录。
- API 返回 run_id、status、output_dir、files。
- 输入为空或过短时返回明确错误。
- 输出目录冲突时返回明确错误或按 `overwrite` 处理。

目标文件：

```text
00_overview.md
01_core_flow.md
02_scope.md
03_domain_model.md
04_data_model.md
05_architecture.md
06_api_contract.md
07_project_skeleton.md
08_implementation_plan.md
09_technical_debt.md
10_iteration_roadmap.md
11_acceptance_criteria.md
```

## Architecture Acceptance

架构验收：

- FastAPI 只负责 HTTP 边界。
- LangGraph 负责生成流程编排。
- 节点输出写入 state。
- Pydantic schema 约束请求、响应和核心 state。
- Markdown 渲染集中在 rendering 模块。
- 文件写入集中在 storage 模块。
- API 层不直接调用底层文件写入细节。
- checker 和 HITL 没有被硬编码进第一版主流程。

## Data Model Acceptance

数据模型验收：

- `MVPilotState` 能表达所有阶段输出。
- `GeneratedDocument` 能表达最终文件。
- 文档清单是固定白名单。
- run metadata 至少能表达 run_id、status、output_dir、files。
- 不需要数据库也能完成一次生成。

## API Acceptance

API 验收：

- `POST /api/v1/doc-runs` 可触发生成。
- `GET /api/v1/doc-runs/{run_id}` 可查看 run 摘要。
- `GET /api/v1/doc-runs/{run_id}/files` 可查看文件清单。
- `GET /api/v1/doc-runs/{run_id}/files/{file_name}` 可读取文件。
- API 错误响应结构统一。
- 不暴露内部 prompt。

## Document Quality Acceptance

文档质量验收：

- `00_overview.md` 能说明项目是什么。
- `01_core_flow.md` 能说明核心闭环。
- `02_scope.md` 能说明做什么和不做什么。
- `03_domain_model.md` 能说明核心领域对象。
- `04_data_model.md` 能说明核心数据结构。
- `05_architecture.md` 能说明架构边界。
- `06_api_contract.md` 能说明核心接口。
- `07_project_skeleton.md` 能说明目录结构。
- `08_implementation_plan.md` 能说明开发顺序。
- `09_technical_debt.md` 能说明可接受和危险技术债。
- `10_iteration_roadmap.md` 能说明后续迭代路线。
- `11_acceptance_criteria.md` 能说明验收标准。

## Non-goals

第一版不验收：

- 自动生成业务代码。
- Web UI。
- 用户登录。
- 数据库任务历史。
- checker 自动回退。
- HITL 人工审批。
- 多模型路由。
- 成本统计。
- 队列和异步 worker。
- 生产级部署方案。

只要正向文档生成闭环稳定，第一版就成立。
