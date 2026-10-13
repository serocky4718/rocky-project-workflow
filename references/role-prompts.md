# Role Prompts

八个职位的提示词已经预先编写在 `references/roles/`，包含职责、输入、工作流程、限制和完成标志，不是空文件。Guided Solo 按需读取技能内的对应角色参考；Strict Handoff 或 Dispatcher 按所选角色复制到项目的 `docs/agent-prompts/`。

## 复制规则

- 新项目由 `scripts/init_project.py` 同时生成 AGENTS 角色路由、README 链接和所选提示词；已有项目使用 `scripts/sync_role_prompts.py` 只补齐缺失的提示词。
- 补齐脚本不会更新已有提示词、README 或 AGENTS。修改入口或升级模板时，先用 `scripts/inspect_project.py --diff` 预览，再合并所需差异。
- 给每份项目副本写入项目名、规模、执行模式和生成日期。
- 项目副本必须自包含，不得引用 Skill 安装目录中的 `references/`。
- Codex 会自动读取项目根目录 `AGENTS.md`，职位 Prompt 只补充当前职责。
- 各角色输入清单明确包含 `AGENTS.md` 和 `WORKFLOW.json`；README 按需用于理解项目，不充当执行规则。
- Guided Solo 默认不生成八份职位文件。

## 模板映射

| 角色 | 负责什么 | 已编写模板 | 项目副本 |
|---|---|---|---|
| PM | 梳理需求、PRD 和任务 | `references/roles/pm.md` | `docs/agent-prompts/pm.md` |
| Architect | 架构、目录与技术边界 | `references/roles/architect.md` | `docs/agent-prompts/architect.md` |
| Dispatcher | 调度 Builder、QA、Reviewer | `references/roles/dispatcher.md` | `docs/agent-prompts/dispatcher.md` |
| Builder | 实现代码与必要验证 | `references/roles/builder.md` | `docs/agent-prompts/builder.md` |
| QA | 测试、复现与验收证据 | `references/roles/qa.md` | `docs/agent-prompts/qa.md` |
| Reviewer | 评审缺陷、回归与风险 | `references/roles/reviewer.md` | `docs/agent-prompts/reviewer.md` |
| Designer | 页面、交互与候选资源 | `references/roles/designer.md` | `docs/agent-prompts/designer.md` |
| DevOps/GitHub | 获授权后处理仓库与发布 | `references/roles/devops-github.md` | `docs/agent-prompts/devops-github.md` |

## 启动示例

已生成 QA 项目副本的 Strict Handoff 项目可以使用：

```text
进入本项目的 QA 角色，按 AGENTS 的开工和角色路由规则读取项目文件。
只执行 QA 职责，记录验证证据和结论。
```

Dispatcher 使用 `spawn_agent` 创建新 Agent，使用 `followup_task` 继续已有 Agent，使用 `send_message` 补充运行中 Agent 的信息，并使用 `wait_agent` 等待状态更新。
