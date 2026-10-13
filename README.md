# Rocky Project Workflow

面向开发新手的 Codex 技能：先把想法整理成明确的需求，再按项目大小生成必要文件，完成开发、验证和交接。

当前规则版本为 **0.3.2**。仓库、技能目录和调用名统一使用 `rocky-project-workflow`。

## 首次安装

在 PowerShell 中运行：

```powershell
git clone https://github.com/serocky4718/rocky-project-workflow.git "$env:USERPROFILE\.codex\skills\rocky-project-workflow"
```

这会下载公开仓库并创建技能目录。已有同名目录时先保留现有修改，不直接覆盖。

成功标志：目录中存在 `SKILL.md`，其中的技能名是 `rocky-project-workflow`。

## 使用方式

在 Codex 中输入：

```text
使用 $rocky-project-workflow 帮我创建一个新项目。
先讨论需求，PRD 确认后按项目规模生成文件，默认在同一窗口继续开发和验证。
```

成功标志：助手先讨论需求；确认后把正文和实际任务保存好，再进入下一阶段。文件是否存在与项目是否可以开工会分别检查。

## 三种执行方式

| 模式 | 适合什么情况 |
|---|---|
| Guided Solo（默认） | 同一个窗口连续完成需求、开发和验证 |
| Strict Handoff | 用户明确要求不同窗口分别承担角色 |
| Dispatcher | 用户明确要求子 Agent 按开发、测试、评审顺序工作 |

技能已编写八个角色的提示词：PM、Architect、Designer、Dispatcher、Builder、QA、Reviewer、DevOps/GitHub。项目按实际模式和需求使用对应角色，小项目不会默认复制全部文件。

## 生成的项目文件

所有规模都有 README、AGENTS、PRD、TASKS、HANDOFF 和 WORKFLOW 状态文件。较大的项目按需增加当前需求切片、架构、文件地图、报告和归档。

| 文件 | 作用 |
|---|---|
| README.md | 给使用者看的项目说明、运行步骤和文档导航 |
| AGENTS.md | AI 的统一开工、角色、验证、报告和交接规则 |
| PRD.md | 已确认的需求及验收标准 |
| TASKS.md | 当前任务 |
| WORKFLOW.json | 当前阶段及确认记录 |
| HANDOFF.md | 展示同一阶段，说明上一阶段结论和下一步 |

GitHub 同步是单独的可选操作，需要用户授权并确定仓库可见性；本地保存代码版本与上传远程分开处理。

## 本仓库的文件

- [SKILL.md](SKILL.md)：技能入口和路由。
- [references/](references/)：需求、规模、模式及交接规则。
- [references/roles/](references/roles/)：八个职务提示词。
- [assets/templates/](assets/templates/)：项目文档模板。
- [scripts/](scripts/)：生成、补齐、进度同步、检查及回归测试工具。
- [版本策略](references/versioning-strategy.md)：当前版本与兼容说明。

README 是仓库的使用说明；技能执行规则由 SKILL 和对应参考文件提供，生成项目的统一规则放在项目 AGENTS 中。

## 修改技能后的本地检查

在仓库目录运行：

```powershell
python -X utf8 -B scripts/test_workflow.py --work-dir work/checks
```

该命令只在 `work/checks` 下生成隔离示例，不访问外部账号。成功标志：四项关键行为检查显示 `OK`，包括需求确认、交接状态、调度顺序和兼容版本保留用户内容。
