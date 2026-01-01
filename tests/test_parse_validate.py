from pathlib import Path
from tspec.validate import load_and_validate

def test_assert_example_validates():
    doc, spec = load_and_validate(Path("examples/assert_only.tspec.md"))
    assert doc.suite.name == "assert-only"
    assert str(spec.resolved) == "0.1.0"
