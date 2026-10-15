@echo off
setlocal
rem ------------------------------------------------------------------
rem  EM propagation workbench launcher  (pure ASCII on purpose:
rem  a .bat with UTF-8 Chinese is read as GBK by cmd.exe and breaks)
rem ------------------------------------------------------------------
pushd "%~dp0."

echo ============================================================
echo   EM propagation workbench
echo ------------------------------------------------------------
echo   working dir : %CD%
echo   viewer url  : http://localhost:8100/em_viewer.html
echo   close this window to stop the server
echo ============================================================
echo.

if not exist "em_viewer.html" (
    echo [ERROR] em_viewer.html not found in %CD%
    pause
    popd
    exit /b 1
)

set PYEXE=
where python >nul 2>nul && set PYEXE=python
if "%PYEXE%"=="" ( where py >nul 2>nul && set PYEXE=py )
if "%PYEXE%"=="" (
    echo [ERROR] Python not found in PATH.
    pause
    popd
    exit /b 1
)

start "" http://localhost:8100/em_viewer.html
"%PYEXE%" "..\..\citymodel\em_server.py" 8100

popd
endlocal
