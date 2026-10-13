#!/usr/bin/env python3
"""Preview or create missing documentation. Does not confirm PRD or migrate."""
from __future__ import annotations
import argparse
import json
from datetime import date
from pathlib import Path
from project_rules import (MODES, SCALES, OPTIONAL_ROLES, STATE_FILE, RULE_VERSION, apply_missing,
                           assert_compatible, files_for, new_state, roles_for)
from sync_role_prompts import role_plan


def role_entry(roles):
    if not roles:
        return ""
    return ("## Agent Role Entry\n\n"
            "在 Codex 中打开本项目目录，告诉助手要进入的角色。"
            "以下链接用于查看各角色职责；AI 的开工和交接规则见 [AGENTS.md](AGENTS.md)。\n\n") + "\n".join(
        f"- {role}: [角色提示词](docs/agent-prompts/{role}.md)" for role in roles)


def role_rules(roles):
    if not roles:
        return ("当前为 Guided Solo，不要求生成或读取八份项目内职位文件。"
                "按当前任务依次执行所需阶段并标注角色，用户要求只分析或只测试时保持该范围。")
    return ("按 WORKFLOW.json 的角色选择和当前任务读取对应文件，不通过 README 推定角色或授权。\n\n" +
            "\n".join(f"- {role}: [职责提示词](docs/agent-prompts/{role}.md)" for role in roles))


def build_plan(name, scale, mode, roles, *, rule_version=RULE_VERSION):
    templates = Path(__file__).resolve().parents[1] / "assets" / "templates"
    values = {"{{PROJECT_NAME}}": name, "{{SCALE}}": scale.upper(), "{{MODE}}": mode,
              "{{DATE}}": date.today().isoformat(), "{{ROLE_ENTRY}}": role_entry(roles),
              "{{ROLE_RULES}}": role_rules(roles)}
    plan = {}
    for filename in files_for(scale):
        content = (templates / f"{filename}.tmpl").read_text(encoding="utf-8")
        for key, value in values.items():
            content = content.replace(key, value)
        plan[filename] = content.rstrip() + "\n"
    plan.update(role_plan(name, scale, mode, roles, rule_version=rule_version))
    # Written last: an I/O failure cannot claim a completed initialization.
    plan[STATE_FILE] = json.dumps(new_state(name, scale, mode, roles), ensure_ascii=False, indent=2) + "\n"
    return plan


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", type=Path)
    parser.add_argument("--project-name", required=True)
    parser.add_argument("--scale", choices=SCALES, required=True)
    parser.add_argument("--mode", choices=MODES, default="guided-solo")
    parser.add_argument("--roles", nargs="*", choices=OPTIONAL_ROLES, default=None,
                        help="Additional strict-handoff roles; preserve existing selection on rerun")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    try:
        if not args.project_name.strip() or any(c in args.project_name for c in "\r\n"):
            raise ValueError("Project name must be a nonempty single line.")
        target = args.target.resolve()
        state = assert_compatible(target, args.project_name, args.scale, args.mode)
        roles = tuple(state["roles"]) if state and args.roles is None else roles_for(args.scale, args.mode, tuple(args.roles or ()))
        assert_compatible(target, args.project_name, args.scale, args.mode, roles)
        plan = build_plan(args.project_name, args.scale, args.mode, roles,
                          rule_version=state["rule_version"] if state else RULE_VERSION)
        for action in apply_missing(target, plan, args.apply):
            print(action)
        print("Skeleton only. PM must save confirmed requirements and update WORKFLOW.json before readiness validation.")
        if not args.apply:
            print("Preview only; no files written. Add --apply to create missing files.")
        return 0
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}")
        print("Stopped. On I/O failure inspect partial files before retrying; existing files are never overwritten.")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
