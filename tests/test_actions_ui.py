from __future__ import annotations

import re
from pathlib import Path

import pytest

from tspec.actions_ui import _forensics_dump, _safe, ui_wait_for
from tspec.errors import ExecutionError


class _DummyInnerDriver:
    current_url = "https://example.test/"
    page_source = "<html><body>ok</body></html>"


class _DummyUIDriver:
    def __init__(self, artifact_dir: Path) -> None:
        self.driver = _DummyInnerDriver()
        self._artifact_dir = artifact_dir

    def screenshot(self, path: str) -> None:
        Path(path).write_text("png", encoding="utf-8")

    def wait_for(self, selector: str, text_contains: str | None, timeout_ms: int) -> None:
        raise RuntimeError("element not found")


class _DummyUI:
    def __init__(self, driver: _DummyUIDriver) -> None:
        self.driver = driver


class _DummyCtx:
    def __init__(self, artifact_dir: Path) -> None:
        self.artifact_dir = str(artifact_dir)
        self.case = {"id": "case/with spaces"}
        self.default_timeout_ms = 1234
        self.ui = _DummyUI(_DummyUIDriver(artifact_dir))


def test_safe_sanitizes_strings() -> None:
    assert _safe("  hello/world?*  ") == "hello_world_"
    assert _safe("") == "step"
    assert _safe("a" * 200) == "a" * 80


def test_forensics_dump_writes_artifacts(tmp_path: Path) -> None:
    ctx = _DummyCtx(tmp_path)
    out = _forensics_dump(ctx, prefix="step:1")

    assert "screenshot" in out
    assert "current_url" in out
    assert "page_source" in out
    assert Path(out["screenshot"]).exists()
    assert Path(out["page_source"]).read_text(encoding="utf-8") == _DummyInnerDriver.page_source


def test_ui_wait_for_includes_diagnostics(tmp_path: Path) -> None:
    ctx = _DummyCtx(tmp_path)

    with pytest.raises(ExecutionError) as exc_info:
        ui_wait_for(ctx, {"selector": "#missing", "text_contains": "ready"})

    msg = str(exc_info.value)
    assert "ui.wait_for failed" in msg
    assert "text_contains='ready'" in msg
    assert "url=https://example.test/" in msg

    shot_match = re.search(r"screenshot=([^\s]+)", msg)
    source_match = re.search(r"page_source=([^\s]+)", msg)
    assert shot_match
    assert source_match
    assert Path(shot_match.group(1)).exists()
    assert Path(source_match.group(1)).exists()
