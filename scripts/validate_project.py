#!/usr/bin/env python3
"""Read-only structure or readiness checks. Never proves product acceptance."""
from __future__ import annotations
import argparse
import re
from pathlib import Path
from project_rules import (MODES, SCALES, RULE_VERSION, files_for, load_state,
                           metadata_errors, rule_version_error, state_errors)


def section_body(content, heading):
    match = re.search(r"^##\s+" + re.escape(heading) + r"\s*$\n?(.*?)(?=^##\s|\Z)", content, re.M | re.S)
    return match.group(1).strip() if match else ""


def meaningful(content):
    text = re.sub(r"<!--.*?-->", "", content, flags=re.S)
    text = re.sub(r"\{\{.*?\}\}", "", text)
    return any(line.strip() and not line.lstrip().startswith("#") and
               line.strip().strip("- *`").lower() not in ("todo", "tbd", "待填写", "待补充")
               for line in text.splitlines())


def handoff_stage(content):
    body = section_body(content, "1. 当前项目处于什么阶段？")
    aliases = {"planning": "pm", "implementation": "builder", "testing": "qa"}
    match = re.match(r"(?:当前阶段\s*[:：]\s*|当前\s*)?[-*` ]*(scaffold|pm|planning|architect|designer|builder|implementation|qa|testing|reviewer|devops|closed|blocked)\b", body, re.I)
    if not match:
        return set()
    token = match.group(1).lower()
    return {aliases.get(token, token)}


def validate(target, scale=None, mode=None, level="structure", *, proposed_state=None, proposed_contents=None):
    errors, warnings = [], []
    proposed_contents = proposed_contents or {}
    try:
        state = proposed_state if proposed_state is not None else load_state(target)
        state_problems = state_errors(state)
        if state_problems:
            raise ValueError(" ".join(state_problems))
        if scale and scale != state["scale"]:
            errors.append("Requested scale differs from WORKFLOW.json.")
        if mode and mode != state["mode"]:
            errors.append("Requested mode differs from WORKFLOW.json.")
        version_error = rule_version_error(state["rule_version"])
        if version_error:
            errors.append(version_error)
        elif state["rule_version"] != RULE_VERSION:
            warnings.append("Compatible older rule version; existing documents are preserved. Review template changes when needed.")
        errors.extend(metadata_errors(target, state, proposed_contents))
        names = list(files_for(state["scale"])) + [f"docs/agent-prompts/{r}.md" for r in state["roles"]]
        contents = {}
        for name in names:
            path = target / name
            if not path.is_file():
                errors.append(f"Missing required file: {name}")
                continue
            contents[name] = proposed_contents.get(name)
            if contents[name] is None:
                contents[name] = path.read_text(encoding="utf-8-sig")
            if not contents[name].strip():
                errors.append(f"Empty required file: {name}")
            if "{{" in contents[name] or "}}" in contents[name]:
                errors.append(f"Unexpanded template token: {name}")
        if not re.search(r"^##\s+Safety\s*$", contents.get("AGENTS.md", ""), re.M):
            errors.append("AGENTS.md is missing the required Safety section.")
        agents = contents.get("AGENTS.md", "")
        for heading in ("Instruction Sources", "Startup", "Role Routing"):
            if not meaningful(section_body(agents, heading)):
                errors.append(f"AGENTS.md needs the workflow instructions section: {heading}")
        for role in state["roles"]:
            name = f"docs/agent-prompts/{role}.md"
            content = contents.get(name, "")
            if not content:
                continue
            if "project-create-rocky-0-1-0" in content or re.search(r"references[/\\]", content):
                errors.append(f"Legacy or non-project-local role prompt: {name}")
            versions = re.findall(r"^- Rule version:\s*`([^`]+)`\s*$", content, re.M)
            if len(versions) != 1 or rule_version_error(versions[0]):
                errors.append(f"Missing/incompatible role version: {name}")
        if state["roles"]:
            readme = contents.get("README.md", "")
            for role in state["roles"]:
                if f"docs/agent-prompts/{role}.md" not in section_body(agents, "Role Routing"):
                    errors.append(f"AGENTS.md has no routing entry for selected role: {role}")
                if f"docs/agent-prompts/{role}.md" not in readme:
                    errors.append(f"README has no entry for selected role: {role}")
        handoff = contents.get("HANDOFF.md", "")
        stages = handoff_stage(handoff)
        if stages and stages != {state["stage"]}:
            errors.append("HANDOFF.md describes a different stage from WORKFLOW.json; synchronize before continuing.")
        if not stages and not re.search(r"^- Stage:\s*`" + re.escape(state["stage"]) + r"`\s*$", handoff, re.M):
            if level == "ready":
                errors.append("HANDOFF.md needs an explicit Stage matching WORKFLOW.json.")
            else:
                warnings.append("Legacy HANDOFF has no recognizable stage; synchronize before readiness validation.")
        if level == "ready":
            if not state["prd_confirmed"] or not state["confirmation_note"].strip():
                errors.append("PRD confirmation and its source/note must be recorded; never infer consent.")
            if state["stage"] in ("scaffold", "pm", "blocked", "closed"):
                errors.append("Project stage is not ready for implementation; resolve planning/blockers first.")
            prd = contents.get("PRD.md", "")
            for heading in ("4. 项目目标", "5. MVP 范围", "9. 验收标准"):
                if not meaningful(section_body(prd, heading)):
                    errors.append(f"PRD section needs content: {heading}")
            tasks = contents.get("TASKS.md", "")
            rows = [line for line in tasks.splitlines() if re.match(r"\|\s*T-[A-Za-z0-9_-]+\s*\|", line)]
            if not any("完成并确认 PRD" not in row and "保存已确认需求" not in row and
                       len(row.split("|")) >= 9 and all(cell.strip() for cell in row.split("|")[1:8]) for row in rows):
                errors.append("TASKS.md needs an implementation task with owner, acceptance and dependencies.")
            for heading in ("1. 当前项目处于什么阶段？", "3. 下一步具体做什么？"):
                body = section_body(handoff, heading)
                if not meaningful(body) or re.search(r"scaffold|保存已确认需求|确认并细化|完成并确认", body):
                    errors.append(f"HANDOFF needs the actual next stage/action: {heading}")
            if state["scale"] in ("m", "l"):
                for heading in ("Current Scope", "Current Acceptance Criteria"):
                    if not meaningful(section_body(contents.get("PRD_CURRENT.md", ""), heading)):
                        errors.append(f"PRD_CURRENT needs content: {heading}")
            warnings.append("Readiness is mechanical; PM must review scope and acceptance quality. Product tests have not been run.")
        else:
            warnings.append("Structure only; empty section bodies may remain. Run --level ready after PM saves confirmed requirements.")
    except (OSError, ValueError) as exc:
        errors.append(str(exc))
    return errors, warnings


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", type=Path)
    parser.add_argument("--scale", choices=SCALES)
    parser.add_argument("--mode", choices=MODES)
    parser.add_argument("--level", choices=("structure", "ready"), default="structure")
    args = parser.parse_args()
    errors, warnings = validate(args.target.resolve(), args.scale, args.mode, args.level)
    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")
    print(f"{args.level} validation {'failed' if errors else 'passed'}; this is not product acceptance.")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
