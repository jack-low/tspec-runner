from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

from .errors import ExecutionError, ValidationError
from .model import Document, Step
from .templating import render
from .when_expr import eval_when
from .registry import ActionRegistry
from .context import RunContext
from . import actions_assert
from . import actions_ui

@dataclass
class StepResult:
    do: str
    name: Optional[str]
    status: str
    duration_ms: int
    error: Optional[Dict[str, Any]] = None

class Runner:
    def __init__(self, doc: Document, *, ctx: RunContext, registry: ActionRegistry):
        self.doc = doc
        self.ctx = ctx
        self.registry = registry

    def _should_skip(self, skip_field) -> Tuple[bool, Optional[str]]:
        if skip_field is True:
            return True, "skipped"
        if isinstance(skip_field, str) and skip_field.strip():
            return True, skip_field.strip()
        return False, None

    def _when_ok(self, when_expr: Optional[str]) -> bool:
        if not when_expr:
            return True
        return eval_when(when_expr, self._render_ctx())

    def _render_ctx(self) -> Dict[str, Any]:
        # templating context; expose vars + saved at top-level
        base = {
            "vars": self.ctx.vars,
            "env": self.ctx.env,
            "suite": self.ctx.suite,
            "case": self.ctx.case,
            **self.ctx.vars,
            **self.ctx.saved,
        }
        return base

    def _dispatch(self, do: str, args: Dict[str, Any]) -> Any:
        if do not in self.registry.actions:
            raise ExecutionError(f"Unknown action: {do}")
        return self.registry.actions[do](self.ctx, args)

    def _run_step(self, step: Step, step_index: int) -> StepResult:
        # expose step index for diagnostics
        self.ctx.env['__step_index'] = step_index
        sk, reason = self._should_skip(step.skip)
        if sk:
            return StepResult(step.do, step.name, "skipped", 0, {"message": reason})

        if step.when and not self._when_ok(step.when):
            return StepResult(step.do, step.name, "skipped", 0, {"message": "when=false"})

        start = time.time()
        try:
            args = render(step.with_, self._render_ctx())
            # allow per-step timeout injection for ui.wait_for
            if step.timeout_ms is not None:
                args = dict(args)
                args.setdefault("timeout_ms", step.timeout_ms)

            out = self._dispatch(step.do, args)

            if isinstance(step.save, str) and step.save.strip():
                self.ctx.put_save(step.save.strip(), out)

            status, err = "passed", None
        except ExecutionError as e:
            status, err = "failed", {"type": "ExecutionError", "message": str(e)}
        except Exception as e:
            status, err = "error", {"type": e.__class__.__name__, "message": str(e)}

        dur = int((time.time() - start) * 1000)
        return StepResult(step.do, step.name, status, dur, err)

    def run(self) -> Dict[str, Any]:
        case_results = []

        for case in self.doc.cases:
            self.ctx.case = {"id": case.id, "title": case.title, "tags": case.tags}

            sk, _reason = self._should_skip(case.skip)
            if sk or (case.when and not self._when_ok(case.when)):
                case_results.append({"id": case.id, "title": case.title, "status": "skipped", "steps": []})
                continue

            steps_out: List[Dict[str, Any]] = []
            status = "passed"

            for i, step in enumerate(case.steps, start=1):
                r = self._run_step(step, i)
                steps_out.append({
                    "do": r.do, "name": r.name, "status": r.status,
                    "duration_ms": r.duration_ms, "error": r.error,
                })
                if r.status in ("failed", "error"):
                    status = r.status
                    if self.doc.suite.fail_fast:
                        break

            case_results.append({"id": case.id, "title": case.title, "status": status, "steps": steps_out})
            if self.doc.suite.fail_fast and status != "passed":
                break

        return {"suite": {"name": self.doc.suite.name, "tags": self.doc.suite.tags}, "cases": case_results}


def build_registry() -> ActionRegistry:
    reg = ActionRegistry()
    reg.register("assert.equals", lambda ctx, a: actions_assert.equals(a))
    reg.register("assert.true", lambda ctx, a: actions_assert.true(a))
    reg.register("assert.contains", lambda ctx, a: actions_assert.contains(a))
    reg.register("assert.matches", lambda ctx, a: actions_assert.matches(a))

    # ui.* actions depend on ctx.ui
    reg.register("ui.open", lambda ctx, a: actions_ui.ui_open(ctx, a))
    reg.register("ui.open_app", lambda ctx, a: actions_ui.ui_open_app(ctx, a))
    reg.register("ui.click", lambda ctx, a: actions_ui.ui_click(ctx, a))
    reg.register("ui.type", lambda ctx, a: actions_ui.ui_type(ctx, a))
    reg.register("ui.wait_for", lambda ctx, a: actions_ui.ui_wait_for(ctx, a))
    reg.register("ui.get_text", lambda ctx, a: actions_ui.ui_get_text(ctx, a))
    reg.register("ui.screenshot", lambda ctx, a: actions_ui.ui_screenshot(ctx, a))
    reg.register("ui.close", lambda ctx, a: actions_ui.ui_close(ctx, a))
    return reg
