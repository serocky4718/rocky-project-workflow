# Report Templates 角色报告模板

本文件定义各职位报告的目录、文件名和最低结构。

目的：避免角色报告写到根目录、写成流水账，或和 `HANDOFF.md` 混在一起。

## 使用条件

项目内的统一报告要求放在 AGENTS 的 Reporting 小节：M/L、Dispatcher 或实际需要审计证据时写正式报告；XS/S 的普通 Guided Solo / Strict Handoff 阶段默认在 HANDOFF 中留下简短证据。严格交接本身不增加报告要求，不为满足模板创建空报告。

## 总规则

- 报告只放 `docs/reports/<type>/`。
- 文件名使用 `YYYY-MM-DD_<scope>.md`，例如 `2026-05-26_login-flow.md`。
- 报告记录过程、证据和结论；`HANDOFF.md` 只保留下一棒必须知道的信息。
- 一个报告只对应一个清楚范围，不把多个阶段混在一篇里。
- 如果报告过长，把细节留在报告里，把下一步摘要写进 `HANDOFF.md`。

## 目录对应关系

```text
docs/reports/architecture/      Architect
docs/reports/implementation/    Builder
docs/reports/qa/                QA
docs/reports/review/            Reviewer
docs/reports/design/            Designer
docs/reports/devops/            DevOps/GitHub
```

## 通用报告头

每篇报告开头必须包含：

```md
# <Role> Report: <scope>

- Date: <YYYY-MM-DD>
- Role: <PM / Architect / Dispatcher / Builder / QA / Reviewer / Designer / DevOps>
- Scope: <本次报告范围>
- Related Tasks: <TASKS.md 中的任务 ID，若无则写 none>
- Status: <done / blocked / failed / needs-review>
```

## Builder 实现报告

路径：`docs/reports/implementation/YYYY-MM-DD_<scope>.md`

```md
# Builder Report: <scope>

## Summary

## Changed Files

| File | Change | Why |
|---|---|---|

## Commands Run

| Command | Result | Notes |
|---|---|---|

## Verification

## Risks

## Not Done

## Handoff To QA

## Absolute Pitfalls
```

## QA 验证报告

路径：`docs/reports/qa/YYYY-MM-DD_<scope>.md`

```md
# QA Report: <scope>

## Test Scope

## Test Steps

| Step | Action | Expected | Actual | Result |
|---|---|---|---|---|

## Commands Run

| Command | Result | Notes |
|---|---|---|

## Pass / Fail

## Reproduction Path

## Issues For Builder

| Issue | Evidence | Suspected File | Severity |
|---|---|---|---|

## Absolute Pitfalls
```

QA 报告只记录验证和复现，不写代码修复过程。

## Architect 架构报告

路径：`docs/reports/architecture/YYYY-MM-DD_<scope>.md`

```md
# Architect Report: <scope>

## Architecture Goal

## Module Boundaries

## Directory Decisions

## Data Flow

## Builder Tasks

## Risks And Tradeoffs

## Absolute Pitfalls
```

## Reviewer 评审报告

路径：`docs/reports/review/YYYY-MM-DD_<scope>.md`

```md
# Reviewer Report: <scope>

## Findings

| Severity | File / Behavior | Issue | Impact | Owner |
|---|---|---|---|---|

## Required Fixes

## Suggested Improvements

## Test Gaps

## Residual Risk

## Absolute Pitfalls
```

## Designer 设计报告

路径：`docs/reports/design/YYYY-MM-DD_<scope>.md`

```md
# Designer Report: <scope>

## Design Goal

## Page / Flow Structure

## Interaction States

## Visual Rules

## Assets

| Asset | Candidate Path | Final Path | Status |
|---|---|---|---|

## Handoff To Builder

## Absolute Pitfalls
```

## DevOps/GitHub 报告

路径：`docs/reports/devops/YYYY-MM-DD_<scope>.md`

```md
# DevOps Report: <scope>

## Repository

## Visibility

## Remote

## Commit / Push Status

## Sensitive File Check

## Deployment Notes

## Absolute Pitfalls
```

## 成功标志

```text
报告在正确目录
文件名能看出日期和范围
报告包含证据、命令、结论
HANDOFF.md 只保留下一棒行动
QA 报告没有混入 Builder 修复过程
```
