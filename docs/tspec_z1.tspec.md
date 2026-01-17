# TSPEC-Z1 manual
JP: TSPEC-Z1 マニュアル

```tspec
manual:
  id: tspec-z1
  title: 'TSPEC-Z1 usage / JP: TSPEC-Z1 圧縮形式（AI引き渡し用）'
  tags:
  - tspec
  - z1
  - decode
  - decompile
  summary: 'EN: Decode/decompile TSPEC-Z1 files for AI handoff.

    JP: TSPEC-Z1 をデコード/デコンパイルして AI への引き渡しに使う。

    '
  prerequisites:
  - tspec-runner installed
  steps:
  - title: '1) Decode / JP: 1) 先頭に Z1| を付与'
    body: "tspec z1-decode docs/selenium_spec.tspecz1 --format text\ntspec z1-decode\
      \ docs/selenium_spec.tspecz1 --format json\n\nJP:\n例:\n  Z1|..."
  - title: '2) Decompile / JP: 2) 辞書 D{...}'
    body: "tspec z1-decompile docs/selenium_spec.tspecz1 --format text\ntspec z1-decompile\
      \ docs/selenium_spec.tspecz1 --format yaml\n\nJP:\nkey=value を ; 区切りで列挙する。\n\
      例:\n  D{p=path;sc=scope;ch=change}"
  - title: 'JP: 3) ペイロード P{...}'
    body: "| 区切りでセクションを分割し、各セクションは TAG:... 形式。\n例:\n  P{SCOPE:...|FILES:...|CHANGES:...}"
  - title: 'JP: 4) 辞書参照'
    body: "@k は辞書参照（k は辞書キー）。\n例:\n  SCOPE:@sc=@se"
  - title: 'JP: 5) 記号の意味'
    body: '# はファイルパス、! は動作要件、+ は追加/変更点、= は値。'
  - title: 'JP: 6) エスケープ'
    body: '| と } は \| と \} にエスケープする。'
  - title: 'JP: 7) CLI で decode'
    body: "構造化データに変換:\n  tspec z1-decode docs/selenium_spec.tspecz1 --format text\n\
      \  tspec z1-decode docs/selenium_spec.tspecz1 --format json\n  tspec z1-decode\
      \ docs/selenium_spec.tspecz1 --format yaml"
  - title: 'JP: 8) CLI で decompile'
    body: "人間可読な展開テキストに変換:\n  tspec z1-decompile docs/selenium_spec.tspecz1 --format\
      \ text\n  tspec z1-decompile docs/selenium_spec.tspecz1 --format json\n  tspec\
      \ z1-decompile docs/selenium_spec.tspecz1 --format yaml"
  references:
  - README.md の TSPEC-Z1 圧縮（AI引き渡し用）
```