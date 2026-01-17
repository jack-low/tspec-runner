# MCP overview

```tspec
manual:
  id: mcp
  title: MCP quick reference
  tags:
    - mcp
    - env
  summary: How to start tspec MCP helpers, check supported backends, and visit environment manuals for Blender/Unity/Unreal.
  prerequisites:
    - uv
    - tspec-runner installed with extras (mcp, blender, unity)
  steps:
    - title: Start the tspec MCP server (stdio)
      body: |
        cd <repo>
        tspec mcp --transport stdio
    - title: Start the tspec MCP server (streamable-http, optional)
      body: |
        cd <repo>
        tspec mcp --transport streamable-http --host 127.0.0.1 --port 8765
    - title: Run backend diagnostics
      body: |
        tspec doctor --selenium --android --ios
    - title: Review Blender/Unity/Unreal MCP guides
      body: |
        tspec manual show blender-mcp --lang en
        tspec manual show unity-mcp --lang en
        tspec manual show unreal-mcp --lang en
  troubleshooting:
    - title: Manual lookup still fails for "mcp"
      body: |
        Run `tspec manual list --lang en` to see available manuals. Use an exact id (e.g., `mcp-env`, `blender-mcp`, `unity-mcp`, `unreal-mcp`) or specify the file path.
  references:
    - 'MCP tools doc: docs/mcp_env.en.tspec.md'
```
