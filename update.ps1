git switch -c upgrade/pytest-reporting-fix

# zip 展開（パスは置き場所に合わせて）
Expand-Archive -Force -Path "$HOME\Downloads\tspec-runner-0.3.0a4-log-analyze-versions.zip" -DestinationPath "."

.venv\Scripts\activate
uv pip install -e ".[dev]"

git add -A
git commit -m "fix: cli syntax + pytest-html reporting (0.3.0a3.post1)"
git tag v0.3.0a3.post1
