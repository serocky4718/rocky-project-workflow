# Versioning Strategy

技能调用名固定为 `rocky-project-workflow`，版本号不进入文件夹名或 `$skill` 名称。

## 当前规则版本

当前内部规则版本：`0.3.2`（与 `scripts/project_rules.py` 的 `RULE_VERSION` 一致）。

- 调用名保持稳定。
- 版本变化记录在本文件中，不在 Skill 根目录维护 `CHANGELOG.md`。
- 不并行安装多个带版本后缀的同名功能 Skill。

## 0.3.1 到 0.3.2

- 两条 PM 入口使用同一职责要求：确认后保存 PRD 正文和实际任务，再记录确认、检查就绪并交接。
- WORKFLOW 是阶段唯一来源；同步工具一起更新 TASKS / HANDOFF 的 Stage，校验阶段矛盾及 Dispatcher 的 Builder -> QA -> Reviewer 前提。
- 本地 commit 与 GitHub 访问、remote、push 的授权分开；角色按实际需求加入，报告要求放在项目 AGENTS，收尾也按规模处理。
- 状态结构仍为 schema_version 1。0.3.0 / 0.3.1 / 0.3.2 是已知兼容版本：不因版本号不同拒绝普通补齐，也不自动改写旧正文或版本号。
- 补齐缺失角色文件时使用项目现有规则版本标记；旧项目遇到实际阶段或规则冲突时，只修正所需内容。未知版本或不兼容结构仍先检查。

## 0.3.0 到 0.3.1

- README 只保存面向使用者的说明与文档导航；开工顺序和角色路由统一生成到 AGENTS。
- 八个角色输入清单统一明确 AGENTS、WORKFLOW 和 PRD；修正角色模板中与 Guided Solo 冲突的无条件停止要求。
- 项目结构校验增加 AGENTS 开工规则和角色路由检查。
- 补齐脚本仍只创建缺失提示词，不覆盖已有项目。需要使用新版规则入口时，先用 `inspect_project.py --diff` 预览，再合并 AGENTS、README 和需要的角色差异并验证；0.3.2 起版本号差异本身不再强制迁移。

## 0.1.x 迁移到 0.2.0

- `$project-create-rocky-0-1-0` 改为 `$rocky-project-workflow`。
- `AI_RULES.md` 改为 Codex 原生 `AGENTS.md`；需要跨平台时保留简短兼容文件。
- 默认执行模式从严格跨窗口改为 Guided Solo。
- GitHub 从自动触发改为两步授权：是否同步、public/private。
- XS/S 使用轻量文档，M/L 或严格协作才生成完整提示词和报告。

## 旧项目升级

1. 先读现有 `README.md`、规则文件、PRD、TASKS、HANDOFF。
2. 用 `scripts/inspect_project.py --diff` 预览；按差异补齐或移动规则，不整体覆盖用户正文。
3. 迁移到 `AGENTS.md` 时明确哪个文件是权威来源；先合并 README 中的 Agent 规则到 AGENTS，再把原位置改为链接，保留用户的项目说明。
4. 旧任务和未来想法先分类，再归档或移动。
5. 新旧规则冲突时说明风险，让用户决定是否迁移。
