from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

from .context import RunContext
from .errors import ExecutionError


def _ensure_mcp_client():
    try:
        from mcp.client.stdio import StdioServerParameters, stdio_client
        from mcp import ClientSession
    except Exception as exc:  # pragma: no cover
        raise ExecutionError("Unreal MCP automation requires: pip install -e '.[mcp]'") from exc
    return StdioServerParameters, stdio_client, ClientSession


def _to_float_list(value: Optional[Iterable[Any]], length: int) -> List[float]:
    if value is None:
        return [0.0] * length
    lst = list(value)
    if len(lst) != length:
        raise ExecutionError(f"expected {length} floats for location, got {len(lst)}")
    try:
        return [float(v) for v in lst]
    except ValueError as exc:
        raise ExecutionError(f"location values must be numeric: {exc}") from exc


def _embed_tool_args(args: Dict[str, Any]) -> Dict[str, Any]:
    location = _to_float_list(args.get("location"), 3)
    tool_args: Dict[str, Any] = {
        "castle_size": args.get("castle_size", "small"),
        "location": location,
        "name_prefix": args.get("name_prefix", "Castle"),
        "include_siege_weapons": bool(args.get("include_siege_weapons", True)),
        "include_village": bool(args.get("include_village", True)),
        "architectural_style": args.get("architectural_style", "medieval"),
    }
    return tool_args


async def _call_tool_async(
    script: Path,
    tool_name: str,
    tool_args: Dict[str, Any],
) -> Dict[str, Any]:
    StdioServerParameters, stdio_client, ClientSession = _ensure_mcp_client()

    params = StdioServerParameters(
        command="uv",
        args=["run", "--with", "mcp", "python", str(script)],
        env=None,
    )

    async with stdio_client(params) as (reader, writer):
        async with ClientSession(reader, writer) as session:
            await session.initialize()
            return await session.call_tool(tool_name, tool_args)


def _run_tool(script: Path, tool_name: str, tool_args: Dict[str, Any], timeout_ms: int) -> Dict[str, Any]:
    timeout_secs = timeout_ms / 1000.0 if timeout_ms else None

    async def _inner():
        return await _call_tool_async(script, tool_name, tool_args, timeout_secs)

    try:
        if timeout_secs is None:
            return asyncio.run(_inner())
        return asyncio.run(asyncio.wait_for(_inner(), timeout_secs))
    except asyncio.TimeoutError as exc:
        raise ExecutionError(f"Unreal MCP tool '{tool_name}' timed out after {timeout_ms} ms") from exc
    except Exception as exc:
        raise ExecutionError(f"Unreal MCP tool '{tool_name}' failed: {exc}") from exc


def create_castle(ctx: RunContext, args: Dict[str, Any]) -> Dict[str, Any]:
    script_arg = args.get("server_script")
    script_path = Path(script_arg or "local_notes/unreal-engine-mcp/Python/unreal_mcp_server_advanced.py").resolve()
    if not script_path.exists():
        raise ExecutionError(f"Unreal MCP server script not found at {script_path}")

    tool_name = args.get("tool", "create_castle_fortress")
    timeout_ms = int(args.get("timeout_ms", 420000) or 420000)
    tool_args = _embed_tool_args(args)

    result = _run_tool(script_path, tool_name, tool_args, timeout_ms)
    return result
