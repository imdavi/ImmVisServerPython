echo Generating Python files...

SET PROTO_FILE="./protofiles/immvis.proto"

python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. %PROTO_FILE%

move /y .\protofiles\*.py ./immvis-grpc/
