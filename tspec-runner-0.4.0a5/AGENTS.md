# AGENTS

This repository contains **tspec-runner**, a CLI + MCP server for running TSpec (Markdown + fenced `tspec`) automation.

## Development environment
- Python >= 3.11
- Recommended: `uv`

### Setup
```bash
uv venv
uv sync
```

### Run CLI
```bash
python -m tspec.cli --help
```

### Run MCP server
```bash
# stdio (recommended)
python -m tspec.cli mcp --transport stdio

# streamable-http
python -m tspec.cli mcp --transport streamable-http --host 127.0.0.1 --port 8765
```

## Neko MCP integration
To enable Neko tools, set:
- `NEKO_BASE_URL`
- (recommended) `NEKO_ALLOWLIST_HOSTS`

See `docs/neko_mcp.md`.

## Testing
```bash
pytest -q
```

## Conventions
- Keep core lightweight; optional integrations via extras.
- Never log secrets (tokens/passwords).
- For any file path arguments, resolve under workdir (existing safety rule).
