from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class Check:
    name: str
    ok: bool
    detail: str

def _which(cmd: str) -> Optional[str]:
    return shutil.which(cmd)

def check_selenium_env() -> list[Check]:
    checks: list[Check] = []

    # python module
    try:
        import selenium  # noqa: F401
        checks.append(Check("python: selenium", True, "import ok"))
    except Exception as e:
        checks.append(Check("python: selenium", False, f"import failed: {e} (install: pip install -e '.[selenium]')"))

    # drivers
    chromedriver = _which("chromedriver")
    checks.append(Check("chromedriver", bool(chromedriver), chromedriver or "not found in PATH"))
    geckodriver = _which("geckodriver")
    checks.append(Check("geckodriver", bool(geckodriver), geckodriver or "not found in PATH (optional)"))

    # browsers (best-effort; varies by OS)
    chrome = _which("google-chrome") or _which("chrome")
    checks.append(Check("chrome", bool(chrome), chrome or "not found in PATH (macOS app may still exist)"))
    firefox = _which("firefox")
    checks.append(Check("firefox", bool(firefox), firefox or "not found in PATH (optional)"))

    # versions (best-effort)
    if chromedriver:
        try:
            out = subprocess.check_output([chromedriver, "--version"], text=True, stderr=subprocess.STDOUT).strip()
            checks.append(Check("chromedriver --version", True, out))
        except Exception as e:
            checks.append(Check("chromedriver --version", False, str(e)))
    return checks
