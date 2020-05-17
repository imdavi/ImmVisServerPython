#!/bin/bash

SCRIPT_DIR="$( cd "$(dirname "$0")" ; pwd -P )"

ROOT_DIR=$(dirname "$SCRIPT_DIR")

PROTO_DIR=$ROOT_DIR/proto

PROTO_FILE=$PROTO_DIR/immvis.proto

OUT_DIR=$ROOT_DIR/immvis/rpc/proto

if [ -f $PROTO_FILE ]; then
    echo Generating Python files...

    if [ ! -e $OUT_DIR ]; then
        mkdir $OUT_DIR
    fi

    python -m grpc_tools.protoc -I $PROTO_DIR  --python_out=$OUT_DIR --grpc_python_out=$OUT_DIR $PROTO_FILE
    
    echo Done! The generated filed are available on $OUT_DIR.
else
   echo "The file '$PROTO_FILE' was not found."
fi