# Project Scale Rules

在 PM 前 1–2 轮根据实际复杂度判断规模，用于决定流程和文档重量。先给出推荐；只有用户选择会显著改变范围、成本或风险时才要求确认。

## 规模与默认流程

| 规模 | 判断特征 | 默认流程 | 最低输出 |
|---|---|---|---|
| XS | 单页、静态页、一次性小脚本 | PM -> Builder -> QA | `README.md`、`AGENTS.md`、`PRD.md`、`TASKS.md`、`HANDOFF.md` |
| S | 小工具、轻量 Web App、无复杂权限 | PM -> Builder -> QA | XS + `BACKLOG.md` |
| M | 多页面、登录、数据库、后台或第三方 API | PM -> Architect -> Builder -> QA -> Reviewer | S + `PRD_CURRENT.md`、`PROJECT_STRUCTURE.md`、`ARCHITECTURE.md`、`CHANGELOG.md`、必要的 `docs/` |
| L | 支付、多人权限、安全边界、复杂数据、CI/部署 | PM -> Architect -> Builder -> QA -> Reviewer；独立设计时加 Designer，需要仓库或发布工作时加 DevOps | M + 版本归档、必要报告目录；角色提示词按执行模式创建，其余目录按需创建 |

## 判断问题

优先从用户描述推断，只补问会改变规模的问题：

- 是否涉及登录、数据库、支付、后台、AI、上传或第三方 API？
- 是否有多人权限、安全、迁移、生产部署或 CI？
- 项目是一次性交付，还是长期维护？

## 覆盖规则

- `Strict Handoff` 或 `Dispatcher` 会额外生成所选角色提示词；报告目录按项目 AGENTS 的 Reporting 和实际内容需要创建。
- `Guided Solo` 按阶段推进，不因项目是 L 规模就复制全部职位文件。
- Strict Handoff 默认 XS/S 使用 PM、Builder、QA，M/L 加 Architect、Reviewer。独立设计、仓库或发布任务明确需要时，用初始化脚本的 `--roles designer devops-github` 等选项加入对应角色；只加入实际需要的角色。
- 生成 DevOps 提示词只是准备职责说明，不构成外部授权。角色名单在初始化前确定，已有项目变更名单先预览差异再合并。
- GitHub、部署和 CI 只在用户明确需要时加入，不由规模自动授权。
- `package.json`、`pyproject.toml`、`go.mod` 等只按真实技术栈创建。
- 不为了满足模板创建空目录或空报告。

## 成功标志

```text
规模和理由已写清
执行模式已选择
输出文件与规模匹配
跳过的角色或文件不会影响验收
```
