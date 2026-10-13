#!/usr/bin/env python3
"""Preview or synchronize workflow stage, tasks metadata and a short handoff."""
from __future__ import annotations

import argparse
import copy
import json
import os
import re
import tempfile
from pathlib import Path

from project_rules import ACTIVE_STAGES, STAGES, rule_version_error, state_errors
from validate_project import validate

STAGE_LABELS = {
    "scaffold": "项目骨架", "pm": "需求梳理", "architect": "架构设计",
    "designer": "界面和资源设计", "builder": "代码实现", "qa": "测试验证",
    "reviewer": "评审", "devops": "已授权的仓库或发布工作",
    "closed": "本阶段已结束", "blocked": "存在阻塞",
}


def replace_section(content, heading, body):
    pattern = re.compile(r"(^##\s+" + re.escape(heading) + r"\s*\n)(.*?)(?=^##\s|\Z)", re.M | re.S)
    if len(list(pattern.finditer(content))) != 1:
        raise ValueError(f"Expected exactly one HANDOFF section: {heading}")
    return pattern.sub(lambda match: match.group(1) + "\n" + body.strip() + "\n\n", content)


def set_stage(content, stage):
    pattern = re.compile(r"^- Stage:.*$", re.M)
    matches = list(pattern.finditer(content))
    if len(matches) > 1:
        raise ValueError("Multiple Stage fields; inspect before synchronizing.")
    line = f"- Stage: `{stage}`"
    if matches:
        return pattern.sub(lambda _: line, content, count=1)
    # Remove only the known initializer's legacy planning marker.
    content = re.sub(r"^- Status: `planning`\n", "", content, count=1, flags=re.M)
    title = re.search(r"^# [^\n]+\n", content, re.M)
    if not title:
        raise ValueError("Document needs its existing top-level title.")
    return content[:title.end()] + "\n" + line + "\n" + content[title.end():]


def build_update(target, stage, summary, next_step, *, confirm_prd=False,
                 confirmation_note=None, reopen_prd=False, pitfalls=None):
    if stage not in STAGES:
        raise ValueError("Unknown workflow stage.")
    before, text = {}, {}
    for name in ("HANDOFF.md", "TASKS.md", "WORKFLOW.json"):
        path = target / name
        if path.is_symlink() or path.resolve().parent != target.resolve() or not path.is_file():
            raise ValueError(f"Expected a regular project file: {name}")
        before[name] = path.read_bytes()
        text[name] = before[name].decode("utf-8-sig").replace("\r\n", "\n")
    state = json.loads(text["WORKFLOW.json"])
    problems = state_errors(state)
    if problems:
        raise ValueError(" ".join(problems))
    version_error = rule_version_error(state["rule_version"])
    if version_error:
        raise ValueError(version_error)
    if not summary.strip() or not next_step.strip():
        raise ValueError("Summary and next step must describe the actual work.")
    if confirm_prd and reopen_prd:
        raise ValueError("Cannot confirm and reopen PRD in the same operation.")
    if confirm_prd and (not confirmation_note or not confirmation_note.strip()):
        raise ValueError("Record the actual user confirmation source; never infer consent.")
    if confirmation_note is not None and not confirm_prd:
        raise ValueError("Use --confirm-prd with --confirmation-note to record a confirmed decision.")
    if reopen_prd and stage not in ("pm", "scaffold", "blocked"):
        raise ValueError("Reopened requirements must return to planning or a blocked stage.")
    proposed = copy.deepcopy(state)
    proposed["stage"] = stage
    if confirm_prd:
        proposed["prd_confirmed"] = True
        proposed["confirmation_note"] = confirmation_note.strip()
    if reopen_prd:
        proposed["prd_confirmed"] = False
        proposed["confirmation_note"] = ""
        proposed["dispatcher"] = None
    handoff = set_stage(text["HANDOFF.md"], stage)
    handoff = replace_section(handoff, "1. 当前项目处于什么阶段？", f"{stage}（{STAGE_LABELS[stage]}）")
    handoff = replace_section(handoff, "2. 上一阶段完成了什么判断？", summary)
    handoff = replace_section(handoff, "3. 下一步具体做什么？", next_step)
    if pitfalls is not None:
        if not pitfalls.strip():
            raise ValueError("Pitfalls must be nonempty when explicitly replaced.")
        handoff = replace_section(handoff, "4. 有哪些绝对不能踩的坑？", pitfalls)
    plan = {"HANDOFF.md": handoff.rstrip() + "\n",
            "TASKS.md": set_stage(text["TASKS.md"], stage),
            "WORKFLOW.json": json.dumps(proposed, ensure_ascii=False, indent=2) + "\n"}
    level = "ready" if stage in ACTIVE_STAGES else "structure"
    errors, warnings = validate(target, level=level, proposed_state=proposed, proposed_contents=plan)
    if errors:
        raise ValueError("Proposed handoff is not valid: " + " ".join(errors))
    return plan, before, warnings


def apply_update(target, plan, before):
    for name, original in before.items():
        if (target / name).read_bytes() != original:
            raise ValueError(f"File changed during preparation; stopped without writes: {name}")
    # State is written last. A partial failure remains detectable by validation.
    for name, content in plan.items():
        path = target / name
        if path.read_bytes() != before[name]:
            raise ValueError(f"Concurrent edit detected; inspect partial changes: {name}")
        original = before[name]
        if b"\r\n" in original:
            content = content.replace("\n", "\r\n")
        data = content.encode("utf-8-sig" if original.startswith(b"\xef\xbb\xbf") else "utf-8")
        fd, temporary = tempfile.mkstemp(prefix=".workflow-", suffix=".tmp", dir=target)
        try:
            with os.fdopen(fd, "wb") as stream:
                stream.write(data)
            os.replace(temporary, path)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", type=Path)
    parser.add_argument("--stage", choices=STAGES, required=True)
    parser.add_argument("--summary", required=True)
    parser.add_argument("--next-step", required=True)
    parser.add_argument("--pitfalls")
    parser.add_argument("--confirm-prd", action="store_true")
    parser.add_argument("--confirmation-note")
    parser.add_argument("--reopen-prd", action="store_true")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    try:
        target = args.target.resolve()
        plan, before, warnings = build_update(target, args.stage, args.summary, args.next_step,
            confirm_prd=args.confirm_prd, confirmation_note=args.confirmation_note,
            reopen_prd=args.reopen_prd, pitfalls=args.pitfalls)
        for warning in warnings:
            print(f"WARNING: {warning}")
        for name in plan:
            print(f"UPDATE: {name}")
        if args.apply:
            apply_update(target, plan, before)
            level = "ready" if args.stage in ACTIVE_STAGES else "structure"
            errors, _ = validate(target, level=level)
            if errors:
                raise ValueError("Post-write validation failed; inspect the current files: " + " ".join(errors))
            print("Workflow stage and handoff synchronized; unrelated document content was preserved.")
        else:
            print("Preview only; no files written. Add --apply for the authorized update.")
        return 0
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}")
        print("On a write failure inspect any partial changes before retrying; do not overwrite concurrent user edits.")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
