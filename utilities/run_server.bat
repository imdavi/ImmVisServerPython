
@ECHO OFF

SET SCRIPT_DIR=%~dp0

SET ROOT_DIR=%SCRIPT_DIR%..

WHERE python >nul 2>nul
if %ERRORLEVEL% EQU 0  (
    pushd %ROOT_DIR% & python immvis & popd
) else (
    echo It seems that Python is not installed. Please install Python to run this script.
)
