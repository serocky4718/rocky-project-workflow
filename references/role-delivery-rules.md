# Role Delivery Rules

角色代表职责边界，不一定代表独立窗口。先读取 `execution-modes.md`：Guided Solo 可以在同一任务切换阶段；Strict Handoff 和 Dispatcher 才使用严格角色锁。

## 通用规则

- 不越过已确认的 PRD 和验收标准。
- 修改或命令按 `safety-rules.md` 分级说明。
- 只创建项目规模和执行模式需要的交付物。
- XS/S 的简单阶段可以只更新 `TASKS.md` 与 `HANDOFF.md`，不强制制造角色报告。
- 报告是否需要和目录以项目 AGENTS 的 Reporting 为准；生成时参照 `report-templates.md`。严格交接本身不要求额外报告。
- 用户要求“只分析”时，不写文件并明确说明。

## PM

负责目标、范围、优先级、验收标准、PRD、当前任务和 Backlog，不写业务代码、不安装依赖、不部署、不执行 Git 写入。

PRD 确认后只完成本地项目文件。GitHub 必须作为单独可选步骤：先确认用户是否要同步，再确认 public/private。

## Architect

负责 `AGENTS.md`、架构、目录、模块边界、数据流、技术选择和验证命令。默认不实现业务功能，不擅自更换依赖、构建或部署方案。

`AGENTS.md` 是 Codex 权威规则。若生成 `AI_RULES.md`，只保留跨平台差异并指向 `AGENTS.md`。

## Builder

负责源码、配置、必要依赖、测试和实现验证。

- 修改前说明范围、原因、风险和成功标志。
- 不扩大需求，不覆盖用户无关改动。
- 大改前建议 checkpoint 或至少记录 `git status`、`git diff --stat`。
- 不未经授权部署、push、删除文件或更换技术栈。

## QA

负责验证、复现和通过/失败结论。

- Strict Handoff / Dispatcher：QA 不修实现，失败交回 Builder。
- Guided Solo：可以在明确标注“切回 Builder 阶段”后修复，再回到 QA 复测；无需因形式上的角色切换请求额外确认。
- 任何模式都不能隐瞒失败、删除数据或为了通过而跳过验证。

## Reviewer

负责按严重程度指出 bug、回归、安全风险和测试缺口。Strict Handoff / Dispatcher 下不直接修代码；Guided Solo 下可明确切回 Builder 阶段处理。

## Designer

负责页面结构、交互状态、视觉规则和候选资源。候选资源先放临时输出目录；未经用户确认不覆盖正式素材、不进入正式资源目录。

## DevOps / GitHub

负责仓库、remote、CI 和部署，但需要分别获得授权：

1. 用户明确同意把项目同步到 GitHub。
2. 用户明确选择 public 或 private。
3. 部署到公网时另行取得部署授权。

授权后可从项目上下文推导仓库名、描述、`.gitignore`、remote 和首次提交策略，不反复询问低价值细节。push 前必须检查敏感文件和当前 Git 状态。

## Handoff

需要下一阶段或下一窗口时，`HANDOFF.md` 只保留：当前阶段、上一阶段结论、下一步、绝对不能踩的坑。以 WORKFLOW 的阶段为唯一状态来源，同步 TASKS / HANDOFF 的 Stage；按 `state-and-handoff.md` 更新并检查一致性。Guided Solo 不为每个微小步骤重写交接。
