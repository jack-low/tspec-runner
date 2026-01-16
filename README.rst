tspec-runner 1.0.5
==================

TSpec (Markdown + ``tspec``) を読み込み、CLI で検証・実行・レポートまで完結する自動化ランナーです。
Markdown の中にある ``tspec`` ブロックを読み取り、同じ手順を複数環境で再現できます。

リンク
----------------------------------------
- GitHub: https://github.com/jack-low/tspec-runner
- PyPI: https://pypi.org/project/tspec-runner/

できること
----------------------------------------
- Spec バージョン解決（無指定＝最新 / 範囲指定 / 3世代前まで）
- validate / list / run / spec / init / doctor / report
- ``assert.*`` による簡易テスト
- **UI 自動化インターフェース（統一 API）**：``ui.*``
  - backend: ``selenium`` / ``appium``(Android/iOS) / ``pywinauto`` / ``agent-browser``
  - 依存は extras で追加（軽いコア）

.. note::
   Android/iOS は Appium を前提にしています（Appium Server + driver は別途セットアップ）。

クイックスタート（推奨: uv）
----------------------------------------
.. code-block:: bash

   uv venv
   uv sync
   tspec validate examples/assert_only.tspec.md
   tspec run examples/assert_only.tspec.md --report out/report.json

pip を使う場合:

.. code-block:: bash

   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -U pip
   pip install -e ".[dev]"

使い方（基本）
----------------------------------------
.. code-block:: bash

   tspec spec
   tspec init example.tspec.md
   tspec validate examples/assert_only.tspec.md --explain-version
   tspec run examples/assert_only.tspec.md --report out/report.json
   tspec report out/report.json --only-errors --show-steps

UI 実行（例：Selenium）
----------------------------------------
.. code-block:: bash

   tspec run examples/selenium_google.tspec.md --backend selenium --report out/ui.json

UI 実行（例：Appium/Android）
----------------------------------------
.. code-block:: bash

   tspec run examples/android_youtube_smoke.tspec.md --backend appium --report out/android_youtube_smoke.json

検索ありのサンプルは YouTube UI 変更の影響を受けやすいので、
``examples/android_youtube_search_play.tspec.md`` の selector を環境に合わせて調整してください。

UI 実行（例：agent-browser）
----------------------------------------
.. code-block:: bash

   tspec run examples/agent_browser_smoke.tspec.md --backend agent-browser --report out/agent-browser.json

画面キャプチャ（実行例）
----------------------------------------
agent-browser による smoke 実行のスクリーンショット:

.. image:: data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAA4KCw0LCQ4NDA0QDw4RFiQXFhQUFiwgIRokNC43NjMuMjI6QVNGOj1OPjIySGJJTlZYXV5dOEVmbWVabFNbXVn/2wBDAQ8QEBYTFioXFypZOzI7WVlZWVlZWVlZWVlZWVlZWVlZWVlZWVlZWVlZWVlZWVlZWVlZWVlZWVlZWVlZWVlZWVn/wAARCAAtAFADASIAAhEBAxEB/8QAGAABAQADAAAAAAAAAAAAAAAAAAIBAwb/xAAlEAEAAgADBwUAAAAAAAAAAAAAAQIDElIREyEycaHRU2GBkZL/xAAUAQEAAAAAAAAAAAAAAAAAAAAA/8QAFBEBAAAAAAAAAAAAAAAAAAAAAP/aAAwDAQACEQMRAD8A78AEb3D9Sn6hVbVty2iektVcKNvGsR8R4XGHl5bTHSI8AsTlnXbsxlnXb6gFics67diKzE7ZtM+3AFAAAAAAAAAAAAAAAAAAAAAA/9k=
   :alt: agent-browser smoke






Selenium（Example Domain）のスクリーンショット:

