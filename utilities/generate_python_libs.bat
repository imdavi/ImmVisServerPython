
@ECHO OFF

SET SCRIPT_DIR=%~dp0

SET ROOT_DIR=%SCRIPT_DIR%..

SET PROTO_DIR=%ROOT_DIR%\proto

SET PROTO_FILE=%PROTO_DIR%\immvis.proto

SET IMMVIS_DIR=%ROOT_DIR%\immvis

SET OUT_DIR=%IMMVIS_DIR%\grpc\proto
MKDIR %OUT_DIR%

if exist %PROTO_FILE% (
    echo Generating Python files...

    python -m grpc_tools.protoc -I %PROTO_DIR%  --python_out=%OUT_DIR% --grpc_python_out=%OUT_DIR% %PROTO_FILE%

    echo Done! The generated filed are available on %IMMVIS_DIR%.
) else (
    echo The file '%PROTO_FILE%' was not found.
)
