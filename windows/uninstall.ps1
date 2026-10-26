$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Add-Type -AssemblyName System.Windows.Forms
$answer = [System.Windows.Forms.MessageBox]::Show(
    "Remove CHTX from this PC?",
    "CHTX",
    [System.Windows.Forms.MessageBoxButtons]::YesNo,
    [System.Windows.Forms.MessageBoxIcon]::Question
)
if ($answer -ne [System.Windows.Forms.DialogResult]::Yes) { exit 0 }

Get-CimInstance Win32_Process | Where-Object {
    $_.CommandLine -and (
        $_.CommandLine -like "*$root\launch.ps1*" -or
        $_.CommandLine -like "*$root\edge-profile*"
    )
} | ForEach-Object {
    Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue
}

$shell = New-Object -ComObject WScript.Shell
$desktopLink = Join-Path ([Environment]::GetFolderPath("Desktop")) "CHTX.lnk"
if (Test-Path $desktopLink) {
    $link = $shell.CreateShortcut($desktopLink)
    if ($link.Arguments -like "*$root*") {
        Remove-Item $desktopLink -Force
    }
}
$menu = Join-Path ([Environment]::GetFolderPath("Programs")) "CHTX"
if (Test-Path $menu) {
    Remove-Item $menu -Recurse -Force
}

$removed = Join-Path $env:TEMP "chtx-uninstall.cmd"
@(
    "@echo off",
    "timeout /t 1 /nobreak >nul",
    "rmdir /s /q `"$root`""
) | Set-Content -Path $removed -Encoding ascii
Start-Process -FilePath $removed -WindowStyle Hidden
