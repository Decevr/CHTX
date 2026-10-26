# Serves the CHTX catalog on localhost and opens it in an Edge app window.
$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$www = Join-Path $root "www"
$profileDir = Join-Path $root "edge-profile"
$portFile = Join-Path $root "port.txt"

function Find-Edge {
    $candidates = @(
        "$env:ProgramFiles\Microsoft\Edge\Application\msedge.exe",
        "${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe"
    )
    foreach ($path in $candidates) {
        if (Test-Path $path) { return $path }
    }
    return $null
}

function Test-Port([int]$Port) {
    $client = New-Object System.Net.Sockets.TcpClient
    try {
        $client.Connect("127.0.0.1", $Port)
        return $true
    } catch {
        return $false
    } finally {
        $client.Dispose()
    }
}

function Get-EdgePids {
    Get-CimInstance Win32_Process -Filter "Name = 'msedge.exe'" | Where-Object {
        $_.CommandLine -and $_.CommandLine -like "*$profileDir*"
    }
}

function Open-Edge([int]$Port) {
    $url = "http://127.0.0.1:$Port/"
    $edge = Find-Edge
    if (-not $edge) {
        Start-Process $url
        return $null
    }
    return Start-Process -FilePath $edge -ArgumentList @(
        "--app=$url",
        "--user-data-dir=$profileDir",
        "--window-size=440,920",
        "--no-first-run",
        "--no-default-browser-check",
        "--disable-sync",
        "--disable-features=msImplicitSignin,msEdgeSync"
    ) -PassThru
}

function Get-ContentType([string]$Path) {
    switch ([IO.Path]::GetExtension($Path).ToLowerInvariant()) {
        ".html" { "text/html; charset=utf-8" }
        ".css" { "text/css; charset=utf-8" }
        ".js" { "text/javascript; charset=utf-8" }
        ".jpg" { "image/jpeg" }
        ".jpeg" { "image/jpeg" }
        ".png" { "image/png" }
        ".woff2" { "font/woff2" }
        ".ttf" { "font/ttf" }
        ".txt" { "text/plain; charset=utf-8" }
        ".ico" { "image/x-icon" }
        default { "application/octet-stream" }
    }
}

function Send-Response($Context) {
    $response = $Context.Response
    try {
        $relative = [Uri]::UnescapeDataString($Context.Request.Url.AbsolutePath).TrimStart("/")
        if ([string]::IsNullOrWhiteSpace($relative)) { $relative = "index.html" }
        $full = [IO.Path]::GetFullPath((Join-Path $www $relative))
        $rootFull = [IO.Path]::GetFullPath($www)
        if (-not $rootFull.EndsWith("\")) { $rootFull = "$rootFull\" }
        $allowed = $full.StartsWith($rootFull, [StringComparison]::OrdinalIgnoreCase) -and (Test-Path $full -PathType Leaf)
        if (-not $allowed) {
            $response.StatusCode = 404
            return
        }
        if ($Context.Request.HttpMethod -eq "HEAD") {
            $response.ContentType = Get-ContentType $full
            return
        }
        $bytes = [IO.File]::ReadAllBytes($full)
        $response.ContentType = Get-ContentType $full
        $response.ContentLength64 = $bytes.Length
        $response.OutputStream.Write($bytes, 0, $bytes.Length)
    } catch {
        $response.StatusCode = 500
    } finally {
        $response.Close()
    }
}

function Serve-Pending($Listener, [ref]$Async, [int]$TimeoutMs) {
    if ($null -eq $Async.Value) {
        $Async.Value = $Listener.BeginGetContext($null, $null)
    }
    if (-not $Async.Value.AsyncWaitHandle.WaitOne($TimeoutMs)) { return }
    Send-Response ($Listener.EndGetContext($Async.Value))
    $Async.Value = $null
}

if (Test-Path $portFile) {
    $saved = (Get-Content $portFile -ErrorAction SilentlyContinue | Select-Object -First 1)
    if ($saved -match "^\d+$" -and (Test-Port ([int]$saved))) {
        Open-Edge ([int]$saved)
        exit 0
    }
}

$port = 47321
$listener = $null
foreach ($candidate in 47321..47340) {
    $tryListener = New-Object System.Net.HttpListener
    $tryListener.Prefixes.Add("http://127.0.0.1:$candidate/")
    try {
        $tryListener.Start()
        $listener = $tryListener
        $port = $candidate
        break
    } catch {
        $tryListener.Close()
    }
}
if (-not $listener) {
    throw "CHTX could not start its local page."
}
Set-Content -Path $portFile -Value $port -Encoding ascii
$edgeProc = Open-Edge $port
$deadline = (Get-Date).AddSeconds(25)
$seen = $false
$pending = $null
try {
    while ($true) {
        Serve-Pending $listener ([ref]$pending) 200
        if ($edgeProc -and -not $edgeProc.HasExited) { $seen = $true }
        if ($seen -and $edgeProc -and $edgeProc.HasExited) { break }
        if (-not $seen) {
            $running = @(Get-EdgePids)
            if ($running.Count -gt 0) { $seen = $true }
            elseif ((Get-Date) -gt $deadline) { break }
        }
    }
} finally {
    $listener.Stop()
    $listener.Close()
    Remove-Item $portFile -ErrorAction SilentlyContinue
}
