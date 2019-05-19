@ECHO OFF

SET SCRIPT_DIR=%~dp0

SET ROOT_DIR=%SCRIPT_DIR%..

WHERE pip >nul 2>nul
if %ERRORLEVEL% EQU 0  (
    pip install -r %ROOT_DIR%/requirements.txt
) else (
    echo It seems that pip is not installed. Please install Python and PIP to run this script.
)
