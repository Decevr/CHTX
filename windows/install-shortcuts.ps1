param(
    [string]$Desktop = [Environment]::GetFolderPath("Desktop"),
    [string]$Programs = [Environment]::GetFolderPath("Programs")
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$icon = Join-Path $root "CHTX.ico"
$launch = Join-Path $root "launch.vbs"
$uninstall = Join-Path $root "uninstall.vbs"
$shell = New-Object -ComObject WScript.Shell
$menu = Join-Path $Programs "CHTX"
New-Item -ItemType Directory -Force -Path $menu | Out-Null

function New-Link([string]$Path, [string]$Target, [string]$Arguments, [string]$Description) {
    $link = $shell.CreateShortcut($Path)
    $link.TargetPath = $Target
    $link.Arguments = $Arguments
    $link.WorkingDirectory = $root
    $link.IconLocation = "$icon,0"
    $link.Description = $Description
    $link.Save()
}

$wscript = Join-Path $env:SystemRoot "System32\wscript.exe"
New-Link (Join-Path $Desktop "CHTX.lnk") $wscript "//B `"$launch`"" "CHTX"
New-Link (Join-Path $menu "CHTX.lnk") $wscript "//B `"$launch`"" "CHTX"
New-Link (Join-Path $menu "Uninstall CHTX.lnk") $wscript "//B `"$uninstall`"" "Uninstall CHTX"
