# Project Structure Rules

目录必须反映真实项目，不为模板完整度创建空目录。

## 所有项目

```text
README.md
AGENTS.md
WORKFLOW.json
PRD.md
TASKS.md
HANDOFF.md
```

其余根目录文件按规模规则创建。

## 技术栈文件

只创建或记录真实技术栈需要的文件：

```text
Node / 前端    package.json、src/、app/、pages/、public/
Python         pyproject.toml、src/ 或包目录、tests/
Go             go.mod、cmd/、internal/
Rust           Cargo.toml、src/
静态站         HTML/CSS/JS 和资源目录
```

不要把 `package.json` 当作所有项目的必备文件。

## 文档

```text
docs/prd/             M/L 版本化需求
docs/archive/         L 或版本收束快照
docs/agent-prompts/   Strict Handoff / Dispatcher
docs/reports/         按 AGENTS 的 Reporting 和实际内容创建
docs/design/          有设计交付时
docs/assets/          有资源说明时
```

## 临时与正式资源

- 候选和临时文件放项目约定的 `output/`、`tmp/` 或工作目录。
- 只有用户确认的正式资源进入 `public/assets/` 等运行目录。
- 私密数据不进入 `public/`，真实凭据不提交 Git。

## 文档卫生

- `TASKS.md` 只保存当前版本任务。
- `BACKLOG.md` 保存未来候选。
- `HANDOFF.md` 保存最短交接。
- `PROJECT_STRUCTURE.md` 必须记录项目实际验证命令，而不是通用命令清单。