.. image:: data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAA4KCw0LCQ4NDA0QDw4RFiQXFhQUFiwgIRokNC43NjMuMjI6QVNGOj1OPjIySGJJTlZYXV5dOEVmbWVabFNbXVn/2wBDAQ8QEBYTFioXFypZOzI7WVlZWVlZWVlZWVlZWVlZWVlZWVlZWVlZWVlZWVlZWVlZWVlZWVlZWVlZWVlZWVlZWVn/wAARCAAtAFADASIAAhEBAxEB/8QAGQABAAMBAQAAAAAAAAAAAAAAAAIDBAEG/8QAJBABAAEDAgUFAAAAAAAAAAAAAAECAxETIQQSIjGSFFNhcYH/xAAUAQEAAAAAAAAAAAAAAAAAAAAA/8QAFBEBAAAAAAAAAAAAAAAAAAAAAP/aAAwDAQACEQMRAD8A9+ADmYmM52MxM4zDBNvhe2hb80tPhZ20KJxG3UDcMtqu1ZiabVumI+Ku6XqYzMTEeUA0CqLlcxmLX11RunTMzHVTy/uQSAAABXy3PcjxWAAAAAAAAAAAAAAAAAD/2Q==
   :alt: selenium example






Appium（YouTube / Androidエミュレータ）のスクリーンショット:

.. image:: data:image/jpeg;base64,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
   :alt: appium android youtube






Appium 検索フロー（Home -> Search -> Results -> Player）:

.. image:: data:image/jpeg;base64,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
   :alt: appium youtube search

.. image:: data:image/jpeg;base64,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
   :alt: appium youtube results

.. image:: data:image/jpeg;base64,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
   :alt: appium youtube player














レポート HTML のスクリーンショット:

.. image:: data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAA4KCw0LCQ4NDA0QDw4RFiQXFhQUFiwgIRokNC43NjMuMjI6QVNGOj1OPjIySGJJTlZYXV5dOEVmbWVabFNbXVn/2wBDAQ8QEBYTFioXFypZOzI7WVlZWVlZWVlZWVlZWVlZWVlZWVlZWVlZWVlZWVlZWVlZWVlZWVlZWVlZWVlZWVlZWVn/wAARCAAtAFADASIAAhEBAxEB/8QAGQABAQEBAQEAAAAAAAAAAAAAAAIBAwQG/8QAKRAAAgIBAwIDCQAAAAAAAAAAAAECEQMSITFRkQRhgRQyQVNxoaLR8P/EABQBAQAAAAAAAAAAAAAAAAAAAAD/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIRAxEAPwD7lQm8nveIVvlzdI6eyzt3my8fNf6Ozi1GXHYQjKSt/YCsalGMY3aXxcrZ0JSae9FAAAAAAAAAeWGRvI1klFR8pHSKxt1DJv0UjViuVyb8kpM3Q1xv6sCoxp8t/VlEaX0/JmaH/TYHQEqNde7NA0GADQRobbtv0Y0b3b7gWAAAAAAAAAAAAA//2Q==
   :alt: report example






.. note::
   Android/iOS のスクリーンショットは Appium Server と実機/エミュレータが必要です。

UI backend を使う場合（extras）
----------------------------------------
Selenium

.. code-block:: bash

   pip install -e ".[selenium]"

Appium（Android/iOS）

.. code-block:: bash

   pip install -e ".[appium]"

pywinauto（Windows GUI）

.. code-block:: bash

   pip install -e ".[pywinauto]"

agent-browser（軽量 headless）

.. code-block:: bash

   npm install -g agent-browser
   agent-browser install

Windows で install が失敗する場合は exe を直接実行する：

.. code-block:: powershell

   & "$env:APPDATA\\npm\\node_modules\\agent-browser\\bin\\agent-browser-win32-x64.exe" install

設定（任意）: tspec.toml
----------------------------------------
``--config tspec.toml`` で読み込みます。最小例：

.. code-block:: toml

   [ui]
   backend = "selenium"  # selenium|appium|pywinauto|agent-browser
   headless = true
   implicit_wait_ms = 2000

   [selenium]
   browser = "chrome"  # chrome|firefox
   driver_path = ""    # optional: chromedriver/geckodriver path
   browser_binary = "" # optional: custom browser binary
   args = ["--lang=ja-JP"]
   prefs = { "intl.accept_languages" = "ja-JP" }
   download_dir = "artifacts/downloads"
   window_size = "1280x720"
   auto_wait_ms = 3000
   page_load_timeout_ms = 30000
   script_timeout_ms = 30000

   [agent_browser]
   binary = "agent-browser"
   timeout_ms = 30000
   poll_ms = 250
   extra_args = []
   wsl_fallback = false
   wsl_distro = ""
   wsl_workdir = ""

