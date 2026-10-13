# Validation 验证规则

修改项目后，要尽量用可重复的方式检查结果。

项目骨架检查使用 `validate_project.py --level structure`。PM 保存确认后的需求、实际任务和交接后，进入实现前运行 `--level ready`；该检查会核对阶段一致性和角色前提，但不能代替人工判断验收质量或产品测试。阶段更新按 `state-and-handoff.md` 同步，结构通过不代表已可开发。

## 修改本技能时

修改生成、状态或校验脚本后，除技能格式检查，还运行 `scripts/test_workflow.py --work-dir <临时工作目录>`。它检查确认内容未保存、旧阶段交接、调度越序和兼容版本保留用户内容等实际行为；只在指定临时目录生成隔离示例，不访问外部账号。不要只用生成脚本自身的规则计算预期结果，以免同一处错误同时通过生成和校验。

## 按技术栈选择验证命令

Architect 阶段必须在 `PROJECT_STRUCTURE.md` 的 `Validation Commands` 小节输出项目专属验证命令清单。

### Node / 前端

```powershell
npm install
npm run lint
npm test
npm run build
npm run dev
```

说明：

- `npm install`: 安装依赖。
- `npm run lint`: 检查代码风格和常见错误。
- `npm test`: 跑测试。
- `npm run build`: 检查项目能否正式构建。
- `npm run dev`: 启动本地开发服务器。

### Python

```powershell
python -m pytest
python -m ruff check .
python -m mypy .
python -m build
```

如果项目没有这些工具，只记录“未配置”，不要强行安装。

### Go

```powershell
go test ./...
go vet ./...
go build ./...
```

### 纯静态站

```powershell
# 如果没有构建工具，优先做人工检查：
# 打开 HTML
# 检查链接
# 检查控制台错误
```

### 其他技术栈

如果无法识别技术栈，先读取：

```text
README.md
package.json
pyproject.toml
go.mod
Cargo.toml
Makefile
```

再给出建议验证命令，不要凭空编造。

## 命令风险说明

运行命令前要判断风险：

- `npm install` 会修改 `node_modules`，有时也会修改 lockfile。
- `npm run build` 通常安全，但可能生成构建目录。
- `npm test` 通常安全，但测试可能写入临时文件。
- 删除、重置、清理类命令有数据丢失风险，不能随意运行。

## 没有验证命令时

如果项目还没有测试或构建命令，在交接里写：

```text
当前没有发现验证命令
已做的人工检查
建议补充的验证方式
```

## 成功标志

验证完成后说明：

- 哪些命令成功。
- 哪些命令失败。
- 失败原因是什么。
- 是否影响本次交付。
