[CmdletBinding()]
param(
    [string]$Root = "",
    [string]$GodotRelease = "4.7.1-stable",
    [string]$ExpectedGodotVersion = "4.7.1.stable.official.a13da4feb",
    [switch]$ForceRebuild
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

if ([string]::IsNullOrWhiteSpace($Root)) {
    $Root = Join-Path $env:PUBLIC "NOVI\RunnerToolchain"
}

$releaseRoot = "https://github.com/godotengine/godot/releases/download/$GodotRelease"
$cacheRoot = Join-Path $Root "Cache\Godot\$GodotRelease"
$installRoot = Join-Path $Root "Godot\$GodotRelease"
$templateRoot = Join-Path $Root "Templates\Godot\$GodotRelease"
$lockRoot = Join-Path $Root "Locks"
$stateRoot = Join-Path $Root "State"
$statePath = Join-Path $stateRoot "godot-$GodotRelease.json"
$lockPath = Join-Path $lockRoot "godot-$GodotRelease.lock"

foreach ($path in @($cacheRoot, $lockRoot, $stateRoot)) {
    New-Item -ItemType Directory -Force -Path $path | Out-Null
}

function Invoke-BoundedDownload {
    param(
        [Parameter(Mandatory = $true)][string]$Uri,
        [Parameter(Mandatory = $true)][string]$Destination,
        [int]$MaxSeconds = 600
    )
    $curl = Get-Command curl.exe -ErrorAction SilentlyContinue
    if (-not $curl) { throw "curl.exe is required." }
    $partial = "$Destination.partial"
    Remove-Item -LiteralPath $partial -Force -ErrorAction SilentlyContinue
    Write-Host "DOWNLOAD $Uri"
    & $curl.Source --fail --location --silent --show-error --connect-timeout 30 --max-time $MaxSeconds --retry 3 --retry-delay 2 --output $partial $Uri
    if ($LASTEXITCODE -ne 0) {
        Remove-Item -LiteralPath $partial -Force -ErrorAction SilentlyContinue
        throw "Download failed for '$Uri' with curl exit code $LASTEXITCODE."
    }
    Move-Item -LiteralPath $partial -Destination $Destination -Force
}

function Get-ExpectedHash {
    param(
        [Parameter(Mandatory = $true)][string]$SumsPath,
        [Parameter(Mandatory = $true)][string]$FileName
    )
    $line = Get-Content -LiteralPath $SumsPath | Where-Object { $_ -match "\s+$([regex]::Escape($FileName))$" } | Select-Object -First 1
    if (-not $line) { throw "No SHA-512 entry for $FileName." }
    return (($line -split "\s+")[0]).ToUpperInvariant()
}

function Get-VerifiedArchive {
    param(
        [Parameter(Mandatory = $true)][string]$FileName,
        [Parameter(Mandatory = $true)][string]$SumsPath
    )
    $archive = Join-Path $cacheRoot $FileName
    $expected = Get-ExpectedHash -SumsPath $SumsPath -FileName $FileName
    $valid = $false
    if (Test-Path -LiteralPath $archive -PathType Leaf) {
        $actual = (Get-FileHash -Algorithm SHA512 -LiteralPath $archive).Hash.ToUpperInvariant()
        $valid = $actual -eq $expected
        if ($valid) { Write-Host "CACHE HIT verified archive: $FileName" }
    }
    if (-not $valid) {
        Invoke-BoundedDownload -Uri "$releaseRoot/$FileName" -Destination $archive -MaxSeconds 600
        $actual = (Get-FileHash -Algorithm SHA512 -LiteralPath $archive).Hash.ToUpperInvariant()
        if ($actual -ne $expected) { throw "SHA-512 mismatch for $FileName." }
    }
    return $archive
}

function Find-GodotBinary {
    param([string]$Directory)
    if (-not (Test-Path -LiteralPath $Directory -PathType Container)) { return $null }
    return Get-ChildItem -LiteralPath $Directory -Filter "Godot_*_console.exe" -File -ErrorAction SilentlyContinue | Select-Object -First 1
}

function Test-GodotInstall {
    param([string]$Directory)
    $binary = Find-GodotBinary -Directory $Directory
    if (-not $binary) { return $null }
    $version = ((& $binary.FullName --version 2>$null) -join "").Trim()
    if ($LASTEXITCODE -ne 0 -or $version -ne $ExpectedGodotVersion) { return $null }
    return $binary
}

function Test-TemplateInstall {
    param([string]$Directory)
    if (-not (Test-Path -LiteralPath $Directory -PathType Container)) { return $null }
    $exact = Join-Path $Directory "windows_release_x86_64.exe"
    if (Test-Path -LiteralPath $exact -PathType Leaf) { return Get-Item -LiteralPath $exact }
    return Get-ChildItem -LiteralPath $Directory -Filter "windows_release*.exe" -File -ErrorAction SilentlyContinue | Select-Object -First 1
}

function Get-FileSha256OrEmpty {
    param([string]$Path)
    if (-not $Path -or -not (Test-Path -LiteralPath $Path -PathType Leaf)) { return "" }
    return (Get-FileHash -Algorithm SHA256 -LiteralPath $Path).Hash.ToUpperInvariant()
}

$deadline = [DateTime]::UtcNow.AddSeconds(120)
$lock = $null
while (-not $lock) {
    try {
        $lock = [System.IO.File]::Open($lockPath, [System.IO.FileMode]::OpenOrCreate, [System.IO.FileAccess]::ReadWrite, [System.IO.FileShare]::None)
    }
    catch {
        if ([DateTime]::UtcNow -ge $deadline) { throw "Timed out waiting for NOVI toolchain lock '$lockPath'." }
        Start-Sleep -Seconds 2
    }
}

try {
    $state = $null
    if (Test-Path -LiteralPath $statePath -PathType Leaf) {
        try { $state = Get-Content -Raw -LiteralPath $statePath | ConvertFrom-Json } catch { $state = $null }
    }

    $engine = Test-GodotInstall -Directory $installRoot
    $sharedTemplate = Test-TemplateInstall -Directory $templateRoot
    $stateMatches = $state -and $state.godot_release -eq $GodotRelease -and $state.expected_version -eq $ExpectedGodotVersion
    $integrityMatches = $false
    if ($stateMatches -and $engine -and $sharedTemplate -and -not $ForceRebuild) {
        $engineHash = Get-FileSha256OrEmpty -Path $engine.FullName
        $templateHash = Get-FileSha256OrEmpty -Path $sharedTemplate.FullName
        $integrityMatches = ($engineHash -eq $state.engine_binary_sha256) -and ($templateHash -eq $state.windows_template_sha256)
    }

    $mode = "HIT"
    if (-not $integrityMatches) {
        $mode = if ($ForceRebuild) { "REBUILD" } else { "REPAIR" }
        Write-Host "NOVI runner toolchain $mode required."

        $sums = Join-Path $cacheRoot "SHA512-SUMS.txt"
        Invoke-BoundedDownload -Uri "$releaseRoot/SHA512-SUMS.txt" -Destination $sums -MaxSeconds 120

        $engineArchiveName = "Godot_v${GodotRelease}_win64.exe.zip"
        $engineArchive = Get-VerifiedArchive -FileName $engineArchiveName -SumsPath $sums
        if ($ForceRebuild -or -not $engine) {
            $staging = Join-Path $Root ("Staging\Godot-" + [guid]::NewGuid().ToString("N"))
            New-Item -ItemType Directory -Force -Path $staging | Out-Null
            Expand-Archive -LiteralPath $engineArchive -DestinationPath $staging -Force
            $staged = Test-GodotInstall -Directory $staging
            if (-not $staged) { throw "Verified Godot archive did not produce expected engine version." }
            if (Test-Path -LiteralPath $installRoot) { Remove-Item -LiteralPath $installRoot -Recurse -Force }
            New-Item -ItemType Directory -Force -Path (Split-Path -Parent $installRoot) | Out-Null
            Move-Item -LiteralPath $staging -Destination $installRoot
            $engine = Test-GodotInstall -Directory $installRoot
        }

        $templateArchiveName = "Godot_v${GodotRelease}_export_templates.tpz"
        $templateArchive = Get-VerifiedArchive -FileName $templateArchiveName -SumsPath $sums
        if ($ForceRebuild -or -not $sharedTemplate) {
            $templateStaging = Join-Path $Root ("Staging\Templates-" + [guid]::NewGuid().ToString("N"))
            New-Item -ItemType Directory -Force -Path $templateStaging | Out-Null
            $templateZip = Join-Path $templateStaging "templates.zip"
            Copy-Item -LiteralPath $templateArchive -Destination $templateZip -Force
            Expand-Archive -LiteralPath $templateZip -DestinationPath $templateStaging -Force
            $source = Join-Path $templateStaging "templates"
            if (-not (Test-Path -LiteralPath $source -PathType Container)) { throw "Export template archive missing templates/." }
            if (Test-Path -LiteralPath $templateRoot) { Remove-Item -LiteralPath $templateRoot -Recurse -Force }
            New-Item -ItemType Directory -Force -Path (Split-Path -Parent $templateRoot) | Out-Null
            Move-Item -LiteralPath $source -Destination $templateRoot
            Remove-Item -LiteralPath $templateStaging -Recurse -Force -ErrorAction SilentlyContinue
            $sharedTemplate = Test-TemplateInstall -Directory $templateRoot
            if (-not $sharedTemplate) { throw "Shared Windows export template missing after extraction." }
        }

        $engineHash = Get-FileSha256OrEmpty -Path $engine.FullName
        $templateHash = Get-FileSha256OrEmpty -Path $sharedTemplate.FullName
        $newState = [ordered]@{
            schema = "novi.runner_toolchain_state.v1"
            godot_release = $GodotRelease
            expected_version = $ExpectedGodotVersion
            engine_binary = $engine.FullName
            engine_binary_sha256 = $engineHash
            shared_template = $sharedTemplate.FullName
            windows_template_sha256 = $templateHash
            updated_utc = [DateTime]::UtcNow.ToString("o")
        }
        $tmpState = "$statePath.tmp"
        $newState | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $tmpState -Encoding UTF8
        Move-Item -LiteralPath $tmpState -Destination $statePath -Force
    }
    else {
        Write-Host "NOVI runner toolchain HIT: verified engine and templates already present."
    }

    $engine = Test-GodotInstall -Directory $installRoot
    if (-not $engine) { throw "NOVI runner toolchain final shared Godot validation failed." }
    $sharedEngineHash = Get-FileSha256OrEmpty -Path $engine.FullName

    $runnerInstallRoot = Join-Path $env:LOCALAPPDATA "NOVI\Godot\$GodotRelease"
    $runnerEngine = Test-GodotInstall -Directory $runnerInstallRoot
    $runnerEngineHash = if ($runnerEngine) { Get-FileSha256OrEmpty -Path $runnerEngine.FullName } else { "" }
    if (-not $runnerEngine -or $runnerEngineHash -ne $sharedEngineHash) {
        Write-Host "REPAIR runner-local Godot view: $runnerInstallRoot"
        if (Test-Path -LiteralPath $runnerInstallRoot) { Remove-Item -LiteralPath $runnerInstallRoot -Recurse -Force }
        New-Item -ItemType Directory -Force -Path $runnerInstallRoot | Out-Null
        Copy-Item -Path (Join-Path $installRoot "*") -Destination $runnerInstallRoot -Recurse -Force
    }

    $templateVersion = $GodotRelease.Replace("-stable", ".stable")
    $runnerTemplateRoot = Join-Path $env:APPDATA "Godot\export_templates\$templateVersion"
    $runnerTemplate = Test-TemplateInstall -Directory $runnerTemplateRoot
    $sharedTemplate = Test-TemplateInstall -Directory $templateRoot
    if (-not $runnerTemplate -or (Get-FileSha256OrEmpty -Path $runnerTemplate.FullName) -ne (Get-FileSha256OrEmpty -Path $sharedTemplate.FullName)) {
        Write-Host "REPAIR runner-local Godot template view: $runnerTemplateRoot"
        if (Test-Path -LiteralPath $runnerTemplateRoot) { Remove-Item -LiteralPath $runnerTemplateRoot -Recurse -Force }
        New-Item -ItemType Directory -Force -Path $runnerTemplateRoot | Out-Null
        Copy-Item -Path (Join-Path $templateRoot "*") -Destination $runnerTemplateRoot -Recurse -Force
    }

    $runnerEngine = Test-GodotInstall -Directory $runnerInstallRoot
    if (-not $runnerEngine) { throw "NOVI runner toolchain final runner-local Godot validation failed." }
    $runnerTemplate = Test-TemplateInstall -Directory $runnerTemplateRoot
    if (-not $runnerTemplate) { throw "NOVI runner toolchain final export-template validation failed." }

    Write-Host "NOVI_TOOLCHAIN_STATUS=$mode"
    Write-Host "NOVI_GODOT=$($engine.FullName)"
    Write-Host "NOVI_RUNNER_GODOT=$($runnerEngine.FullName)"
    Write-Host "NOVI_TEMPLATES=$runnerTemplateRoot"
    if ($env:GITHUB_OUTPUT) {
        "status=$mode" >> $env:GITHUB_OUTPUT
        "godot=$($engine.FullName)" >> $env:GITHUB_OUTPUT
        "runner_godot=$($runnerEngine.FullName)" >> $env:GITHUB_OUTPUT
        "templates=$runnerTemplateRoot" >> $env:GITHUB_OUTPUT
        "root=$Root" >> $env:GITHUB_OUTPUT
    }
}
finally {
    if ($lock) { $lock.Dispose() }
}