``ui.*`` の主なアクション
----------------------------------------
- ``ui.open`` with ``{url}`` （Selenium / agent-browser）
- ``ui.open_app`` with ``{caps, server_url}`` （Appium）
- ``ui.click`` with ``{selector}``
- ``ui.type`` with ``{selector, text}``
- ``ui.wait_for`` with ``{selector, text_contains?}``
- ``ui.get_text`` with ``{selector}`` + ``save: "name"``
- ``ui.screenshot`` with ``{path}``
- ``ui.close``

.. note::
   selector は backend ごとに解釈されます（Seleniumは CSS を基本、``css=``/``xpath=``/``id=``/``name=``/``link=`` などのprefixも可）。

Neko (m1k1o/neko) MCP 連携
----------------------------------------
MCP Server で ``neko.*`` を有効化し、Neko の REST API をツールとして使えます。

準備:

- ``pip install -e ".[mcp,neko]"``
- 環境変数を設定:
  - ``NEKO_BASE_URL``（例: ``http://localhost:8080``）
  - ``NEKO_ALLOWLIST_HOSTS``（例: ``localhost,localhost:8080``）
  - 任意: ``NEKO_AUTH_MODE``, ``NEKO_USERNAME``, ``NEKO_PASSWORD``, ``NEKO_BEARER_TOKEN``

起動:

.. code-block:: bash

   tspec mcp --transport stdio --workdir .

詳細: ``docs/neko_mcp.md``

レポート表示
----------------------------------------
.. code-block:: bash

   tspec report out/report.json
   tspec report out/report.json --only-errors --show-steps
   tspec report out/report.json --case UI-001 --show-steps
   tspec report out/report.json --grep google --status failed --status error

メッセージが長い場合（Stacktrace等）
----------------------------------------
.. code-block:: bash

   tspec report out/report.json --only-errors --show-steps --full-trace --max-message-len 0

失敗時の鑑識セット（自動採取）
----------------------------------------
- ``ui.wait_for`` が失敗すると、既定で以下を ``artifacts/forensics/`` に保存します：
  - screenshot（PNG）
  - current_url（メッセージに表示）
  - page_source（HTML, Seleniumのみ）

MCP (AI連携)
----------------------------------------
MCP Server として起動し、AIクライアントから TSpec をツール呼び出しできます。

.. code-block:: bash

   pip install -e ".[mcp]"
   tspec mcp --transport stdio --workdir .

マニュアル: ``tspec manual show mcp-env --full``

TSPEC-Z1 圧縮（AI引き渡し用）
----------------------------------------
CLI:

.. code-block:: bash

   tspec z1-decode docs/selenium_spec.tspecz1 --format text
   tspec z1-decode docs/selenium_spec.tspecz1 --format json
   tspec z1-decompile docs/selenium_spec.tspecz1 --format text
   tspec z1-decompile docs/selenium_spec.tspecz1 --format yaml

Pytest reporting (pytest / pytest-html)
----------------------------------------
Install:

.. code-block:: bash

   uv pip install -e ".[report]"

Generate during run:

.. code-block:: bash

   tspec run examples/android_login.tspec.md --backend appium --report out/android.json --pytest-html out/android.html --pytest-junitxml out/android.xml

Generate from existing JSON:

.. code-block:: bash

   tspec pytest-report out/android.json --html out/android.html

Update helper (PowerShell)
----------------------------------------
.. code-block:: powershell

   # extract the update script from installed package (optional)
   tspec asset update.ps1 --to .

   # apply a downloaded zip into current repo
   .\scripts\update.ps1 -ZipPath "$HOME\Downloads\tspec-runner-<version>.zip" -RepoDir .
