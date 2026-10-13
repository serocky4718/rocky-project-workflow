# Output File Templates

优先使用 `assets/templates/` 和 `scripts/init_project.py` 生成稳定骨架。本文件定义语义，不要求所有项目生成全部文件。

## 所有规模

### `README.md`

包含项目简介、快速开始、当前状态和项目文档入口。Strict Handoff 或 Dispatcher 模式再加入 Agent Role Entry。

README 面向使用者，只解释如何打开项目、运行项目和选择角色；角色入口是文档导航。统一开工顺序、角色路由、权限、验证与交接规则放在 `AGENTS.md`，不要在 README 再维护一份执行规则。

### `AGENTS.md`

Codex 自动读取的权威规则，至少包含：

```md
# Agent Instructions

## Project Goal
## Instruction Sources
## Working Mode
## Startup
## Role Routing
## File Ownership
## Before Editing Or Running Commands
## Validation
## Reporting
## Handoff
## Safety
```

Startup 规定先读取适用的 Agent 规则、`WORKFLOW.json`、PRD、TASKS、HANDOFF。Role Routing 只列当前模式实际生成的角色提示词；Guided Solo 写明按阶段推进，不引用未生成的角色文件。

### `WORKFLOW.json`

脚本生成的状态文件，记录规模、模式、角色、阶段及 PRD 确认来源。骨架初始化为未确认；PM 只能在用户已确认后记录事实，不能把模板生成当作确认。

它是阶段的唯一状态来源，TASKS / HANDOFF 的 Stage 同步展示该阶段；优先用 `scripts/update_workflow.py` 一起更新，进入实现前检查就绪。

### `PRD.md`

包含背景、用户、问题、目标、MVP、本阶段不做、流程或模块、数据和权限、验收标准、风险。

### `TASKS.md`

只保存当前版本任务，建议字段：ID、状态、优先级、负责人、任务、验收标准、依赖。

### `HANDOFF.md`

只回答：

```text
1. 当前项目处于什么阶段？
2. 上一阶段完成了什么判断？
3. 下一步具体做什么？
4. 有哪些绝对不能踩的坑？
```

## S 及以上

### `BACKLOG.md`

保存未进入当前版本的候选事项，并说明为什么现在不做以及重新考虑的触发条件。

## M 及以上

- `PRD_CURRENT.md`：当前执行切片、已确认决策、开放问题、验收标准和下一阶段。
- `PROJECT_STRUCTURE.md`：真实技术栈的目录地图、归属和验证命令；不要默认写入 `package.json`。
- `ARCHITECTURE.md`：技术栈、模块边界、数据流、风险与取舍。
- `CHANGELOG.md`：重要产品和实现变化。
- `docs/prd/`、`docs/reports/`：只创建会使用的子目录。

## 按执行模式或交付需要

- `docs/archive/`：旧版本状态快照。
- `docs/agent-prompts/`：Strict Handoff / Dispatcher 所选角色的项目内自包含提示词；Guided Solo 不因规模较大就生成八份文件。
- `docs/reports/<role>/`：角色报告；不要预先生成空报告。
- `docs/design/`、`docs/assets/`、`.github/` 和部署配置：仅在真实需求存在时创建。

## `AI_RULES.md` 可选兼容文件

仅在需要支持不会自动读取 `AGENTS.md` 的其他平台时创建：

```md
# AI Rules Compatibility Note

本项目的权威 Agent 规则位于 `AGENTS.md`。
本文件只记录当前平台差异，不复制完整规则。
```
