# agent-browser Environment Setup Manual
JP: agent-browser 環境構築マニュアル

This file is editable. The actual manual content is stored in the ` ```tspec ` block and can be displayed via `tspec manual`.
JP: このファイルは編集可能です。内容は ` ```tspec ` ブロックに格納され、`tspec manual` で表示できます。

```tspec
manual:
  id: agent-browser-env
  title: 'agent-browser setup / JP: agent-browser 環境構築'
  tags:
  - agent-browser
  - web
  - headless
  - setup
  summary: 'EN: agent-browser is a lightweight headless browser CLI. It can be a Selenium
    alternative in simple cases.

    JP: agent-browser は軽量な headless ブラウザ CLI。Selenium を避けたいケースの代替として使える。

    '
  prerequisites:
  - Node.js (npm)
  - 'JP: Node.js (npm)'
  steps:
  - title: '1) Install agent-browser / JP: 1) agent-browser をインストール'
    body: "EN: Install with npm and run the installer.\nJP: npm でインストール後、install を実行。\n\
      \nnpm install -g agent-browser\nagent-browser install\n\nEN: If install fails\
      \ on Windows, run the exe directly:\nJP: Windows で install が失敗する場合は exe を直接実行する：\n\
      \  $env:APPDATA\\\\npm\\\\node_modules\\\\agent-browser\\\\bin\\\\agent-browser-win32-x64.exe\
      \ install\n"
  - title: '2) Smoke test / JP: 2) 動作確認'
    body: 'EN: Basic CLI smoke test.

      JP: CLI の動作確認。


      agent-browser open https://example.com

      agent-browser snapshot

      agent-browser screenshot artifacts/agent-browser/smoke.png

      agent-browser close

      '
  - title: '3) Use from tspec-runner / JP: 3) tspec-runner から使う'
    body: "EN: Run the sample spec with the agent-browser backend.\nJP: agent-browser\
      \ backend でサンプルを実行。\n\ntspec run examples/agent_browser_smoke.tspec.md --backend\
      \ agent-browser --report out/agent-browser.json\n\nEN: If agent-browser is not\
      \ found on Windows, set the binary path:\nJP: Windows で agent-browser が見つからない場合は\
      \ binary を指定する：\n  [agent_browser]\n  binary = \"C:/Users/<user>/AppData/Roaming/npm/node_modules/agent-browser/bin/agent-browser-win32-x64.exe\"\
      \n"
  - title: '4) Optional: fallback to WSL / JP: 4) Windows から WSL 版にフォールバック（任意）'
    body: "EN: If Windows agent-browser is unavailable, use a WSL fallback configuration.\n\
      JP: Windows 側に agent-browser が無い場合、WSL の agent-browser を使う設定例：\n\n  [agent_browser]\n\
      \  wsl_fallback = true\n  wsl_distro = \"Ubuntu\"\n  wsl_workdir = \"/mnt/c/WorkSpace/Private/Python/tspec-runner\"\
      \n\nEN: Run with --config:\nJP: 実行時は --config を指定する：\n  tspec run examples/agent_browser_smoke.tspec.md\
      \ --backend agent-browser --config tspec.toml --report out/agent-browser.json\n"
  troubleshooting:
  - title: 'agent-browser not found / JP: agent-browser が見つからない'
    body: 'EN: PATH might be missing npm''s global bin.

      JP: PATH が通っていない可能性。npm の global bin を PATH に追加する。

      '
  - title: 'Daemon failed to start / JP: Daemon failed to start'
    body: 'EN: The Windows CLI may fail to spawn the daemon; tspec-runner falls back
      to protocol mode.

      JP: Windows で CLI が daemon を起動できない場合がある。tspec-runner は内部で protocol 接続にフォールバックする。

      '
  references:
  - 'agent-browser: https://github.com/vercel-labs/agent-browser'
```
## Quick summary
- install: `npm install -g agent-browser` -> `agent-browser install` (Windows: exe fallback)
- run: `tspec run examples/agent_browser_smoke.tspec.md --backend agent-browser --report out/agent-browser.json`
- Windows fallback: `[agent_browser] binary=...` or `wsl_fallback=true`
JP: 手順の要約は上記です。
