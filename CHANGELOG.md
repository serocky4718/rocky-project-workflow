# Changelog

## 0.3.2 — 2026-10-13

- 技能与仓库统一命名为 `rocky-project-workflow`，调用名保持稳定。
- 默认在同一窗口推进；严格交接和 Dispatcher 由用户明确选择。
- README 提供使用导航，AGENTS 承担项目统一执行规则，八个角色提示词按需生成。
- 增加项目骨架、角色补齐、阶段同步、只读预览和结构 / 就绪检查脚本。
- 确认需求后保存正文和实际任务，阶段矛盾、调度越序与过期验证结果会被检查。
- 本地 commit 与 GitHub 授权分开，项目文档、报告和收尾按规模处理。
- 已知 0.3.x 状态兼容；补齐操作保留旧版本标记与用户正文，未知结构先检查。
- 保留四项可重复执行的关键行为回归检查。

## 0.1.0

初始 Rocky 版。

- 建立 PM -> Architect -> Builder -> QA -> Reviewer -> DevOps/GitHub 的手动跨窗口交接规则。
- 建立 PM 需求探讨到 PRD 确认的流程。
- 建立 README Agent Role Entry 导航规则。
- 建立项目内 `docs/agent-prompts/<role>.md` 职位提示词规则。
- GitHub 建库只保留 public/private 一个用户决策点。

## 0.1.0 时的计划（历史）

候选方向：

- 增加项目初始化脚本，把 reference 模板复制到新项目。
- 增加更多技术栈模板，例如 Python、Go、静态站、Next.js、CLI 工具。
- 增加更细的部署平台规则，例如 Vercel、GitHub Pages、Docker。
- 增加多平台 AI 接口元数据，例如 OpenAI、通用 Markdown、其他 Agent 平台。

## 兼容策略

当前兼容策略以 `references/versioning-strategy.md` 为准。旧的 0.1.x 项目先预览迁移差异，按需要合并规则并保留用户正文。

- 0.1.x 只做文档规则补强，不破坏已生成项目的文件名。
- 0.2.0 可以新增文件，但默认不重命名 `PRD.md`、`TASKS.md`、`HANDOFF.md`、`docs/agent-prompts/`。
- 已有项目升级时，优先追加新小节，不覆盖用户已经写过的正文。
