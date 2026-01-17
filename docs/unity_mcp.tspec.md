# Unity MCP manual
JP: Unity MCP 連携マニュアル

```tspec
manual:
  id: unity-mcp
  title: 'Unity MCP setup / JP: Unity MCP 連携セットアップ'
  tags:
  - mcp
  - unity
  - integration
  - setup
  summary: 'EN: Configure Unity MCP HTTP endpoint as tspec MCP tools.

    JP: Unity の HTTP エンドポイントを MCP tool として呼び出すための設定。

    '
  prerequisites:
  - pip install -e '.[mcp,unity]'
  - Unity MCP HTTP server exposes /health and /mcp
  - 'JP: pip install -e ''.[mcp,unity]'''
  - 'JP: Unity MCP の HTTP サーバ（/health と /mcp）が起動していること'
  steps:
  - title: '1) Set environment variables / JP: 1) 環境変数を設定'
    body: "EN:\n  UNITY_MCP_MODE=mcp-http\n  UNITY_MCP_MCP_URL=http://localhost:8080/mcp\n\
      \  UNITY_MCP_ALLOWLIST_HOSTS=localhost,localhost:8080\n  (optional) UNITY_MCP_AUTH_MODE=none|bearer|token\n\
      JP:\n  UNITY_MCP_MODE=mcp-http\n  UNITY_MCP_MCP_URL=http://localhost:8080/mcp\n\
      \  UNITY_MCP_ALLOWLIST_HOSTS=localhost,localhost:8080\n  (任意) UNITY_MCP_AUTH_MODE=none|bearer|token\n"
  - title: '2) Start tspec MCP server / JP: 2) MCP サーバを起動'
    body: "tspec mcp --transport stdio --workdir .\nEN: Optional CLI override:\n \
      \ tspec mcp --transport stdio --unity-mcp-url http://localhost:8080/mcp\n\n\
      JP:\ntspec mcp --transport stdio --workdir ."
  - title: '3) Verify tools / JP: 3) ツール動作確認'
    body: 'unity.health

      unity.tool(name="debug_request_context", arguments={})


      JP:

      unity.health

      unity.tool(name="debug_request_context", arguments={})'
```