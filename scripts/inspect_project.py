#!/usr/bin/env python3
"""Read-only project status and migration preview. Never applies changes."""
from __future__ import annotations
import argparse
import difflib
import json
from pathlib import Path
from project_rules import MODES, SCALES, OPTIONAL_ROLES, STATE_FILE, load_state, roles_for, state_errors
from init_project import build_plan
from validate_project import validate


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", type=Path)
    parser.add_argument("--project-name")
    parser.add_argument("--scale", choices=SCALES)
    parser.add_argument("--mode", choices=MODES)
    parser.add_argument("--roles", nargs="*", choices=OPTIONAL_ROLES, default=None)
    parser.add_argument("--diff", action="store_true", help="Show template differences; may include private project text")
    args = parser.parse_args()
    target = args.target.resolve()
    try:
        if not target.is_dir():
            raise ValueError("Target must be an existing project directory.")
        state = None
        if (target / STATE_FILE).exists():
            state = load_state(target)
            print(json.dumps(state, ensure_ascii=False, indent=2))
            errors, warnings = validate(target)
            for error in errors:
                print(f"CONFLICT: {error}")
            for warning in warnings:
                print(f"NOTE: {warning}")
        else:
            print("Existing/legacy project: no WORKFLOW.json. Read AGENTS/README/PRD/TASKS/HANDOFF before adoption.")
        name = args.project_name or (state or {}).get("project_name")
        scale = args.scale or (state or {}).get("scale")
        mode = args.mode or (state or {}).get("mode")
        if not all((name, scale, mode)):
            print("Preview requires --project-name, --scale and --mode when no state exists. No files written.")
            return 1
        if args.roles is None and state and mode == state["mode"]:
            extras = tuple(r for r in state["roles"] if r in OPTIONAL_ROLES) if mode == "strict-handoff" else ()
        else:
            extras = tuple(args.roles or ())
        roles = roles_for(scale, mode, extras)
        plan = build_plan(name, scale, mode, roles)
        if state:
            proposed = json.loads(plan[STATE_FILE])
            for key in ("stage", "prd_confirmed", "confirmation_note"):
                proposed[key] = state[key]
            proposed["dispatcher"] = state.get("dispatcher") if mode == state["mode"] else None
            errors = state_errors(proposed)
            if errors:
                raise ValueError(" ".join(errors))
            plan[STATE_FILE] = json.dumps(proposed, ensure_ascii=False, indent=2) + "\n"
        for filename, proposed in plan.items():
            path = target / filename
            if not path.exists():
                print(f"PROPOSE ADD: {filename}")
                if args.diff:
                    print("".join(difflib.unified_diff([], proposed.splitlines(True), fromfile="/dev/null", tofile=filename)))
            elif not path.is_file():
                print(f"CONFLICT path type: {filename}")
            else:
                old = path.read_text(encoding="utf-8-sig")
                if old == proposed:
                    print(f"KEEP: {filename}")
                elif filename == STATE_FILE or filename.startswith("docs/agent-prompts/") or filename in ("README.md", "AGENTS.md"):
                    print(f"REVIEW/MERGE (never replace user prose wholesale): {filename}")
                    if args.diff:
                        print("".join(difflib.unified_diff(old.splitlines(True), proposed.splitlines(True), fromfile=filename, tofile=filename+" (template proposal)")))
                else:
                    print(f"KEEP user document: {filename}")
        prompts = target / "docs" / "agent-prompts"
        if prompts.is_dir():
            for path in prompts.glob("*.md"):
                if path.stem not in roles:
                    print(f"REVIEW inactive role (preserve until migration): {path.name}")
        print("Read-only preview. Diffs are template proposals, not safe automatic replacements. Merge selected changes, preserve user content, then validate.")
        return 0
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
