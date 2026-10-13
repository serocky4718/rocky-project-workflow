# Source Map

本技能保留通用的 PM、规模判断、角色边界、任务/Backlog/交接、验证、回滚、版本收束和资源安全能力。

0.2.0 针对当前 Codex 环境做了这些适配：

- 使用稳定调用名 `$rocky-project-workflow`。
- 使用项目根目录 `AGENTS.md` 作为 Codex 权威规则。
- 默认 Guided Solo；Strict Handoff 和 Dispatcher 显式启用。
- Dispatcher 映射到 `spawn_agent`、`followup_task`、`send_message`、`wait_agent` 等当前协作工具。
- XS/S/M/L 使用不同文档规模。
- GitHub 需要“是否同步”和“public/private”两步授权。
- 模板放入 `assets/templates/`，确定性操作放入 `scripts/`。

本技能不包含具体业务领域结构，不自动创建远程仓库、部署或使用付费服务。
