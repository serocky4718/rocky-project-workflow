# Platform Adapter Rules

本文件说明 `agents/openai.yaml` 的定位，以及未来多 AI 平台支持方式。

## 当前定位

`agents/openai.yaml` 只服务 OpenAI Codex / OpenAI 相关 UI 的 skill 展示和默认提示。

它不是通用 Agent 标准，也不代表其他平台一定会读取。

## 当前支持

```text
agents/openai.yaml    OpenAI Codex UI metadata
SKILL.md              通用入口和路由表
references/           平台无关规则文档
项目 AGENTS.md         Codex 自动读取的项目级权威规则
```

## 未来扩展

如果要支持其他平台，可以新增：

```text
agents/generic.md
agents/claude.md
agents/gemini.md
agents/custom.yaml
```

规则：

- 平台专属文件只放接口说明和默认入口提示。
- 核心流程仍然放在 `SKILL.md` 和 `references/`。
- 不在多个平台文件里重复完整规则。

## openai.yaml 语言

本 skill 是中文体系，`agents/openai.yaml` 的用户可见内容应使用中文。
