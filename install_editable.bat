@echo off
SETLOCAL

REM I Use this because 'pip install -e .' breaks my pylance for some reason

REM Set your project directory here
set "PROJECT_DIR=D:\python\swisscore-tba-lite"
set "PACKAGE_NAME=swisscore_tba_lite"
set "VENV_DIR=%PROJECT_DIR%\.venv\Lib\site-packages"

REM Full path to target and link
set "LINK_PATH=%VENV_DIR%\%PACKAGE_NAME%"
set "TARGET_PATH=%PROJECT_DIR%\%PACKAGE_NAME%"

REM Delete existing link if it exists
IF EXIST "%LINK_PATH%" (
    echo Deleting existing path: %LINK_PATH%
    rmdir /S /Q "%LINK_PATH%"
)

REM Create symlink
echo Creating symlink...
mklink /D "%LINK_PATH%" "%TARGET_PATH%"

echo Done.
pause