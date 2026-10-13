# README Role Entry

README 是使用者的导航页。只在 Strict Handoff 或 Dispatcher 模式加入角色提示词链接；Guided Solo 不需要用户反复新开窗口。

## README 与 AGENTS 的分工

- README：说明如何打开项目、选择角色和查看文档，提供角色提示词链接。
- AGENTS：维护统一开工顺序、规则来源、角色路由、权限、验证及交接规则。
- 角色提示词：维护各职务自己的输入、职责、限制和交付物。

不要把“Agent 必须先读取哪些文件”或“完成后如何切换角色”写成 README 中的统一执行规则。生成脚本把这些要求写入 AGENTS；README 通过链接引导使用者。

## 生成与补齐

新项目使用 `scripts/init_project.py`，会同时生成 AGENTS 规则入口、README 导航和当前模式需要的角色提示词。

已有项目的补齐脚本仅创建缺失的提示词，不更新已有正文和入口。参数必须与 `WORKFLOW.json` 一致；已知兼容版本无需只为补齐而整体迁移，新文件保留项目版本标记。例如补齐一个 S 规模的严格交接项目：

```powershell
python "<skill>/scripts/sync_role_prompts.py" "<project>" --project-name "<name>" --scale s --mode strict-handoff
```

先查看预览清单，确认后加 `--apply` 创建缺失文件。成功标志：缺失提示词已创建，原有文件未被覆盖。模板升级或入口缺失时，先用 `inspect_project.py --diff` 预览，再合并所需差异；不要把补齐脚本当成更新脚本。

项目提示词从 `references/roles/` 复制并附上项目上下文。项目副本不得要求其他窗口访问技能安装目录；项目专属验证命令维护在 AGENTS 或现有 `PROJECT_STRUCTURE.md` 中，角色按需读取。

## README 小节模板

只列实际已生成的角色，不直接粘贴八个角色全表：

```md
## Agent Role Entry

在 Codex 中打开本项目目录，告诉助手要进入的角色。
以下链接用于查看各角色职责；AI 的开工和交接规则见 [AGENTS.md](AGENTS.md)。

- Builder：[角色提示词](docs/agent-prompts/builder.md)
- QA：[角色提示词](docs/agent-prompts/qa.md)
```

## 给使用者的启动语

Strict Handoff 的 Builder 示例：

```text
进入本项目的 Builder 角色，完成当前交接中的实现任务。
```

Dispatcher 示例（只用于已经选择该模式的项目）：

```text
启动本项目的 Dispatcher，按项目规则调度 Builder、QA、Reviewer 完成当前任务。
```

成功标志：助手遵守项目 AGENTS，根据当前模式读取所选提示词；README 提供使用入口，没有另建一套执行规则。
