# GitHub Automation Rules

GitHub 是可选的外部写操作，不是 PRD 确认后的默认步骤。

## 授权顺序

先问：

```text
是否要把这个项目同步到 GitHub？
```

只有用户明确同意后，再问：

```text
仓库要使用 public 还是 private？
```

没有得到第一项授权时，不访问 GitHub 账号、不创建仓库、不配置 GitHub remote、不 push。部署授权与 GitHub 授权分开处理。

本地 commit 只在电脑上保存代码版本，按 `safety-rules.md` 的本地操作规则处理。它不依赖 GitHub 同步授权，不代表代码已上传；PM 自身仍不执行 Git 写入。

## 工具顺序

1. 优先使用已安装且已授权的 GitHub 连接器。
2. 没有连接器时，先用只读方式检查 `gh auth status`，再决定是否使用 GitHub CLI。
3. 两者都不可用时，给出手动步骤并记录阻塞，不假装完成。

## 可自动推导的内容

用户授权后，可从 PRD、README 和项目目录推导：

- 仓库名和描述。
- `.gitignore` 类型。
- remote 名称。
- 初始化提交说明。

仓库名冲突时使用安全后缀并记录实际名称。不要切换未知账号或组织。

## 执行前检查

- 解释 public/private、commit、remote、push 的含义和风险。
- 检查 `git status`、现有 remote、`.gitignore`。
- 搜索 `.env`、API Key、token、密码、session、证书和用户数据。
- 说明将提交的文件范围。
- 不覆盖不明 remote，不丢弃用户改动。

## 成功标志

```text
GitHub 同步授权已记录
public/private 已确认
敏感文件检查已完成
仓库地址、remote、commit hash、push 状态明确
HANDOFF.md 已记录外部状态
```
