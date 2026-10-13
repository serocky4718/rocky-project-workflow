#!/usr/bin/env python3
"""Fill missing role prompts only; existing prompts and README are never updated."""
from __future__ import annotations
import argparse
from datetime import date
from pathlib import Path
from project_rules import MODES, SCALES, RULE_VERSION, apply_missing, assert_compatible, reports_required


def role_plan(name, scale, mode, roles, *, rule_version=RULE_VERSION):
    source = Path(__file__).resolve().parents[1] / "references" / "roles"
    reporting = "formal" if reports_required(scale, mode) else "brief-handoff"
    header = ("# Project Context\n\n"
              f"- Project: `{name}`\n- Scale: `{scale.upper()}`\n- Execution mode: `{mode}`\n"
              f"- Rule version: `{rule_version}`\n- Generated: `{date.today().isoformat()}`\n\n"
              f"- Reporting default: `{reporting}`\n\n"
              "项目根目录 AGENTS.md 是权威规则；WORKFLOW.json 记录模式和阶段。\n\n"
              "## Mode Boundaries\n\n"
              "Guided Solo 可在已授权范围内连续切换阶段；Strict Handoff 完成后交给用户；"
              "Dispatcher 子 Agent 交付后返回调度者，由调度者安排下一角色。"
              "Dispatcher 的总阶段、任务状态和 HANDOFF 由调度者更新，子 Agent 不提前改写总交接。"
              "用户明确要求只分析或只测试时，保持该范围。\n\n")
    if rule_version != RULE_VERSION:
        header += ("## Reporting Compatibility\n\n"
                   "报告以项目 AGENTS 的 Reporting 为准；旧项目缺少该小节时，"
                   "使用上述 Reporting default。brief-handoff 在交接中保留简短证据；"
                   "formal 写实际报告，记录日期、角色、范围、任务、状态、验证证据和风险。"
                   "用户另有审计要求时按实际要求处理。\n\n")
    return {f"docs/agent-prompts/{role}.md": header + (source / f"{role}.md").read_text(encoding="utf-8") for role in roles}


def sync_roles(target, project_name, scale, mode, apply=False):
    state = assert_compatible(target, project_name, scale, mode)
    if state is None:
        raise ValueError("Initialize or adopt the project before filling role prompts.")
    return apply_missing(target, role_plan(project_name, scale, mode, tuple(state["roles"]),
                                         rule_version=state["rule_version"]), apply)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", type=Path)
    parser.add_argument("--project-name", required=True)
    parser.add_argument("--scale", choices=SCALES, required=True)
    parser.add_argument("--mode", choices=MODES, required=True)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    try:
        for action in sync_roles(args.target.resolve(), args.project_name, args.scale, args.mode, args.apply):
            print(action)
        print("Missing prompts only; no existing prompts or README were updated.")
        if not args.apply:
            print("Preview only. Add --apply to write missing prompts.")
        return 0
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
