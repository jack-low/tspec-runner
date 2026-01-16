import pytest

httpx = pytest.importorskip("httpx")

from tspec.blender_client import BlenderAuth, BlenderClient
from tspec.errors import ValidationError


def test_blender_base_url_required():
    with pytest.raises(ValidationError):
        BlenderClient(base_url="")


def test_blender_allowlist_blocks():
    with pytest.raises(ValidationError):
        BlenderClient(base_url="http://example.com:8080", allowlist_hosts=["localhost:8080"])


def test_blender_request_auth_bearer_header():
    seen = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["auth"] = request.headers.get("Authorization")
        return httpx.Response(200, json={"ok": True})

    transport = httpx.MockTransport(handler)
    auth = BlenderAuth(mode="bearer", bearer_token="TESTTOKEN")
    c = BlenderClient(base_url="http://localhost:8080", auth=auth, allowlist_hosts=["localhost:8080"])
    c._client = httpx.Client(base_url="http://localhost:8080", transport=transport)  # type: ignore[attr-defined]
    out = c.get_json("/health")
    assert out["ok"] is True
    assert seen["auth"] == "Bearer TESTTOKEN"
