# Iteration Roadmap

## V0.1 MVP

目标：跑通正向文档生成闭环。

交付：

- FastAPI 服务入口。
- LangGraph 直线生成流程。
- 固定 12 个目标文档。
- Pydantic schema。
- Markdown 渲染器。
- 本地文件系统输出。
- 基础 API。
- 基础错误处理。

验收：

- 输入一段产品想法后，稳定生成 `00` 到 `11` 共 12 个 Markdown 文件。

## V0.2 Usability

目标：提升本地开发和使用体验。

可能交付：

- CLI 入口。
- 更清晰的 run manifest。
- 输出目录模板。
- 更好的错误提示。
- 示例输入和示例输出。
- 基础测试覆盖。

不做：

- 复杂前端。
- 多用户系统。
- 自动代码生成。

## V0.3 Validation

目标：接入轻量 checker，但不引入复杂自修复。

可能交付：

- Scope Consistency Checker。
- Domain/Data Consistency Checker。
- API/Data Consistency Checker。
- Architecture Boundary Checker。
- checker findings 写入文档或 manifest。

第一阶段 checker 只给出问题，不自动回退。

## V0.4 HITL

目标：让用户能在关键阶段做选择。

可能交付：

- 阶段性预览。
- 继续 / 重试 / 手动修改。
- 用户修改后的 state merge。
- HITL 决策记录。

风险：

- 容易把简单工具做成复杂工作台。
- 需要明确哪些节点值得人工确认。

## V0.5 Reliability

目标：提升稳定性和可复现性。

可能交付：

- prompt 版本管理。
- run history。
- 失败重试。
- 生成结果 diff。
- 更严格 schema 校验。
- 回归测试样例集。

## V1.0 Productization

目标：从本地开发工具变成可长期使用的产品。

可能交付：

- Web UI。
- 用户系统。
- 项目空间。
- 数据库存储。
- 多模型配置。
- 成本统计。
- 导出项目骨架。
- 与 Codex 工作流进一步衔接。

## Deferred Ideas

暂不进入第一版：

- 自动生成代码。
- 自动创建仓库。
- 自动执行测试。
- 多 agent 并行评审。
- 复杂权限和组织管理。
- 生产级观测系统。
