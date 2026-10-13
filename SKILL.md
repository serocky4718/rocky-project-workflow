---
name: rocky-project-workflow
description: Rocky 中文项目创建与角色协作工作流。仅在用户明确调用 $rocky-project-workflow，或明确要求 Rocky 工作流、PRD 多角色交接、严格 Builder/QA/Reviewer 分工或 Dispatcher 调度时使用。支持新手需求梳理、XS/S/M/L 规模判断、按规模生成项目文档、Codex AGENTS.md、验证与回滚规则，以及经用户明确授权后的 GitHub 建库与推送。
---

# Rocky Project Workflow

把本文件作为路由入口。只读取当前任务需要的 `references/`，不要一次加载全部规则。

## 默认原则

- 默认使用 `Guided Solo`：同一任务内按 PM、Builder、QA 阶段持续推进，不因角色切换反复停下。
- 仅在用户明确要求严格跨窗口交接时使用 `Strict Handoff`。
- 仅在用户明确要求 Dispatcher、多 Agent 或 Builder/QA/Reviewer 子 Agent 时使用 `Dispatcher`。
- 先确认 PRD，再按项目规模生成文件；不要给 XS/S 项目套完整文档体系。
- 生成 Codex 原生 `AGENTS.md`。`AI_RULES.md` 仅在用户需要跨平台副本时生成，并指向 `AGENTS.md` 作为权威来源。
- `README.md` 面向使用者，保存项目介绍、运行步骤和文档链接；统一开工顺序、角色路由、权限与交接规则放在 `AGENTS.md`，角色专属职责放在职位提示词中。
- GitHub 是可选外部操作。先确认是否同步到 GitHub；用户同意后再确认 `public` 或 `private`。
- 修改文件、运行命令或访问外部账号前，按风险等级批量说明，不为每条低风险读取命令重复打断用户。

## 推荐启动语

```text
使用 $rocky-project-workflow 帮我创建一个新项目。
先进入 PM 阶段讨论需求，不要写代码；PRD 确认后再生成与项目规模匹配的文档。
```

## 核心流程

```text
启用技能
-> PM 需求探讨
-> 判断 XS / S / M / L
-> 推荐执行模式和交付规模
-> 用户确认 PRD
-> 预览将创建的文件
-> 按规模生成项目文件
-> 保存已确认需求、实现任务和确认来源
-> 同步项目阶段与交接并检查就绪
-> 按 Guided Solo / Strict Handoff / Dispatcher 推进
-> 可选：用户明确授权后同步 GitHub
```

## 路由表

| 触发条件 | 读取文件 |
|---|---|
| 创建新项目、进入 PM | `references/roles/pm.md` -> `references/pm-discovery-flow.md` -> `references/project-scale-rules.md` -> `references/execution-modes.md` -> `references/output-file-templates.md` |
| 用户询问 Builder 模型选择 | `references/builder-model-selection-rules.md` |
| 选择执行模式 | `references/execution-modes.md` -> `references/agent-workflow.md` |
| 进入某个角色 | `references/role-delivery-rules.md` -> 对应的 `references/roles/<role>.md` |
| 启动 Dispatcher / 多 Agent | `references/execution-modes.md` -> `references/roles/dispatcher.md` -> `references/role-prompts.md` |
| 生成项目骨架 | `references/project-scale-rules.md` -> `references/output-file-templates.md`；优先使用 `scripts/init_project.py` |
| 记录 PRD 确认、更新阶段或交接 | `references/state-and-handoff.md`；优先使用 `scripts/update_workflow.py`，同步前预览，进入实现前做就绪检查 |
| 检查或补齐职位提示词、角色入口 | `references/role-prompts.md` -> `references/readme-role-entry.md`；`scripts/sync_role_prompts.py` 只补齐缺失提示词，已有 README / AGENTS 入口按差异合并 |
| 设计目录、资源或数据放置 | `references/project-structure.md` -> `references/asset-and-data-rules.md` |
| 需要角色报告 | `references/report-templates.md` |
| GitHub 建库或 push | `references/github-automation-rules.md` -> `references/safety-rules.md` |
| 修改文件或运行命令 | `references/safety-rules.md` |
| 验证或回滚 | `references/validation-rules.md` -> `references/rollback-rules.md` |
| 失败恢复 | `references/failure-recovery-rules.md` |
| 版本收束 | `references/version-closure-rules.md` |
| 技能升级或旧项目迁移 | `references/versioning-strategy.md` |
| 平台适配或规则来源 | `references/platform-adapter-rules.md` -> `references/source-map.md` |

## 规模化最低输出

| 规模 | 最低输出 |
|---|---|
| XS | `README.md`、`AGENTS.md`、`PRD.md`、`TASKS.md`、`HANDOFF.md` |
| S | XS + `BACKLOG.md` |
| M | S + `PRD_CURRENT.md`、`PROJECT_STRUCTURE.md`、`ARCHITECTURE.md`、`CHANGELOG.md`、必要的 `docs/` |
| L | M + 版本归档、必要报告目录；角色提示词按执行模式创建，设计、CI、部署目录按实际需求创建 |

严格交接或 Dispatcher 模式需要的角色提示词、报告目录，可以覆盖上述最低输出；只创建当前流程真正会使用的目录。

生成脚本还会创建 `WORKFLOW.json` 记录规模、模式、角色、阶段和确认来源；初始骨架不表示 PRD 已确认或项目已可实现。

## 新手说明

在一组相关操作开始前，一次说明：

```text
我要做什么
为什么要这样做
会改哪些文件或运行哪些命令
风险等级和具体风险
成功标志是什么
是否需要用户授权
```

低风险、只读、同一目的的命令可以合并说明。外部账号、费用、公开发布、push、部署和破坏性操作必须单独说明并取得所需授权。
