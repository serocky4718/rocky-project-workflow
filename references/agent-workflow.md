# Agent Workflow

## 项目入口

所有规模都使用：

- `README.md`：人类入口和快速开始。
- `AGENTS.md`：Codex 自动读取的权威 Agent 规则。
- `WORKFLOW.json`：规模、模式、角色、阶段和 PRD 确认记录；状态不构成授权。
- `PRD.md`：产品目标和验收标准。
- `TASKS.md`：当前版本任务。
- `HANDOFF.md`：展示同一阶段，解释上一阶段结论和下一步；阶段本身以 WORKFLOW 为唯一来源。

其他文件按 `project-scale-rules.md` 创建。需要跨平台说明时，可生成 `AI_RULES.md`，但只写明“权威规则见 AGENTS.md”和平台差异，不能复制一套会漂移的完整规则。

统一开工顺序和角色路由写入 `AGENTS.md` 的 Startup / Role Routing。README 只放使用说明及链接，不承载另一套“Agent 必须先读什么、何时切换角色”的规则。角色提示词只补充该职务的输入、职责和交付物。

## 执行模式

先读取 `execution-modes.md`。Guided Solo 是默认；Strict Handoff 和 Dispatcher 必须由用户明确选择。

### Guided Solo

- 同一任务可以依次执行多个阶段。
- 在输出中标注当前阶段，保持 PM、Builder、QA 的判断边界。
- 阶段之间不因形式上的角色切换停下来请求确认。
- 遇到需求冲突、外部账号、付费、公开发布、高风险操作或重大范围变化时暂停。

### Strict Handoff

- 当前任务只执行声明的角色。
- 完成后更新 `HANDOFF.md`，由用户决定何时开启下一窗口。
- QA 和 Reviewer 不直接修改实现，除非用户明确切换到 Builder。

### Dispatcher

用户明确要求多 Agent 后，才调用协作工具：

| 目的 | 当前 Codex 工具 |
|---|---|
| 创建新子 Agent | `spawn_agent` |
| 让已存在且空闲的 Agent 继续下一轮 | `followup_task` |
| 给正在运行的 Agent 补充信息 | `send_message` |
| 等待状态更新 | `wait_agent` |
| 查看状态 | `list_agents` |
| 中止当前工作 | `interrupt_agent` |

`spawn_agent` 不能“继续”已有 Agent。当前环境没有 `send_input`。如果这些能力不可用，明确说明不能自动调度，不得假装已创建 Agent。

默认不使用 `create_thread`。只有用户明确要求独立、可见的 Codex 任务窗口时，才使用线程创建能力。

Dispatcher 强制顺序：

```text
Builder -> QA -> Reviewer
```

最多三轮。任何角色结论不清时，先要求该角色补充，不自行脑补通过。

## 文档卫生

- `TASKS.md` 只保留当前活跃版本任务。
- `BACKLOG.md` 只保留未来候选事项。
- `HANDOFF.md` 只回答：当前阶段、上一阶段结论、下一步、绝对不能踩的坑。
- 报告条件和目录统一维护在项目 AGENTS 的 Reporting；严格交接本身不要求报告。
- 阶段变化按 `state-and-handoff.md` 同步 TASKS / HANDOFF 的 Stage，避免三个文件表达不同进度。
- 版本收束时把旧快照移入 `docs/archive/<version>/`。

## 新手说明

把同一目的的低风险读取和检查命令合并说明。文件写入、依赖安装、Git 写入、外部账号、费用、公开发布和数据删除要分别说明实际风险及授权要求。
