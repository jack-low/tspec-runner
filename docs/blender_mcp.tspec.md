# Blender MCP manual
JP: Blender MCP 連携マニュアル

```tspec
manual:
  id: blender-mcp
  title: 'Blender MCP setup / JP: Blender MCP 連携セットアップ'
  tags:
  - mcp
  - blender
  - integration
  - setup
  summary: 'EN: Configure Blender HTTP endpoints as tspec MCP tools.

    JP: Blender の HTTP エンドポイントを MCP tool として呼び出すための設定。

    '
  prerequisites:
  - pip install -e '.[mcp,blender]'
  - Blender exposes /health and /rpc HTTP endpoints
  - blender-mcp is stdio; REST requires a proxy
  - 'JP: pip install -e ''.[mcp,blender]'''
  - 'JP: Blender 側に /health と /rpc の HTTP エンドポイントがあること'
  - 'JP: blender-mcp は stdio のため、そのままでは REST 連携不可'
  steps:
  - title: '1) Set environment variables / JP: 1) 環境変数を設定'
    body: 'BLENDER_MCP_BASE_URL=http://localhost:7300

      BLENDER_MCP_ALLOWLIST_HOSTS=localhost,localhost:7300

      (optional) BLENDER_MCP_AUTH_MODE=none|bearer|token


      JP:

      BLENDER_MCP_BASE_URL=http://localhost:7300

      BLENDER_MCP_ALLOWLIST_HOSTS=localhost,localhost:7300

      (任意) BLENDER_MCP_AUTH_MODE=none|bearer|token'
  - title: '2) Start tspec MCP server / JP: 2) MCP サーバを起動'
    body: "tspec mcp --transport stdio --workdir .\nEN: Optional CLI override:\n \
      \ tspec mcp --transport stdio --blender-mcp-url http://localhost:7300\n\nJP:\n\
      tspec mcp --transport stdio --workdir ."
  - title: '3) Verify tools / JP: 3) ツール動作確認'
    body: 'blender.health

      blender.rpc(method="scene.list", params={})


      JP:

      blender.health

      blender.rpc(method="scene.list", params={})'
```