$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $PSScriptRoot
$StagingRoot = Join-Path $env:TEMP "railway-template-repos"
$GitExe = "C:\Program Files\Git\cmd\git.exe"
$GitHubUser = "romeoxt"
$GitName = "romeoxt"
$GitEmail = "herbylegall9@gmail.com"
$HookSource = Join-Path $Root "scripts/prepare-commit-msg"

$Templates = @(
    @{ Folder = "fastapi-postgres"; Repo = "railway-template-fastapi-postgres" },
    @{ Folder = "hono-postgres"; Repo = "railway-template-hono-postgres" },
    @{ Folder = "openai-chat-api"; Repo = "railway-template-openai-chat-api" },
    @{ Folder = "ai-agent-api"; Repo = "railway-template-ai-agent-api" },
    @{ Folder = "rag-pgvector"; Repo = "railway-template-rag-pgvector" },
    @{ Folder = "simple-analytics"; Repo = "railway-template-simple-analytics" },
    @{ Folder = "personal-blog"; Repo = "railway-template-personal-blog" },
    @{ Folder = "postgres-pgweb"; Repo = "railway-template-postgres-pgweb" },
    @{ Folder = "umami-analytics"; Repo = "railway-template-umami-analytics" }
)

function Invoke-Git {
    param([string[]]$GitArgs)
    & $GitExe @GitArgs
    if ($LASTEXITCODE -ne 0) {
        throw "git $($GitArgs -join ' ') failed with exit code $LASTEXITCODE"
    }
}

function New-CleanCommit {
    param([string]$MessagePath)

    $tree = (Invoke-Git @("write-tree")).Trim()
    $commit = (Invoke-Git @("commit-tree", $tree, "-F", $MessagePath)).Trim()
    Invoke-Git @("reset", "--hard", $commit) | Out-Null
    $log = (Invoke-Git @("log", "-1", "--format=%B")).Trim()
    if ($log -match "cursoragent|Co-authored-by:\s*Cursor") {
        throw "Commit still contains Cursor attribution: $log"
    }
}

New-Item -ItemType Directory -Force -Path $StagingRoot | Out-Null

$Results = @()

foreach ($Template in $Templates) {
    $Source = Join-Path (Join-Path $Root "templates") $Template.Folder
    $Target = Join-Path $StagingRoot $Template.Repo
    $FullRepo = "$GitHubUser/$($Template.Repo)"

    if (Test-Path $Target) {
        Remove-Item $Target -Recurse -Force
    }

    New-Item -ItemType Directory -Force -Path $Target | Out-Null
    robocopy $Source $Target /E /XD node_modules dist .venv __pycache__ .git /XF package-lock.json | Out-Null

    Copy-Item (Join-Path $Root "LICENSE") $Target -Force
    Copy-Item (Join-Path $Root "AUTHOR") $Target -Force
    Copy-Item (Join-Path $Root ".gitignore") $Target -Force

    Push-Location $Target

    $env:GIT_AUTHOR_NAME = $GitName
    $env:GIT_AUTHOR_EMAIL = $GitEmail
    $env:GIT_COMMITTER_NAME = $GitName
    $env:GIT_COMMITTER_EMAIL = $GitEmail

    Invoke-Git @("init", "-b", "main") | Out-Null
    Invoke-Git @("config", "user.name", $GitName) | Out-Null
    Invoke-Git @("config", "user.email", $GitEmail) | Out-Null
    Invoke-Git @("config", "commit.gpgsign", "false") | Out-Null

    New-Item -ItemType Directory -Force -Path ".git/hooks" | Out-Null
    Copy-Item $HookSource ".git/hooks/prepare-commit-msg" -Force

    $CommitMessagePath = Join-Path $env:TEMP "$($Template.Repo)-commit-message.txt"
    [System.IO.File]::WriteAllText($CommitMessagePath, "Initial release by romeoxt")

    Invoke-Git @("add", ".") | Out-Null
    New-CleanCommit -MessagePath $CommitMessagePath
    Remove-Item $CommitMessagePath -Force

    $PreviousErrorAction = $ErrorActionPreference
    $ErrorActionPreference = "SilentlyContinue"
    gh repo view $FullRepo --json name 2>$null | Out-Null
    $RepoExists = $LASTEXITCODE -eq 0
    $ErrorActionPreference = $PreviousErrorAction

    if (-not $RepoExists) {
        gh repo create $FullRepo --public --source=. --remote=origin --push
        if ($LASTEXITCODE -ne 0) { throw "Failed to create $FullRepo" }
    } else {
        $PreviousErrorAction = $ErrorActionPreference
        $ErrorActionPreference = "SilentlyContinue"
        & $GitExe remote remove origin 2>$null | Out-Null
        $ErrorActionPreference = $PreviousErrorAction
        Invoke-Git @("remote", "add", "origin", "https://github.com/$FullRepo.git")
        Invoke-Git @("push", "-u", "origin", "main", "--force")
    }

    $Url = "https://github.com/$FullRepo"
    $Results += [PSCustomObject]@{ Template = $Template.Folder; Repo = $FullRepo; Url = $Url }
    Pop-Location
}

$Results | Format-Table -AutoSize
$Results | ConvertTo-Json | Set-Content (Join-Path $Root "published-repos.json")
