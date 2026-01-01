from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from ..errors import ExecutionError
from .base import UIDriver, UISettings

@dataclass
class SeleniumSettings:
    browser: str = "chrome"  # chrome|firefox

class SeleniumUIDriver(UIDriver):
    def __init__(self, ui: UISettings, selenium: SeleniumSettings):
        try:
            from selenium import webdriver  # noqa: F401
            from selenium.webdriver.common.by import By  # noqa: F401
        except Exception as e:
            raise ExecutionError(
                "Selenium backend selected but selenium is not installed. "
                "Install with: pip install -e '.[selenium]'"
            ) from e

        from selenium import webdriver
        self.By = __import__("selenium.webdriver.common.by", fromlist=["By"]).By  # type: ignore

        browser = (selenium.browser or "chrome").lower()
        if browser == "chrome":
            from selenium.webdriver.chrome.options import Options
            opts = Options()
            if ui.headless:
                opts.add_argument("--headless=new")
            self.driver = webdriver.Chrome(options=opts)
        elif browser == "firefox":
            from selenium.webdriver.firefox.options import Options
            opts = Options()
            if ui.headless:
                opts.add_argument("-headless")
            self.driver = webdriver.Firefox(options=opts)
        else:
            raise ExecutionError(f"Unsupported selenium browser: {selenium.browser!r}")

        if ui.implicit_wait_ms and ui.implicit_wait_ms > 0:
            self.driver.implicitly_wait(ui.implicit_wait_ms / 1000.0)

    def open(self, url: str) -> None:
        self.driver.get(url)

    def open_app(self, server_url: str, caps: dict) -> None:
        raise ExecutionError("open_app is not supported on selenium backend. Use appium backend.")

    def click(self, selector: str) -> None:
        el = self.driver.find_element(self.By.CSS_SELECTOR, selector)
        el.click()

    def type(self, selector: str, text: str) -> None:
        el = self.driver.find_element(self.By.CSS_SELECTOR, selector)
        el.clear()
        el.send_keys(text)

    def wait_for(self, selector: str, text_contains: Optional[str], timeout_ms: int) -> None:
        try:
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
        except Exception as e:
            raise ExecutionError("Selenium support modules missing.") from e

        wait = WebDriverWait(self.driver, timeout_ms / 1000.0)
        if text_contains is None:
            wait.until(EC.presence_of_element_located((self.By.CSS_SELECTOR, selector)))
        else:
            wait.until(EC.text_to_be_present_in_element((self.By.CSS_SELECTOR, selector), text_contains))

    def get_text(self, selector: str) -> str:
        # Special case: 'title' selector returns document title (useful in demos)
        if selector.strip().lower() == "title":
            return self.driver.title
        el = self.driver.find_element(self.By.CSS_SELECTOR, selector)
        return el.text

    def screenshot(self, path: str) -> None:
        self.driver.save_screenshot(path)

    def close(self) -> None:
        try:
            self.driver.quit()
        except Exception:
            pass
