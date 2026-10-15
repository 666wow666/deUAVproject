@echo off
setlocal
rem ------------------------------------------------------------------
rem  Zhengzhou building 3D model - local preview launcher
rem  NOTE: this file is intentionally pure ASCII. A .bat containing
rem  UTF-8 Chinese text is read by cmd.exe as GBK and gets garbled.
rem ------------------------------------------------------------------

pushd "%~dp0."

echo ============================================================
echo   Zhengzhou building 3D model  -  local preview
echo ------------------------------------------------------------
echo   working dir : %CD%
echo   viewer url  : http://localhost:8000/viewer.html
echo   close this window to stop the server
echo ============================================================
echo.

if not exist "viewer.html" (
    echo [ERROR] viewer.html not found in %CD%
    echo         Keep this .bat in the same folder as viewer.html.
    pause
    popd
    exit /b 1
)
if not exist "city_model.glb" (
    echo [ERROR] city_model.glb not found in %CD%
    pause
    popd
    exit /b 1
)

set PYEXE=
where python >nul 2>nul && set PYEXE=python
if "%PYEXE%"=="" ( where py >nul 2>nul && set PYEXE=py )
if "%PYEXE%"=="" (
    echo [ERROR] Python not found in PATH.
    echo         Install Python, then run:  python -m http.server 8000
    pause
    popd
    exit /b 1
)

echo Starting server with "%PYEXE%" ...
start "" http://localhost:8000/viewer.html
"%PYEXE%" -m http.server 8000

popd
endlocal
