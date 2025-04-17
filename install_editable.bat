@echo off
SETLOCAL

REM I Use this because 'pip install -e .' breaks my pylance for some reason

set "PROJECT_DIR=%~dp0"
set "PACKAGE_NAME=swisscore_tba_lite"
set "VENV_DIR=%PROJECT_DIR%\.venv\Lib\site-packages"

set "LINK_PATH=%VENV_DIR%\%PACKAGE_NAME%"
set "TARGET_PATH=%PROJECT_DIR%\%PACKAGE_NAME%"

IF EXIST "%LINK_PATH%" (
    echo Deleting existing path: %LINK_PATH%
    rmdir /S /Q "%LINK_PATH%"
)

echo Creating symlink...
mklink /D "%LINK_PATH%" "%TARGET_PATH%"

echo Done.
pause