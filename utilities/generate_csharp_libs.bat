@ECHO OFF

SET SCRIPT_DIR=%~dp0

SET ROOT_DIR=%SCRIPT_DIR%..

SET PROTO_DIR=%ROOT_DIR%\proto

SET PROTO_FILE=%PROTO_DIR%\immvis.proto

SET IMMVIS_DIR=%ROOT_DIR%\immvis

SET CSHARP_DIR=%ROOT_DIR%\csharp

SET NUGET_FILE_NAME=nuget.exe

SET NUGET_DIR=%CSHARP_DIR%\nuget

SET NUGET_FILE_PATH=%NUGET_DIR%\%NUGET_FILE_NAME%

SET GRPC_VERSION=2.26.0

IF NOT EXIST %CSHARP_DIR% MKDIR %CSHARP_DIR%

IF NOT EXIST %NUGET_DIR% MKDIR %NUGET_DIR%

IF NOT EXIST %NUGET_FILE_PATH% (
    SET NUGET_URL=https://dist.nuget.org/win-x86-commandline/latest/nuget.exe
    powershell -Command "Invoke-WebRequest %NUGET_URL% -OutFile %NUGET_FILE_PATH%"
) 

pushd %NUGET_DIR% & %NUGET_FILE_PATH% install Grpc -Version %GRPC_VERSION% & popd

pushd %NUGET_DIR% & %NUGET_FILE_PATH% install Grpc.Tools -Version %GRPC_VERSION% & popd

SET GRPC_TOOLS_PATH=%NUGET_DIR%\Grpc.Tools.%GRPC_VERSION%\tools\windows_x86

SET GRPC_CSHARP_PLUGIN_PATH=%GRPC_TOOLS_PATH%\grpc_csharp_plugin.exe

SET PROTOC_PATH=%GRPC_TOOLS_PATH%\protoc.exe

SET OUTPUT_DIR=%CSHARP_DIR%

IF EXIST %PROTOC_PATH% (
    IF NOT EXIST %OUTPUT_DIR% MKDIR %OUTPUT_DIR%
    %PROTOC_PATH% -I %PROTO_DIR% --csharp_out %OUTPUT_DIR% --grpc_out %OUTPUT_DIR% %PROTO_FILE% --plugin=protoc-gen-grpc=%GRPC_CSHARP_PLUGIN_PATH%
    echo Done! The generated filed are available on %OUTPUT_DIR%.
) else (
    echo Coundn't find protoc tools, please check if the script ran properly.
)
