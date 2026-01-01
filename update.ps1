git switch -c upgrade/0.3.0a4-post3

Expand-Archive -Force -Path "$HOME\Downloads\tspec-runner-0.3.0a4.post3-with-updateps1.zip" -DestinationPath "."

git add -A
git commit -m "fix: versions appium status uses urllib (no requests)"
git tag v0.3.0a4.post3

uv pip install -e ".[dev]"

clear
tspec versions