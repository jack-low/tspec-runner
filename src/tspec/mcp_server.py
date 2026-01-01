from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, Optional

from .errors import ExecutionError, ValidationError


def _resolve_workdir(workdir: Optional[str]) -> Path:
    wd = workdir or os.environ.get("TSPEC_WORKDIR") or os.getcwd()
    return Path(wd).resolve()


def _safe_path(workdir: Path, p: str) -> Path:
    """Resolve a path under workdir. Reject escapes."""
    if not p:
        raise ValidationError("path is required")
    rp = (workdir / p).resolve() if not Path(p).is_absolute() else Path(p).resolve()
    try:
        rp.relative_to(workdir)
    except Exception as e:
        raise ValidationError(f"path must be under workdir: {workdir} (got {rp})") from e
    return rp


def start(
    *,
    transport: str = "stdio",
    workdir: Optional[str] = None,
    host: str = "127.0.0.1",
    port: int = 8765,
) -> None:
    """Start tspec MCP server.

    - stdio: recommended for local clients (Claude Desktop etc.)
    - streamable-http: for inspector / remote
    """
    try:
        from mcp.server.fastmcp import FastMCP  # type: ignore
    except Exception as e:  # pragma: no cover
        raise ExecutionError("MCP support requires: pip install -e '.[mcp]'") from e

    from .manual_loader import discover_manuals, find_manual_by_id, load_manual
    from .doctor_android import check_android_env
    from .doctor_selenium import check_selenium_env
    from .doctor_ios import check_ios_env
    from .report_view import load_report as load_report_view, format_error_message
    from .programmatic import run_spec_file
    from .validate import load_and_validate

    wd = _resolve_workdir(workdir)

    mcp = FastMCP(
        name="tspec-runner",
        instructions=(
            "Tools to validate/run TSpec specs and inspect reports/manuals. "

            "For safety, all file paths are resolved under workdir."

        ),
    )

    # ---------- Tools ----------
    @mcp.tool()
    def tspec_validate(path: str) -> Dict[str, Any]:
        """Validate a spec and return resolved version + case count."""
        p = _safe_path(wd, path)
        doc, spec = load_and_validate(p)
        return {
            "path": str(p),
            "declared": getattr(spec, "declared", None),
            "resolved": str(spec.resolved),
            "case_count": len(doc.cases),
        }

    @mcp.tool()
    def tspec_run(
        path: str,
        backend: str = "selenium",
        report: str = "out/report.json",
        case_id: Optional[str] = None,  # reserved for future
    ) -> Dict[str, Any]:
        """Run a spec; writes report JSON and returns summary."""
        p = _safe_path(wd, path)
        r = _safe_path(wd, report)
        result = run_spec_file(p, backend=backend, report=r)
        passed = sum(1 for c in result.get("cases", []) if c.get("status") == "passed")
        failed = len(result.get("cases", [])) - passed
        return {"path": str(p), "backend": backend, "report": str(r), "passed": passed, "failed": failed}

    @mcp.tool()
    def tspec_report(
        report: str,
        only_errors: bool = False,
        case_id: Optional[str] = None,
        full_trace: bool = False,
        max_rows: int = 50,
    ) -> Dict[str, Any]:
        """Summarize a JSON report; returns rows (optionally only errors)."""
        rp = _safe_path(wd, report)
        rv = load_report_view(rp)

        rows = []
        for c in rv.cases:
            if case_id and c.id != case_id:
                continue
            for s in c.steps:
                status = s.status
                if only_errors and status == "passed":
                    continue
                msg = format_error_message(s.error, full_trace=full_trace) if s.error else ""
                rows.append(
                    {
                        "case_id": c.id,
                        "title": c.title,
                        "step": s.do if s.name is None else f"{s.do} ({s.name})",
                        "status": status,
                        "message": msg,
                    }
                )

        summary = {
            "cases_total": len(rv.cases),
            "steps_total": sum(len(c.steps) for c in rv.cases),
            "rows_returned": min(len(rows), max_rows),
            "truncated": len(rows) > max_rows,
        }
        return {"report": str(rp), "summary": summary, "rows": rows[:max_rows]}

    @mcp.tool()
    def tspec_manual_list(base: str = "docs") -> Dict[str, Any]:
        b = _safe_path(wd, base)
        items = discover_manuals(b)
        return {
            "base": str(b),
            "manuals": [
                {"id": mf.manual.id, "title": mf.manual.title, "tags": mf.manual.tags, "path": str(p)}
                for p, mf in items
            ],
        }

    @mcp.tool()
    def tspec_manual_show(target: str, base: str = "docs", full: bool = False) -> Dict[str, Any]:
        tp = Path(target)
        if tp.exists():
            p = _safe_path(wd, target)
            mf = load_manual(p)
        else:
            b = _safe_path(wd, base)
            p, mf = find_manual_by_id(b, target)
        man = mf.manual
        out: Dict[str, Any] = {
            "id": man.id,
            "title": man.title,
            "tags": man.tags,
            "summary": man.summary,
            "prerequisites": man.prerequisites,
            "steps": [{"title": s.title, "body": s.body} for s in man.steps],
        }
        if full:
            out["troubleshooting"] = [{"title": s.title, "body": s.body} for s in man.troubleshooting]
            out["references"] = man.references
        return out

    @mcp.tool()
    def tspec_doctor(android: bool = False, selenium: bool = False, ios: bool = False) -> Dict[str, Any]:
        out: Dict[str, Any] = {"workdir": str(wd), "checks": {}}
        if android:
            out["checks"]["android"] = [c.__dict__ for c in check_android_env()]
        if selenium:
            out["checks"]["selenium"] = [c.__dict__ for c in check_selenium_env()]
        if ios:
            out["checks"]["ios"] = [c.__dict__ for c in check_ios_env()]
        return out

    # ---------- Resources (read-only) ----------
    @mcp.resource("file://workdir")
    def workdir_info() -> str:
        return str(wd)

    # Run
    if transport not in {"stdio", "streamable-http"}:
        raise ExecutionError("transport must be 'stdio' or 'streamable-http'")

    if transport == "streamable-http":
        mcp.settings.host = host
        mcp.settings.port = port
        mcp.run(transport="streamable-http")
    else:
        mcp.run(transport="stdio")
