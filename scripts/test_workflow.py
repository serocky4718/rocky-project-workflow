#!/usr/bin/env python3
"""Local regression checks. Writes isolated fixtures only inside --work-dir."""
from __future__ import annotations

import argparse
import json
import tempfile
import unittest
from pathlib import Path

from init_project import build_plan
from project_rules import apply_missing, new_state, state_errors
from update_workflow import apply_update, build_update
from validate_project import validate

WORK_DIR = None


class WorkflowRegression(unittest.TestCase):
    def setUp(self):
        self.target = Path(tempfile.mkdtemp(prefix="rocky-regression-", dir=WORK_DIR))
        if not self.target.resolve().is_relative_to(WORK_DIR):
            raise ValueError("Fixture escaped the specified work directory.")
        apply_missing(self.target, build_plan("待办", "xs", "guided-solo", ()), True)

    def save_requirements(self):
        path = self.target / "PRD.md"
        content = path.read_text(encoding="utf-8")
        for heading, body in (("4. 项目目标", "帮助用户记录待办。"), ("5. MVP 范围", "新增、展示和完成待办。"),
                              ("9. 验收标准", "新增待办可见，完成状态可切换。")):
            content = content.replace("## " + heading + "\n", "## " + heading + "\n\n" + body + "\n")
        path.write_text(content, encoding="utf-8")
        with (self.target / "TASKS.md").open("a", encoding="utf-8") as stream:
            stream.write("\n| T-002 | todo | P0 | Builder | 实现待办 | 新增和完成正常 | - |\n")

    def confirm(self):
        self.save_requirements()
        plan, before, _ = build_update(self.target, "builder", "确认需求已保存", "实现 T-002",
                                      confirm_prd=True, confirmation_note="用户在对话中确认待办 MVP")
        apply_update(self.target, plan, before)

    def test_confirmation_requires_saved_content_and_source(self):
        with self.assertRaises(ValueError):
            build_update(self.target, "builder", "准备实现", "实现待办")
        with self.assertRaises(ValueError):
            build_update(self.target, "builder", "准备实现", "实现待办", confirm_prd=True)
        with self.assertRaises(ValueError):
            build_update(self.target, "builder", "准备实现", "实现待办", confirm_prd=True, confirmation_note="用户确认")
        self.confirm()
        self.assertFalse(validate(self.target, level="ready")[0])

    def test_old_planning_handoff_cannot_pass_as_implementation(self):
        self.confirm()
        path = self.target / "HANDOFF.md"
        path.write_text(path.read_text(encoding="utf-8").replace("builder（代码实现）", "PM / planning"), encoding="utf-8")
        self.assertTrue(validate(self.target, level="ready")[0])

    def test_dispatcher_requires_current_predecessor_results(self):
        state = new_state("调度", "s", "dispatcher", ("dispatcher", "builder", "qa", "reviewer"))
        state.update(stage="builder", prd_confirmed=True, confirmation_note="用户确认")
        state["dispatcher"] = {"round": 1, "revision": "r1", **{
            role: {"status": "not-started", "agent_id": None} for role in ("builder", "qa", "reviewer")}}
        state["dispatcher"]["qa"]["status"] = "running"
        self.assertTrue(state_errors(state))
        state["dispatcher"]["builder"].update(status="passed", revision="r1")
        self.assertFalse(state_errors(state))
        state["dispatcher"]["reviewer"]["status"] = "running"
        self.assertTrue(state_errors(state))
        state["dispatcher"]["qa"].update(status="passed", revision="r1")
        self.assertFalse(state_errors(state))
        state["dispatcher"]["revision"] = "r2"
        self.assertTrue(state_errors(state))

    def test_compatible_patch_keeps_user_documents_and_consent(self):
        path = self.target / "WORKFLOW.json"
        state = json.loads(path.read_text(encoding="utf-8"))
        state["rule_version"] = "0.3.1"
        path.write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")
        self.confirm()
        with (self.target / "TASKS.md").open("a", encoding="utf-8") as stream:
            stream.write("\n用户自己写的说明。\n")
        original = (self.target / "TASKS.md").read_bytes()
        plan, before, _ = build_update(self.target, "qa", "实现已完成", "执行测试")
        self.assertEqual((self.target / "TASKS.md").read_bytes(), original)
        apply_update(self.target, plan, before)
        updated = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(updated["rule_version"], "0.3.1")
        self.assertEqual(updated["confirmation_note"], "用户在对话中确认待办 MVP")
        self.assertIn("用户自己写的说明", (self.target / "TASKS.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--work-dir", type=Path, required=True)
    args = parser.parse_args()
    WORK_DIR = args.work_dir.resolve()
    WORK_DIR.mkdir(parents=True, exist_ok=True)
    unittest.main(argv=["test_workflow.py"], verbosity=2)
