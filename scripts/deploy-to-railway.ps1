$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $PSScriptRoot
$WorkspaceId = "28e6f57d-85df-4589-9536-b1c99a8081f5"
$StagingRoot = Join-Path $env:TEMP "railway-deploy-projects"

function New-RailwayProject {
    param([string]$Name)

    $ProjectDir = Join-Path $StagingRoot $Name
    New-Item -ItemType Directory -Force -Path $ProjectDir | Out-Null
    Push-Location $ProjectDir

    $Json = railway init -n $Name -w $WorkspaceId --json | ConvertFrom-Json
    Pop-Location
    return [PSCustomObject]@{ Id = $Json.id; Name = $Name; Dir = $ProjectDir }
}

function Add-RailwayService {
    param([string]$ProjectDir, [string]$ServiceName)

    Push-Location $ProjectDir
    $Json = railway add -s $ServiceName --json | ConvertFrom-Json
    Pop-Location
    return $Json.name
}

function Add-RailwayPostgres {
    param([string]$ProjectDir)

    Push-Location $ProjectDir
    railway add -d postgres -s "Postgres" --json | Out-Null
    Pop-Location
}

function Deploy-Template {
    param(
        [string]$ProjectName,
        [string]$ServiceName,
        [string]$TemplatePath,
        [hashtable]$Variables,
        [switch]$WithPostgres
    )

    Write-Output "`n=== Deploying $ProjectName ==="
    $Project = New-RailwayProject -Name $ProjectName

    if ($WithPostgres) {
        Add-RailwayPostgres -ProjectDir $Project.Dir
    }

    Add-RailwayService -ProjectDir $Project.Dir -ServiceName $ServiceName | Out-Null

    Push-Location $TemplatePath
    railway link -p $Project.Id -s $ServiceName -w $WorkspaceId | Out-Null

    foreach ($Key in $Variables.Keys) {
        railway variable set "$Key=$($Variables[$Key])" --skip-deploys | Out-Null
    }

    railway up -d | Out-Null
    railway domain -s $ServiceName | Out-Null
    Pop-Location

    return [PSCustomObject]@{
        Project = $ProjectName
        ProjectId = $Project.Id
        Service = $ServiceName
        Dashboard = "https://railway.com/project/$($Project.Id)"
    }
}

function New-ApiKey {
    return -join ((48..57 + 65..90 + 97..122) | Get-Random -Count 32 | ForEach-Object { [char]$_ })
}

New-Item -ItemType Directory -Force -Path $StagingRoot | Out-Null

$ApiKey = New-ApiKey
$OpenAiKey = $env:OPENAI_API_KEY
if (-not $OpenAiKey) {
    Write-Warning "OPENAI_API_KEY is not set. AI templates will deploy but need the key in Railway before they work."
}

$Results = @()

# OpenAI Chat API - skip if project already exists from test deploy
$Results += Deploy-Template `
    -ProjectName "FastAPI Postgres API Template" `
    -ServiceName "FastAPI Postgres API" `
    -TemplatePath (Join-Path $Root "templates/fastapi-postgres") `
    -WithPostgres `
    -Variables @{
        "DATABASE_URL" = '${{Postgres.DATABASE_URL}}'
        "API_KEY"      = $ApiKey
    }

$Results += Deploy-Template `
    -ProjectName "Hono Postgres API Template" `
    -ServiceName "Hono Postgres API" `
    -TemplatePath (Join-Path $Root "templates/hono-postgres") `
    -WithPostgres `
    -Variables @{
        "DATABASE_URL" = '${{Postgres.DATABASE_URL}}'
        "API_KEY"      = $ApiKey
    }

if ($OpenAiKey) {
    $Results += Deploy-Template `
        -ProjectName "AI Agent API Template" `
        -ServiceName "AI Agent API" `
        -TemplatePath (Join-Path $Root "templates/ai-agent-api") `
        -Variables @{
            "OPENAI_API_KEY" = $OpenAiKey
            "OPENAI_MODEL"   = "gpt-4o-mini"
            "API_KEY"        = $ApiKey
            "MAX_TOOL_ROUNDS" = "5"
        }

    $Results += Deploy-Template `
        -ProjectName "RAG Pgvector API Template" `
        -ServiceName "RAG Pgvector API" `
        -TemplatePath (Join-Path $Root "templates/rag-pgvector") `
        -WithPostgres `
        -Variables @{
            "DATABASE_URL"           = '${{Postgres.DATABASE_URL}}'
            "OPENAI_API_KEY"         = $OpenAiKey
            "OPENAI_EMBEDDING_MODEL" = "text-embedding-3-small"
            "OPENAI_CHAT_MODEL"      = "gpt-4o-mini"
            "API_KEY"                = $ApiKey
        }
}

$Results | Format-Table -AutoSize
$Results | ConvertTo-Json | Set-Content (Join-Path $Root "railway-deployments.json")

Write-Output "`nShared API_KEY for protected routes: $ApiKey"
Write-Output "OpenAI Chat API was deployed separately as 'OpenAI Chat API Template'."
