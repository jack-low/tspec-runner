import pytest

from tspec.ui.selenium_utils import extract_major_version, parse_selector, parse_window_size


def test_parse_selector_prefixes():
    assert parse_selector("css=.btn") == ("css selector", ".btn")
    assert parse_selector("xpath=//div") == ("xpath", "//div")
    assert parse_selector("id=login") == ("id", "login")


def test_parse_selector_default_css():
    assert parse_selector(".card") == ("css selector", ".card")


def test_parse_window_size():
    assert parse_window_size("1280x720") == (1280, 720)
    assert parse_window_size("1280,720") == (1280, 720)


def test_parse_window_size_invalid():
    with pytest.raises(ValueError):
        parse_window_size("bad")


def test_extract_major_version():
    assert extract_major_version("ChromeDriver 114.0.5735.90") == 114
    assert extract_major_version("Google Chrome 124.0.6367.208") == 124
    assert extract_major_version("unknown") is None
