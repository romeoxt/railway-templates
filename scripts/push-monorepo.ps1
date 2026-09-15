$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $PSScriptRoot
$GitName = "romeoxt"
$GitEmail = "herbylegall9@gmail.com"

Set-Location $Root
git config user.name $GitName
git config user.email $GitEmail
git config commit.gpgsign false

$env:GIT_AUTHOR_NAME = $GitName
$env:GIT_AUTHOR_EMAIL = $GitEmail
$env:GIT_COMMITTER_NAME = $GitName
$env:GIT_COMMITTER_EMAIL = $GitEmail

$CommitMessagePath = Join-Path $env:TEMP "railway-templates-commit-message.txt"
$Message = if ($args.Count -gt 0) { $args[0] } else { "Railway template collection with plain READMEs and deploy configs" }
[System.IO.File]::WriteAllText($CommitMessagePath, $Message)

git add -A
$Status = git status --porcelain
if ($Status) {
    git commit --no-verify -F $CommitMessagePath
} else {
    Write-Output "No changes to commit."
}

Remove-Item $CommitMessagePath -Force -ErrorAction SilentlyContinue
git push origin master

Write-Output "Pushed romeoxt/railway-templates"
