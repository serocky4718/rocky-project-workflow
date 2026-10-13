"""Shared structure, state and preflight rules. Standard library only."""
from __future__ import annotations
import json
import re
from pathlib import Path

RULE_VERSION = "0.3.2"
COMPATIBLE_RULE_VERSIONS = ("0.3.0", "0.3.1", RULE_VERSION)
STATE_FILE = "WORKFLOW.json"
SCALES = ("xs", "s", "m", "l")
MODES = ("guided-solo", "strict-handoff", "dispatcher")
STAGES = ("scaffold", "pm", "architect", "designer", "builder", "qa", "reviewer", "devops", "closed", "blocked")
BASE_FILES = ("README.md", "AGENTS.md", "PRD.md", "TASKS.md", "HANDOFF.md")
MEDIUM_FILES = ("PRD_CURRENT.md", "PROJECT_STRUCTURE.md", "ARCHITECTURE.md", "CHANGELOG.md")
OPTIONAL_ROLES = ("architect", "reviewer", "designer", "devops-github")
ACTIVE_STAGES = ("architect", "designer", "builder", "qa", "reviewer", "devops")


def rule_version_error(version):
    if version not in COMPATIBLE_RULE_VERSIONS:
        return "Unsupported rule version; inspect before migrating."
    return None


def files_for(scale):
    return BASE_FILES + (() if scale == "xs" else ("BACKLOG.md",)) + (MEDIUM_FILES if scale in ("m", "l") else ())


def reports_required(scale, mode):
    return scale in ("m", "l") or mode == "dispatcher"


def roles_for(scale, mode, extra=()):
    if extra and mode != "strict-handoff":
        raise ValueError("Extra roles are supported only in strict-handoff mode.")
    if any(role not in OPTIONAL_ROLES for role in extra):
        raise ValueError("Unknown optional role.")
    if mode == "guided-solo":
        return ()
    if mode == "dispatcher":
        return ("dispatcher", "builder", "qa", "reviewer")
    base = ("pm", "architect", "builder", "qa", "reviewer") if scale in ("m", "l") else ("pm", "builder", "qa")
    return tuple(dict.fromkeys((*base, *extra)))


def new_state(name, scale, mode, roles):
    return {"schema_version": 1, "rule_version": RULE_VERSION, "project_name": name,
            "scale": scale, "mode": mode, "roles": list(roles), "stage": "scaffold",
            "prd_confirmed": False, "confirmation_note": "", "dispatcher": None}


def state_errors(state):
    if not isinstance(state, dict):
        return ["WORKFLOW.json must contain an object."]
    errors = []
    if type(state.get("schema_version")) is not int or state.get("schema_version") != 1:
        errors.append("Unsupported schema_version; inspect before migrating.")
    for key, choices in (("scale", SCALES), ("mode", MODES), ("stage", STAGES)):
        if state.get(key) not in choices:
            errors.append(f"Invalid state {key}.")
    for key in ("project_name", "rule_version"):
        if not isinstance(state.get(key), str) or not state[key].strip():
            errors.append(f"Missing {key}.")
    if type(state.get("prd_confirmed")) is not bool:
        errors.append("prd_confirmed must be a boolean.")
    if not isinstance(state.get("confirmation_note"), str):
        errors.append("confirmation_note must be a string.")
    if state.get("stage") in ACTIVE_STAGES and (state.get("prd_confirmed") is not True or
            not isinstance(state.get("confirmation_note"), str) or not state["confirmation_note"].strip()):
        errors.append("Active stages require recorded PRD confirmation and its source.")
    roles = state.get("roles")
    if not isinstance(roles, list) or not all(isinstance(r, str) for r in roles):
        errors.append("roles must be a list of role names.")
    elif state.get("scale") in SCALES and state.get("mode") in MODES:
        required = set(roles_for(state["scale"], state["mode"]))
        allowed = required | (set(OPTIONAL_ROLES) if state["mode"] == "strict-handoff" else set())
        if len(roles) != len(set(roles)) or not required.issubset(roles) or not set(roles).issubset(allowed):
            errors.append("roles do not match scale/mode or contain duplicates.")
    dispatch = state.get("dispatcher")
    if dispatch is not None:
        if state.get("mode") != "dispatcher" or not isinstance(dispatch, dict):
            errors.append("dispatcher state requires dispatcher mode and an object.")
        else:
            if type(dispatch.get("round")) is not int or not 1 <= dispatch["round"] <= 3:
                errors.append("dispatcher.round must be 1..3.")
            if not isinstance(dispatch.get("revision"), str) or not dispatch["revision"].strip():
                errors.append("dispatcher.revision must identify the working state.")
            for role in ("builder", "qa", "reviewer"):
                item = dispatch.get(role)
                if not isinstance(item, dict):
                    errors.append(f"Missing dispatcher.{role} state.")
                    continue
                if item.get("status") not in ("not-started", "running", "passed", "failed", "blocked"):
                    errors.append(f"Invalid dispatcher.{role}.status.")
                if item.get("agent_id") is not None and not isinstance(item.get("agent_id"), str):
                    errors.append(f"Invalid dispatcher.{role}.agent_id.")
                if item.get("status") == "passed" and item.get("revision") != dispatch.get("revision"):
                    errors.append(f"Stale dispatcher.{role} result: revision changed.")
            qa, review = dispatch.get("qa", {}), dispatch.get("reviewer", {})
            builder = dispatch.get("builder", {})
            if isinstance(builder, dict) and isinstance(qa, dict) and qa.get("status") in ("running", "passed") and builder.get("status") != "passed":
                errors.append("QA cannot run/pass before current Builder completes.")
            if isinstance(qa, dict) and isinstance(review, dict) and review.get("status") in ("running", "passed") and qa.get("status") != "passed":
                errors.append("Reviewer cannot run/pass before current QA passes.")
    if state.get("mode") == "dispatcher" and state.get("stage") in ("qa", "reviewer"):
        required = ("builder",) if state["stage"] == "qa" else ("builder", "qa")
        for role in required:
            item = dispatch.get(role) if isinstance(dispatch, dict) else None
            if not isinstance(item, dict) or item.get("status") != "passed":
                errors.append(f"Stage {state['stage']} requires completed dispatcher.{role} evidence.")
    return errors


