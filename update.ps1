git switch -c upgrade/0.3.0a4-post1

# zip展開（場所は適宜）
Expand-Archive -Force -Path "$HOME\Downloads\tspec-runner-0.3.0a4.post1-log-analyze-versions.zip" -DestinationPath "."

git add -A
git commit -m "fix: versions command imports __version__"
git tag v0.3.0a4.post1
