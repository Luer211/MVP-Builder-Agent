# Technical Debt

## Principle

第一版允许“实现粗糙”，不允许“边界混乱”。

可以欠的债是体验和自动化，不可以欠的债是领域模型、状态结构、文档清单和架构依赖方向。

## Acceptable Technical Debt

MVP 阶段可以接受：

- 同步生成，不做异步队列。
- 本地文件系统持久化，不引入数据库。
- 简单日志，不接观测平台。
- 简单错误处理，不做复杂恢复。
- Prompt 模板先放在代码仓库中。
- checker 节点暂不接入主流程。
- HITL 节点暂不接入主流程。
- 没有 Web 前端。
- 没有用户系统。
- 没有 token 成本统计。

这些债不会破坏核心生成闭环。

## Dangerous Technical Debt

不能接受：

- API handler 直接拼 prompt。
- API handler 直接写 12 个 Markdown。
- 节点输出不受 schema 约束。
- 文档文件名由模型决定。
- state 结构只有一个大字符串。
- 每个节点都各自决定上下文格式。
- Markdown 渲染逻辑散落在节点里。
- 错误 run 被标记为 completed。
- 文档数量不稳定。
- 文档之间核心事实互相冲突。

这些债会直接破坏后续迭代和 Codex 可读性。

## Debt Review Rules

判断一项技术债是否危险，看三个问题：

1. 它会不会让输出文档不稳定？
2. 它会不会让后续 checker/HITL 难以接入？
3. 它会不会让 Codex 读 docs 后误解项目边界？

如果任意一个答案是“会”，就不应该进入第一版主干。

## Refactoring Triggers

出现这些情况必须还债：

- 同一类 prompt 在多个节点中重复且开始分叉。
- 生成文件数量偶发不一致。
- 新增 checker 时需要改大量旧节点。
- 输出目录写入逻辑开始散落。
- API 响应和 manifest 对不上。
- state 字段含义开始不清晰。
- 用户输入稍微复杂就导致文档冲突。

## Deferred Improvements

后续可以规划：

- checker 自动回退。
- HITL 审批和局部修改。
- 任务历史数据库。
- Web UI。
- prompt 版本管理。
- 多模型策略。
- 生成成本统计。
- docs 到项目骨架的下一步自动化。
