@echo off
setlocal
set "HERE=%~dp0"
set "DEST=%LOCALAPPDATA%\CHTX"
echo Installing CHTX...
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -and ($_.CommandLine -like '*\CHTX\launch.ps1*' -or $_.CommandLine -like '*\CHTX\edge-profile*') } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }"
if exist "%DEST%" rmdir /s /q "%DEST%"
mkdir "%DEST%"
tar.exe -xf "%HERE%CHTX-payload.zip" -C "%DEST%"
if errorlevel 1 (
  echo CHTX could not unpack its files.
  exit /b 1
)
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%DEST%\install-shortcuts.ps1"
if errorlevel 1 (
  echo CHTX could not create its shortcuts.
  exit /b 1
)
echo CHTX is installed.
exit /b 0
