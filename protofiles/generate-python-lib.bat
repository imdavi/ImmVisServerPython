echo Generating CS files...

SET OUTPUT_DIR="./python-lib"

mkdir %OUTPUT_DIR%

SET PROTO_FILE="./immvis.proto"

python -m grpc_tools.protoc -I. --python_out=%OUTPUT_DIR% --grpc_python_out=%OUTPUT_DIR% %PROTO_FILE%