def load_state(target):
    path = target / STATE_FILE
    if not path.is_file():
        raise ValueError("Missing WORKFLOW.json. Use inspect_project.py before adopting/migrating.")
    state = json.loads(path.read_text(encoding="utf-8-sig"))
    errors = state_errors(state)
    if errors:
        raise ValueError(" ".join(errors))
    return state


def metadata_errors(target, state, content_overrides=None):
    errors = []
    content_overrides = content_overrides or {}
    specs = [("AGENTS.md", "Project scale", "Execution mode"),
             ("README.md", "Scale", "Working mode"), ("PRD_CURRENT.md", "Scale", "Mode"),
             ("TASKS.md", "Scale", None)]
    prompts = target / "docs" / "agent-prompts"
    if prompts.is_dir():
        specs.extend((str(p.relative_to(target)), "Scale", "Execution mode") for p in prompts.glob("*.md"))
    for filename, scale_label, mode_label in specs:
        path = target / filename
        if not path.is_file():
            continue
        content = content_overrides.get(filename)
        if content is None:
            content = path.read_text(encoding="utf-8-sig")
        for label, expected in ((scale_label, state["scale"]), (mode_label, state["mode"])):
            if label is None:
                continue
            values = re.findall(r"^\s*-\s*" + re.escape(label) + r":\s*`?([^`\r\n]+)`?\s*$", content, re.M)
            if any(v.strip().lower() != expected for v in values):
                errors.append(f"Conflicting {label} in {filename}; inspect/migrate before writing.")
    for filename in ("TASKS.md", "HANDOFF.md"):
        path = target / filename
        if not path.is_file():
            continue
        content = content_overrides.get(filename)
        if content is None:
            content = path.read_text(encoding="utf-8-sig")
        stages = re.findall(r"^\s*-\s*Stage:\s*`?([^`\r\n]+)`?\s*$", content, re.M)
        if len(stages) > 1 or any(stage.strip() != state["stage"] for stage in stages):
            errors.append(f"Conflicting Stage in {filename}; synchronize the handoff before continuing.")
    return errors


def assert_compatible(target, name, scale, mode, roles=None):
    if target.exists() and not target.is_dir():
        raise ValueError("Target is not a directory.")
    if (target / STATE_FILE).exists():
        state = load_state(target)
        version_error = rule_version_error(state["rule_version"])
        if version_error:
            raise ValueError(version_error)
        for key, value in {"project_name": name, "scale": scale, "mode": mode}.items():
            if state.get(key) != value:
                raise ValueError(f"Existing {key} differs. Use inspect_project.py; initializer never migrates.")
        if roles is not None and set(state["roles"]) != set(roles):
            raise ValueError("Role selection differs; inspect/migrate before writing.")
        conflicts = metadata_errors(target, state)
        if conflicts:
            raise ValueError(" ".join(conflicts))
        return state
    if any((target / n).exists() for n in (*BASE_FILES, "AI_RULES.md", "docs/agent-prompts")):
        raise ValueError("Existing project has no workflow state. Use inspect_project.py; no files written.")
    return None


def apply_missing(target, plan, apply):
    # Preflight every output before writing any file. Exclusive creation prevents overwrites.
    for relative in plan:
        path = target / relative
        if path.exists() and not path.is_file():
            raise ValueError(f"Expected a file, found another path type: {path}")
        current = path
        while current != target:
            if current.is_symlink():
                raise ValueError(f"Refusing symlink output: {current}")
            if current != path and current.exists() and not current.is_dir():
                raise ValueError(f"Parent is not a directory: {current}")
            current = current.parent
    actions = []
    for relative, content in plan.items():
        path = target / relative
        if path.is_file():
            actions.append(f"KEEP existing: {relative}")
            continue
        actions.append(f"CREATE: {relative}")
        if apply:
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("x", encoding="utf-8", newline="\n") as stream:
                stream.write(content)
    return actions
