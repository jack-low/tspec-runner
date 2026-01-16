import pytest

httpx = pytest.importorskip("httpx")

from tspec.unity_client import UnityAuth, UnityClient, UnityMcpHttpClient
from tspec.errors import ValidationError


def test_unity_base_url_required():
    with pytest.raises(ValidationError):
        UnityClient(base_url="")


def test_unity_allowlist_blocks():
    with pytest.raises(ValidationError):
        UnityClient(base_url="http://example.com:8080", allowlist_hosts=["localhost:8080"])


def test_unity_request_auth_bearer_header():
    seen = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["auth"] = request.headers.get("Authorization")
        return httpx.Response(200, json={"ok": True})

    transport = httpx.MockTransport(handler)
    auth = UnityAuth(mode="bearer", bearer_token="TESTTOKEN")
    c = UnityClient(base_url="http://localhost:8080", auth=auth, allowlist_hosts=["localhost:8080"])
    c._client = httpx.Client(base_url="http://localhost:8080", transport=transport)  # type: ignore[attr-defined]
    out = c.get_json("/health")
    assert out["ok"] is True
    assert seen["auth"] == "Bearer TESTTOKEN"


def test_unity_mcp_url_required():
    with pytest.raises(ValidationError):
        UnityMcpHttpClient(mcp_url="")


def test_unity_mcp_allowlist_blocks():
    with pytest.raises(ValidationError):
        UnityMcpHttpClient(mcp_url="http://example.com:8080/mcp", allowlist_hosts=["localhost:8080"])
