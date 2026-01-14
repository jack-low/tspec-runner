# agent-browser TestCase 仕様

目的: agent-browser backend が CLI 経由で基本動作できることを確認する。

## Unit Test Cases
- TC-AB-001: backend 指定で `agent-browser` が選択できる
- TC-AB-002: `agent_browser` / `agent-browser` の両表記が同じ backend に解決される

## Manual / Integration (optional)
- TC-AB-003: `tspec run examples/agent_browser_smoke.tspec.md --backend agent-browser` が完走する
- TC-AB-004: `ui.wait_for` が selector を検出できる
