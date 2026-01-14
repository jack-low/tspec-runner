from tspec.ui.agent_browser_driver import _windows_path_to_wsl


def test_windows_path_to_wsl_absolute():
    path = r"C:\WorkSpace\Private\Python\tspec-runner\out\shot.png"
    assert _windows_path_to_wsl(path) == "/mnt/c/WorkSpace/Private/Python/tspec-runner/out/shot.png"


def test_windows_path_to_wsl_relative():
    path = r"artifacts\agent-browser\shot.png"
    assert _windows_path_to_wsl(path) == path
