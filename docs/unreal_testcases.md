# Unreal Engine MCP TestCases
JP: Unreal Engine MCP テストケース

## Preconditions
- Unreal Engine 5.5+ running with UnrealMCP plugin enabled
- `uv` available
JP: UE とプラグイン起動が前提

## TestCases

### UE-001: MCP server start
- Goal: start the MCP server
- Steps: `uv run unreal_mcp_server_advanced.py` (in `unreal-engine-mcp/Python`)
- Expected: server starts and waits for UE connection
JP: サーバ起動確認

### UE-002: MCP client connect
- Goal: MCP client can call tools
- Steps: connect from MCP client (Cursor/Claude/Windsurf) and list tools
- Expected: tools list returned
JP: MCP クライアントでツール一覧取得


## JP (original)
# Unreal Engine MCP TestCase 仕様

目的: Unreal Engine MCP サーバの起動と MCP クライアント接続を確認する。

## Manual / Integration (optional)
- TC-UE-001: サーバが起動し、UE から接続できる
- TC-UE-002: MCP クライアントからツールを呼び出せる
