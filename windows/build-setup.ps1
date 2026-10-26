$ErrorActionPreference = "Stop"
$repo = Split-Path -Parent $PSScriptRoot
$gradle = Get-Content (Join-Path $repo "app\build.gradle") -Raw
if ($gradle -notmatch 'versionName "([^"]+)"') { throw "versionName was not found." }
$version = $Matches[1]
$dist = Join-Path $repo "dist"
$payload = Join-Path $dist "payload"
if (Test-Path $payload) { Remove-Item $payload -Recurse -Force }
New-Item -ItemType Directory -Path (Join-Path $payload "www") -Force | Out-Null
Copy-Item (Join-Path $repo "app\src\main\assets\www\*") (Join-Path $payload "www") -Recurse -Force
Copy-Item (Join-Path $repo "CHTX.ico") (Join-Path $payload "CHTX.ico") -Force
foreach ($name in @("launch.ps1", "launch.vbs", "install-shortcuts.ps1", "uninstall.ps1", "uninstall.vbs")) {
    Copy-Item (Join-Path $PSScriptRoot $name) (Join-Path $payload $name) -Force
}
$zip = Join-Path $dist "CHTX-payload.zip"
if (Test-Path $zip) { Remove-Item $zip -Force }
tar.exe -a -c -f $zip -C $payload .
if ($LASTEXITCODE -ne 0) { throw "The payload zip failed." }
$staging = Join-Path $dist "staging"
if (Test-Path $staging) { Remove-Item $staging -Recurse -Force }
New-Item -ItemType Directory -Path $staging -Force | Out-Null
Copy-Item $zip (Join-Path $staging "CHTX-payload.zip") -Force
Copy-Item (Join-Path $PSScriptRoot "install.cmd") (Join-Path $staging "install.cmd") -Force
$setup = Join-Path $dist "CHTX-Setup-$version.exe"
$sed = Join-Path $dist "CHTX.sed"
$lines = @(
    "[Version]",
    "Class=IEXPRESS",
    "SEDVersion=3",
    "[Options]",
    "PackagePurpose=InstallApp",
    "ShowInstallProgramWindow=1",
    "HideExtractAnimation=0",
    "UseLongFileName=1",
    "InsideCompressed=0",
    "CAB_FixedSize=0",
    "CAB_ResvCodeSigning=0",
    "RebootMode=N",
    "InstallPrompt=%InstallPrompt%",
    "DisplayLicense=%DisplayLicense%",
    "FinishMessage=%FinishMessage%",
    "TargetName=%TargetName%",
    "FriendlyName=%FriendlyName%",
    "AppLaunched=%AppLaunched%",
    "PostInstallCmd=%PostInstallCmd%",
    "AdminQuietInstCmd=%AdminQuietInstCmd%",
    "UserQuietInstCmd=%UserQuietInstCmd%",
    "SourceFiles=SourceFiles",
    "[Strings]",
    "InstallPrompt=Install CHTX on this PC? It adds a desktop shortcut and a Start menu entry.",
    "DisplayLicense=",
    "FinishMessage=CHTX is installed. Open it from the desktop shortcut or the Start menu.",
    "TargetName=$setup",
    "FriendlyName=CHTX",
    "AppLaunched=install.cmd",
    "PostInstallCmd=<None>",
    "AdminQuietInstCmd=",
    "UserQuietInstCmd=",
    'FILE0="install.cmd"',
    'FILE1="CHTX-payload.zip"',
    "[SourceFiles]",
    "SourceFiles0=$staging",
    "[SourceFiles0]",
    "%FILE0%=",
    "%FILE1%="
)
[IO.File]::WriteAllText($sed, (($lines -join "`r`n") + "`r`n"))
& "$env:SystemRoot\SysWOW64\iexpress.exe" /N $sed
if ($LASTEXITCODE -ne 0 -or -not (Test-Path $setup)) {
    throw "CHTX Setup was not created (exit $LASTEXITCODE)."
}
Get-Item $setup | Select-Object FullName, Length, LastWriteTime
