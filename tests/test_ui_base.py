import pytest

from tspec.ui.base import ensure_supported_backend
from tspec.errors import ExecutionError


def test_agent_browser_backend_supported():
    assert ensure_supported_backend("agent-browser") == "agent-browser"
    assert ensure_supported_backend("agent_browser") == "agent-browser"


def test_unknown_backend_rejected():
    with pytest.raises(ExecutionError):
        ensure_supported_backend("unknown-backend")
