import pytest

httpx = pytest.importorskip("httpx")

from tspec.neko_client import NekoClient, NekoAuth
from tspec.errors import ValidationError, ExecutionError


def test_neko_base_url_required():
    with pytest.raises(ValidationError):
        NekoClient(base_url="")


def test_neko_allowlist_blocks():
    with pytest.raises(ValidationError):
        NekoClient(base_url="http://example.com:8080", allowlist_hosts=["localhost:8080"])


def test_neko_request_auth_bearer_header():
    # ensure bearer header is applied and request is made
    seen = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["auth"] = request.headers.get("Authorization")
        return httpx.Response(200, json={"ok": True})

    transport = httpx.MockTransport(handler)
    auth = NekoAuth(mode="bearer", bearer_token="TESTTOKEN")
    c = NekoClient(base_url="http://localhost:8080", auth=auth, allowlist_hosts=["localhost:8080"])
    # monkeypatch internal client transport
    c._client = httpx.Client(base_url="http://localhost:8080", transport=transport)  # type: ignore[attr-defined]
    out = c.get_json("/api/stats")
    assert out["ok"] is True
    assert seen["auth"] == "Bearer TESTTOKEN"
