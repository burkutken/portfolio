# Prepare a normal update to the existing repository; does not commit or push.
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$publishRoot = Join-Path $projectRoot '.publish'
$repositoryUrl = 'https://github.com/burkutken/portfolio.git'

Get-Command git, python -ErrorAction Stop | Out-Null
Push-Location -LiteralPath $projectRoot
try {
    python scripts/build.py --output .
    if ($LASTEXITCODE -ne 0) { throw 'Root page build failed.' }
    python scripts/build.py
    if ($LASTEXITCODE -ne 0) { throw 'Publishing build failed.' }
    python scripts/check_site.py
    if ($LASTEXITCODE -ne 0) { throw 'Site validation failed.' }

    if (-not (Test-Path -LiteralPath $publishRoot)) {
        git clone --branch main --single-branch $repositoryUrl $publishRoot
        if ($LASTEXITCODE -ne 0) { throw 'Repository clone failed.' }
    }
    if (-not (Test-Path -LiteralPath (Join-Path $publishRoot '.git'))) {
        throw '.publish exists but is not the expected Git checkout.'
    }
    $remoteUrl = git -C $publishRoot remote get-url origin
    if ($LASTEXITCODE -ne 0 -or $remoteUrl -ne $repositoryUrl) {
        throw 'The publishing checkout has an unexpected origin.'
    }
    $branch = git -C $publishRoot branch --show-current
    if ($LASTEXITCODE -ne 0 -or $branch -ne 'main') {
        throw 'The publishing checkout must be on main.'
    }

    # Explicit list keeps report extracts, tools, previews and archives local.
    foreach ($directory in @('.github', 'assets', 'content', 'docs', 'images', 'pdf', 'scripts', 'templates', 'case-studies')) {
        Copy-Item -LiteralPath (Join-Path $projectRoot $directory) -Destination $publishRoot -Recurse -Force
    }
    foreach ($file in @('README.md', 'requirements.txt', '.gitignore', '.nojekyll', 'sitemap.xml', '._generated-pages.json')) {
        Copy-Item -LiteralPath (Join-Path $projectRoot $file) -Destination $publishRoot -Force
    }
    $generatedPages = Get-Content -LiteralPath (Join-Path $projectRoot '._generated-pages.json') -Raw | ConvertFrom-Json
    foreach ($page in $generatedPages) {
        if ($page -notmatch '/') {
            Copy-Item -LiteralPath (Join-Path $projectRoot $page) -Destination $publishRoot -Force
        }
    }
    git -C $publishRoot add --all
    if ($LASTEXITCODE -ne 0) { throw 'Git staging failed.' }
    git --no-pager -C $publishRoot diff --cached --stat
    if ($LASTEXITCODE -ne 0) { throw 'Could not inspect the staged changes.' }
    Write-Output 'Ready in .publish. Review the staged changes, then commit and push.'
} finally {
    Pop-Location
}
