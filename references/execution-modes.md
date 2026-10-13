# Execution Modes

根据用户意图选择一种执行模式。默认不要把新手推向多窗口或多 Agent。

## Guided Solo（默认）

适合大多数 XS、S 和普通 M 项目。

- 在同一任务内按 PM -> Architect（如需要）-> Builder -> QA -> Reviewer（如需要）推进。
- 用阶段标题保持职责边界，但不要求用户每次确认角色切换。
- 发现需求冲突、外部账号、高风险操作或必须由用户决定的范围变化时才暂停。
- 每个阶段只生成该规模需要的交付物。

## Strict Handoff

仅在用户明确要求严格角色分离、手动跨窗口、审计式交接时使用。

- 每个窗口只承担一个角色。
- 完成后更新 `HANDOFF.md`，等待用户在新窗口进入下一角色。
- 不自动把 QA 切换成 Builder，也不让 Reviewer 直接修代码。

## Dispatcher

仅在用户明确要求 Dispatcher、多 Agent、子 Agent 或 Builder/QA/Reviewer 自动闭环时使用。

- Dispatcher 只协调 Builder、QA、Reviewer。
- 强制顺序：Builder -> QA -> Reviewer。
- 最多三轮；三轮后仍不通过则交还 PM。
- 不使用 `create_thread` 代替子 Agent，除非用户明确要求可见的独立任务窗口。

## 选择规则

```text
用户未指定 -> Guided Solo
用户明确说手动跨窗口 / 严格角色隔离 -> Strict Handoff
用户明确说 Dispatcher / 多 Agent / 子 Agent -> Dispatcher
```

推荐执行模式属于可调整建议。只有模式选择会显著增加外部操作、成本或用户工作量时，才需要用户确认。
