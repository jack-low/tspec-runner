from pathlib import Path

import pytest

from tspec.errors import ValidationError
from tspec.manual_loader import find_manual_by_id


def _write_manual(path: Path, manual_id: str, tags: list[str], title: str | None = None) -> None:
    manual_title = title or f"Manual {manual_id}"
    content = f"""# Manual

```tspec
manual:
  id: {manual_id}
  title: "{manual_title}"
  tags: [{", ".join(tags)}]
  summary: |
    Test manual.
  steps:
    - title: "Step"
      body: |
        Do it.
```
"""
    path.write_text(content, encoding="utf-8")


def test_find_manual_by_id_matches_tag(tmp_path: Path) -> None:
    base = tmp_path / "docs"
    base.mkdir()
    _write_manual(base / "android_env.tspec.md", "android-env", ["android", "setup"])

    _path, mf = find_manual_by_id(base, "android")
    assert mf.manual.id == "android-env"


def test_find_manual_by_id_matches_path_key(tmp_path: Path) -> None:
    base = tmp_path / "docs"
    base.mkdir()
    _write_manual(base / "sample_env.tspec.md", "manual-x", ["misc"])

    _path, mf = find_manual_by_id(base, "sample_env")
    assert mf.manual.id == "manual-x"


def test_find_manual_by_id_ambiguous_tag_raises(tmp_path: Path) -> None:
    base = tmp_path / "docs"
    base.mkdir()
    _write_manual(base / "a.tspec.md", "a", ["shared"])
    _write_manual(base / "b.tspec.md", "b", ["shared"])

    with pytest.raises(ValidationError, match="tag/path matches"):
        find_manual_by_id(base, "shared")


def test_find_manual_by_id_prefers_en_when_multiple_langs(tmp_path: Path) -> None:
    base = tmp_path / "docs"
    base.mkdir()
    _write_manual(base / "android_env.en.tspec.md", "android-env", ["android"], title="Manual EN")
    _write_manual(base / "android_env.jp.tspec.md", "android-env", ["android"], title="Manual JP")

    path, mf = find_manual_by_id(base, "android-env")
    assert path.name.endswith(".en.tspec.md")
    assert mf.manual.title == "Manual EN"


def test_find_manual_by_id_lang_filter(tmp_path: Path) -> None:
    base = tmp_path / "docs"
    base.mkdir()
    _write_manual(base / "android_env.en.tspec.md", "android-env", ["android"], title="Manual EN")
    _write_manual(base / "android_env.jp.tspec.md", "android-env", ["android"], title="Manual JP")

    path, mf = find_manual_by_id(base, "android-env", lang="jp")
    assert path.name.endswith(".jp.tspec.md")
    assert mf.manual.title == "Manual JP"
