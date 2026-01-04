# tspec-runner 0.3.0a2

TSpec（Markdown + ```tspec）を読み込み、CLI から自動実行する runner です。

## できること（この版）
- Spec バージョン解決（無指定＝最新 / 範囲指定 / 3世代前まで）
- validate / list / run / spec / init / doctor
- `assert.*` 実装
- **UI 自動化インターフェース（統一 API）**を実装：`ui.*`
  - backend: `selenium` / `appium`(Android/iOS) / `pywinauto`
  - 依存は extras で追加（軽いコア）

> Android/iOS は Appium を前提にしています（Appium Server + driver は別途セットアップ）。

---

## 開発環境
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -U pip
pip install -e ".[dev]"
```

## UI backend を使う場合（extras）
### Selenium
```bash
pip install -e ".[selenium]"
```

### Appium（Android/iOS）
```bash
pip install -e ".[appium]"
```

### pywinauto（Windows GUI）
```bash
pip install -e ".[pywinauto]"
```

---

## 使い方
```bash
tspec spec
tspec init example.tspec.md
tspec validate examples/assert_only.tspec.md --explain-version
tspec run examples/assert_only.tspec.md --report out/report.json
```

### UI 実行（例：Selenium）
```bash
tspec run examples/selenium_google.tspec.md --backend selenium --report out/ui.json
```

---

## 設定（任意）: tspec.toml
`--config tspec.toml` で読み込みます。最小例：

```toml
[ui]
backend = "selenium"  # selenium|appium|pywinauto
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
```

---

## 実装している `ui.*`
- `ui.open` with `{url}` （Seleniumのみ）
- `ui.open_app` with `{caps, server_url}` （Appium）
- `ui.click` with `{selector}`
- `ui.type` with `{selector, text}`
- `ui.wait_for` with `{selector, text_contains?}`
- `ui.get_text` with `{selector}` + `save: "name"`
- `ui.screenshot` with `{path}`
- `ui.close`

> selector は backend ごとに解釈されます（Seleniumは CSS を基本、`css=`/`xpath=`/`id=`/`name=`/`link=` などのprefixも可）。

作成日: 2025-12-30


## レポート表示（画面で解析しやすくする）
実行時に `--report` で出力した JSON を、テーブルで見やすく表示できます。

```bash
tspec report out/report.json
tspec report out/report.json --only-errors --show-steps
tspec report out/report.json --case UI-001 --show-steps
tspec report out/report.json --grep google --status failed --status error
```


### メッセージが長い場合（Stacktrace等）
既定では `Stacktrace:` 以降を省略し、表示を短くします。

```bash
tspec report out/report.json --only-errors --show-steps
tspec report out/report.json --only-errors --show-steps --full-trace --max-message-len 0
```


## 失敗時の鑑識セット（自動採取）
- `ui.wait_for` が失敗すると、既定で以下を `artifacts/forensics/` に保存します：
  - screenshot（PNG）
  - current_url（メッセージに表示）
  - page_source（HTML, Seleniumのみ）
メッセージに保存パスが出るので、そのまま追跡できます。


### Appium-Python-Client v4+ について
- v4+ は `desired_capabilities` を受け付けず、Options API を使います。
- 本 runner は `caps:` を dict のまま受け取り、内部で `AppiumOptions.load_capabilities()` に変換します。


## 環境構築マニュアル（編集可能 / tspec形式）
マニュアルは `docs/*.tspec.md` として管理し、CLI から表示できます。

```bash
tspec manual list
tspec manual show android-env --full
tspec doctor --android
```


### Selenium マニュアル
```bash
tspec manual show selenium-env --full
tspec doctor --selenium
```


### iOS マニュアル
```bash
tspec manual show ios-env --full
tspec doctor --ios
```

### TSPEC-Z1 圧縮マニュアル
```bash
tspec manual show tspec-z1 --full
```


## MCP (AI連携)
MCP Server として起動し、AIクライアントから TSpec をツール呼び出しできます。

```bash
pip install -e ".[mcp]"
tspectest="tspec mcp --transport stdio --workdir ."
$tspectest
```

マニュアル: `tspec manual show mcp-env --full`


## TSPEC-Z1 圧縮（AI引き渡し用）
AIに渡す仕様を、独自形式で短くまとめるための圧縮形式です。

アルゴリズム（復元ルール）:
- 先頭に `Z1|` を置く
- `D{...}`: 辞書。`key=value` を `;` 区切り
- `P{...}`: ペイロード。`|` 区切りでセクション、各セクションは `TAG:...`
- `@k` は辞書参照（`k` は辞書キー）
- `#` はファイルパス、`!` は動作要件、`+` は追加/変更点、`=` は値
- 文字列中の `|` と `}` は `\|` と `\}` でエスケープ

拡張子は `*.tspecz1` を推奨。

CLI:
```bash
tspec z1-decode docs/selenium_spec.tspecz1 --format text
tspec z1-decode docs/selenium_spec.tspecz1 --format json
tspec z1-decompile docs/selenium_spec.tspecz1 --format text
tspec z1-decompile docs/selenium_spec.tspecz1 --format yaml
```

Python API:
```python
from pathlib import Path
from tspec.tspec_z1 import decode_z1_file, decompile_z1_file

doc = decode_z1_file(Path("docs/selenium_spec.tspecz1"))
text = decompile_z1_file(Path("docs/selenium_spec.tspecz1"))
```


## Live monitoring / robust error handling (0.3.0a2)

`tspec run` can now emit *live* step progress logs and enforce a runner-side hard timeout per step
(useful when a backend call blocks until its own timeout).

```bash
tspec run examples/android_youtube_search_play.tspec.md --backend appium --watch --step-timeout-ms 60000 --on-error abort
```

Per-step policies (optional):

- `timeout_ms`: hard timeout (ms)
- `retry`: `{ max, backoff_ms }`
- `on_error`: `{ action: abort|skip_case|continue, note }`


## Pytest reporting (pytest / pytest-html)
Legacy JSON report remains the default. When requested and available, pytest-based reports can be generated from the JSON without rerunning UI actions.

Install:
```bash
uv pip install -e ".[report]"
```

Generate during run:
```bash
tspec run examples/android_login.tspec.md --backend appium --report out/android.json --pytest-html out/android.html --pytest-junitxml out/android.xml
```

Generate from existing JSON:
```bash
tspec pytest-report out/android.json --html out/android.html
```


## Update helper (PowerShell)
同梱の `scripts/update.ps1` は、配布zipを安全に取り込むための補助スクリプトです。

```powershell
# list bundled assets
# tspec asset list

# extract the update script from installed package (optional)
tspectool="tspec asset update.ps1 --to ."
$tspectool

# apply a downloaded zip into current repo
.\scripts\update.ps1 -ZipPath "$HOME\Downloads\tspec-runner-<version>.zip" -RepoDir .
```
