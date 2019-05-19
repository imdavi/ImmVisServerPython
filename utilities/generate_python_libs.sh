#!/bin/bash

SCRIPT_DIR="$( cd "$(dirname "$0")" ; pwd -P )"

ROOT_DIR=$(dirname "$SCRIPT_DIR")

PROTO_DIR=$ROOT_DIR/proto

PROTO_FILE=$PROTO_DIR/immvis.proto

IMMVIS_DIR=$ROOT_DIR/immvis

if [ -f $PROTO_FILE ]; then
    echo Generating Python files...

    python -m grpc_tools.protoc -I $PROTO_DIR  --python_out=$IMMVIS_DIR --grpc_python_out=$IMMVIS_DIR $PROTO_FILE
else
   echo "The file '$PROTO_FILE' was not found."
fi