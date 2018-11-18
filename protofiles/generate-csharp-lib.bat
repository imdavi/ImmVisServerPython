
echo Generating CS files...

SET OUTPUT_DIR="./csharp-lib"

mkdir %OUTPUT_DIR%

SET GRPC_TOOLS_PATH="%HOMEPATH%\.nuget\packages\grpc.tools\1.14.1\tools\windows_x86"

SET PROTO_FILE="./immvis.proto"

%GRPC_TOOLS_PATH%\protoc.exe -I. --csharp_out %OUTPUT_DIR% --grpc_out %OUTPUT_DIR% %PROTO_FILE% --plugin=protoc-gen-grpc=%GRPC_TOOLS_PATH%\grpc_csharp_plugin.exe
