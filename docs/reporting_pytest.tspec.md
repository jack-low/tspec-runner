# pytest reporting manual
JP: pytest レポート生成マニュアル

```tspec
manual:
  id: reporting-pytest
  title: 'pytest report generation / JP: Pytest / pytest-html レポート出力'
  tags:
  - report
  - pytest
  - html
  - junit
  summary: 'EN: Convert tspec JSON reports into pytest-html / junitxml.

    JP: tspec の JSON レポートを pytest-html / junitxml に変換する。

    '
  prerequisites:
  - pip install -e '.[report]'
  - 'JP: uv pip install -e ''.[report]'''
  steps:
  - title: '1) Run a spec with JSON report / JP: Run と同時に HTML を生成'
    body: 'tspec run examples/assert_only.tspec.md --report out/report.json


      JP:

      tspec run <spec> --report out/report.json --pytest-html out/report.html'
  - title: '2) Generate pytest-html / junitxml / JP: 既存 JSON から HTML を生成'
    body: 'tspec report out/report.json --only-errors --show-steps

      tspec pytest-report out/report.json --html out/report.html

      tspec pytest-report out/report.json --junitxml out/report.xml


      JP:

      tspec pytest-report out/report.json --html out/report.html'
  - title: 'JP: CI向け junitxml'
    body: tspec run <spec> --report out/report.json --pytest-junitxml out/report.xml
  troubleshooting:
  - title: 'JP: pytest-html が無い'
    body: 'extras が未導入: uv pip install -e ".[report]"'
```