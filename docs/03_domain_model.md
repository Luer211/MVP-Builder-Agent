# Domain Model

## Core Concepts

MVP Builder Agent 的核心领域不是通用聊天，而是“产品想法到 MVP 文档集”的工程化转换。

核心概念包括：

- Product Idea：用户输入的原始产品想法。
- Generation Run：一次完整的文档生成任务。
- Generation Stage：文档生成流程中的阶段。
- Stage Output：某个阶段生成的结构化内容。
- Document Spec：目标文档的定义。
- Document Artifact：最终写出的 Markdown 文件。
- Project Assumption：系统在需求不完整时做出的显式假设。

## Entities

### ProductIdea

用户输入的原始需求。

核心属性：

- raw_text
- preferred_tech_stack
- target_output_dir
- constraints

### GenerationRun

一次生成任务。

核心属性：

- run_id
- input
- status
- state
- output_files
- errors
- created_at
- completed_at

### GenerationStage

一个生成阶段。

核心属性：

- stage_name
- depends_on
- output_schema
- prompt_template
- status

### DocumentArtifact

最终 Markdown 文档。

核心属性：

- file_name
- title
- content
- source_stage
- write_path

## Value Objects

### TechStackPreference

表示用户偏好的技术栈。

字段：

- backend_language
- framework
- database
- cache
- deployment

### ProjectAssumption

表示系统补足的不确定信息。

字段：

- assumption
- reason
- impact

### ValidationNote

第一版只用于记录，不做自动回退。

字段：

- target
- severity
- message
- suggested_fix

## Domain Relationships

```text
ProductIdea
  -> GenerationRun
      -> GenerationStage[]
          -> StageOutput
      -> DocumentArtifact[]
```

一个 `GenerationRun` 只能对应一个用户输入，但会生成多个阶段输出和 12 个文档 artifact。

`DocumentArtifact` 不直接调用模型，它只由结构化 stage output 渲染得到。

## Business Rules

- 每次生成必须从同一个 `ProductIdea` 出发。
- 阶段输出必须写入 state，不能只存在于 prompt 上下文。
- 后续阶段只能依赖前序阶段的结构化输出。
- 文档生成必须由固定文档清单驱动。
- 输出文档数量第一版固定为 12 个。
- 如果需求缺失，系统要显式写出假设，而不是隐藏猜测。

## Non-negotiable Domain Constraints

- 不能把“用户输入”“中间状态”“最终文档”混成一个字符串。
- 不能让每个节点自由决定输出文件名。
- 不能让文档渲染逻辑散落在各个 agent 节点里。
- 不能在 API handler 中直接拼 prompt 或写文档内容。
- 不能让失败的 run 看起来像成功生成。
