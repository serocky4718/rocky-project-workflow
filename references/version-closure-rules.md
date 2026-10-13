# Version Closure Rules 版本收束和文档清理规则

本文件定义一个版本完成、暂停、转入下一版本时，如何保持项目文档干净。

核心目标：让新窗口接手时，只看到当前最重要的信息，不被旧任务、旧判断、未来想法干扰。

## 触发时机

出现以下情况时，必须执行版本收束：

- 当前版本 MVP 已验收通过。
- 用户明确说“这个版本结束”“收束一下”“进入下一版本”。
- Builder、QA、Reviewer 完成一个闭环，下一步要进入新范围。
- 当前任务太多太乱，已经影响下一位 Agent 判断。

收束按规模和实际目的执行，先整理已有文件。XS/S 的一次性小项目完成时，保留已完成任务和简短验收证据，同步 WORKFLOW / TASKS / HANDOFF 为 closed，不默认新增 Backlog、Changelog 或归档目录。只是整理当前任务时保持实际阶段，不误标为已完成。

M/L 或确实要开启新版本时，先保存旧任务、交接和必要需求快照再清理入口；已有 Changelog 才更新它。下一版本返回 PM，用 `--reopen-prd` 清除旧确认及调度结果，不能沿用上一版本的确认执行新范围。

## 收束前说明

执行前必须向用户说明：

```text
我要做什么：整理当前版本文档并归档旧内容
为什么做：让 TASKS 和 HANDOFF 保持只服务当前版本
会改哪些文件：本项目已有的 TASKS.md、HANDOFF.md、WORKFLOW.json，以及本次确有需要的 Backlog、Changelog 或归档
风险是什么：可能把旧内容移动到归档，当前入口会更精简
成功标志是什么：新窗口只读 HANDOFF 和 TASKS 就能知道下一步
```

## TASKS.md 清理规则

`TASKS.md` 只保留当前活跃版本内容。

允许保留：

- 当前版本待做任务。
- 当前版本正在做的任务。
- 当前版本阻塞任务。
- 当前版本刚完成、仍影响验收的任务。

必须移走：

- 已关闭旧版本任务。
- “以后可以做”的想法。
- 未进入当前版本范围的优化。
- 长篇历史过程记录。

移动规则：

- 未来可能做的内容移入已有 `BACKLOG.md`；XS 没有该文件时，可在对话中提出建议，用户要求保存候选事项时再创建。
- 真正开启下一版本或 M/L 正式收束时，把旧版本已完成记录归档到 `docs/archive/<version>/TASKS.md`；XS/S 单次交付保留已完成记录即可。
- 决策过程和长报告归档到 `docs/archive/<version>/` 或 `docs/reports/`。

## BACKLOG.md 规则

`BACKLOG.md` 专门放“不急，但未来可能做”的内容。

推荐结构：

```md
# Backlog

## Candidate Ideas

| ID | Source | Idea | Why Later | Trigger |
|---|---|---|---|---|
| B-001 | PM | <未来想法> | <为什么现在不做> | <什么情况下再做> |

## Parking Lot

## Rejected For Now
```

要求：

- 不把 Backlog 内容混进 `TASKS.md`。
- 每条 Backlog 都要写清“为什么不是现在做”。
- 只有 PM 或用户确认进入当前版本后，才从 `BACKLOG.md` 移入 `TASKS.md`。

## HANDOFF.md 清理规则

`HANDOFF.md` 只承担交接功能，不做历史流水账。

必须回答四个问题：

```text
1. 当前项目处于什么阶段？
2. 上一棒完成了什么判断？
3. 下一棒具体要做什么？
4. 有哪些绝对不能踩的坑？
```

禁止写入：

- 长篇过程复盘。
- 已完成旧版本的完整任务列表。
- 未来可能做但未进入当前版本的想法。
- 和下一棒行动无关的背景资料。

## docs/archive/ 规则

归档目录用于保存旧内容，不作为当前工作入口。

推荐结构：

```text
docs/archive/
  <version>/
    PRD_CURRENT.md
    TASKS.md
    HANDOFF.md
    release-notes.md
```

归档要求：

- 旧版本关闭后，把当时的关键状态快照放入对应版本目录。
- 根目录 `TASKS.md` 和 `HANDOFF.md` 必须重新整理成当前版本可读状态。
- `docs/archive/` 中的内容默认只供追溯，不要求下一位 Agent 每次读取。

## 成功标志

```text
TASKS.md 只包含当前版本任务，清理前必要历史已保存
已有 BACKLOG.md 存放未来候选事项
HANDOFF.md 只回答四个交接问题，Stage 与 WORKFLOW / TASKS 一致
需要归档时 docs/archive/<version>/ 保存旧版本快照
已有 CHANGELOG.md 记录版本收束结果，未为小项目额外造文件
下一位 Agent 能在 5 分钟内判断该做什么
```
