# Core TestCases
JP: コア機能テストケース

## Preconditions
- `pip install -e ".[dev]"`
JP: 開発用 extras が必要

## TestCases

### TC-CORE-001: validate
- Goal: validate a spec
- Steps: `tspec validate examples/assert_only.tspec.md`
- Expected: `OK`
JP: validate の基本動作

### TC-CORE-002: run + report
- Goal: run a spec and read report
- Steps:
  - `tspec run examples/assert_only.tspec.md --report out/report.json`
  - `tspec report out/report.json --only-errors --show-steps`
- Expected: report renders
JP: run と report の基本動作

### TC-NEKO-003: bearer auth
- Goal: bearer header is set
- Steps: run Neko client test
- Expected: Authorization header is `Bearer <token>`
JP: bearer 認証が Authorization ヘッダに反映される


## JP (original)
# Core TestCase 仕様

目的: tspec-runner のコア機能とオプション機能（Neko/Manual）の動作確認を行う。

## Unit Test Cases
- TC-CORE-001: manual id 指定で正しいマニュアルが取得できる
- TC-CORE-002: manual tag 指定で正しいマニュアルが取得できる
- TC-CORE-003: manual path key 指定で正しいマニュアルが取得できる
- TC-CORE-004: agent-browser backend を指定できる（alias も含む）
- TC-NEKO-001: Neko base_url 未指定で ValidationError
- TC-NEKO-002: allowlist に無い host が ValidationError
- TC-NEKO-003: bearer 認証が Authorization ヘッダに反映される

## Manual / Integration (optional)
- TC-CORE-005: `tspec manual show android --full` が android-env を表示する

## 設定/手順まとめ
- unit: `pytest -q`
- manual: `tspec manual show <id> --full`
