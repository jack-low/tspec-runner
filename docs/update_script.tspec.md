# update.ps1 manual
JP: update.ps1 マニュアル

```tspec
manual:
  id: update-script
  title: 'PowerShell update.ps1 usage / JP: 更新取り込み（PowerShell update.ps1）'
  tags:
  - update
  - powershell
  - git
  summary: 'EN: Use update.ps1 to update the repo from a zip or local path.

    JP: update.ps1 を使って zip などからリポジトリを更新する。

    '
  prerequisites:
  - Windows PowerShell / PowerShell 7
  - git
  - 'JP: Windows PowerShell / PowerShell 7'
  - 'JP: git が利用可能'
  steps:
  - title: '1) Use update.ps1 in repo / JP: 1) update.ps1 を使う（repo直下で）'
    body: '.\scripts\update.ps1 -ZipPath "$HOME\Downloads\tspec-runner-<version>.zip"
      -RepoDir .


      JP:

      .\scripts\update.ps1 -ZipPath "$HOME\Downloads\tspec-runner-<version>.zip" -RepoDir
      .'
  - title: '2) Choose ZipPath / JP: 2) ZipPath 省略（Downloadsから最新を自動選択）'
    body: '.\scripts\update.ps1 -RepoDir .


      JP:

      .\scripts\update.ps1 -RepoDir .'
  - title: '3) Refresh install / JP: 3) install版から取り出す（任意）'
    body: 'tspec asset list

      tspec asset update.ps1 --to .


      JP:

      tspec asset list

      tspec asset update.ps1 --to .'
  troubleshooting:
  - title: 'not a git repository / JP: not a git repository'
    body: 'EN: run git init / commit first.

      JP: git init / commit を先に行う。'
```