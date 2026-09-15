$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $PSScriptRoot
$GitExe = "C:\Program Files\Git\cmd\git.exe"
$GitName = "romeoxt"
$GitEmail = "herbylegall9@gmail.com"
$HookSource = Join-Path $Root "scripts/prepare-commit-msg"

function Invoke-Git {
    param([string[]]$GitArgs)
    & $GitExe @GitArgs
    if ($LASTEXITCODE -ne 0) {
        throw "git $($GitArgs -join ' ') failed with exit code $LASTEXITCODE"
    }
}

Set-Location $Root

$env:GIT_AUTHOR_NAME = $GitName
$env:GIT_AUTHOR_EMAIL = $GitEmail
$env:GIT_COMMITTER_NAME = $GitName
$env:GIT_COMMITTER_EMAIL = $GitEmail

Invoke-Git @("config", "user.name", $GitName) | Out-Null
Invoke-Git @("config", "user.email", $GitEmail) | Out-Null

New-Item -ItemType Directory -Force -Path ".git/hooks" | Out-Null
Copy-Item $HookSource ".git/hooks/prepare-commit-msg" -Force

Invoke-Git @("checkout", "--orphan", "clean-master") | Out-Null
Invoke-Git @("add", "-A") | Out-Null

$CommitMessagePath = Join-Path $env:TEMP "railway-templates-rewrite-message.txt"
[System.IO.File]::WriteAllText($CommitMessagePath, "Railway template collection by romeoxt")

$tree = (Invoke-Git @("write-tree")).Trim()
$commit = (Invoke-Git @("commit-tree", $tree, "-F", $CommitMessagePath)).Trim()
Invoke-Git @("reset", "--hard", $commit) | Out-Null
Remove-Item $CommitMessagePath -Force

$log = (Invoke-Git @("log", "-1", "--format=%B")).Trim()
if ($log -match "cursoragent|Co-authored-by:\s*Cursor") {
    throw "Commit still contains Cursor attribution"
}

Invoke-Git @("branch", "-D", "master") 2>$null
Invoke-Git @("branch", "-m", "master") | Out-Null
Invoke-Git @("push", "--force", "origin", "master") | Out-Null

Write-Output "Rewrote romeoxt/railway-templates to a single clean commit by $GitName <$GitEmail>"
