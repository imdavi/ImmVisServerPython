#!/bin/bash

SCRIPT_DIR="$( cd "$(dirname "$0")" ; pwd -P )"

ROOT_DIR=$(dirname "$SCRIPT_DIR")

PROTO_DIR=$ROOT_DIR/proto

PROTO_FILE=$PROTO_DIR/immvis.proto

GRPC_VERSION=2.23.0

CSHARP_DIR=$ROOT_DIR/csharp

NUGET_DIR=$CSHARP_DIR/nuget

if hash nuget 2>/dev/null; then
    if [ ! -e $CSHARP_DIR ]; then
        mkdir $CSHARP_DIR
    fi

    if [ ! -e $NUGET_DIR ]; then
        mkdir $NUGET_DIR
    fi

    (cd $NUGET_DIR; nuget install Grpc -Version $GRPC_VERSION)
    
    (cd $NUGET_DIR; nuget install Grpc.Tools -Version $GRPC_VERSION)
    
    GRPC_TOOLS_PATH=$NUGET_DIR/Grpc.Tools.$GRPC_VERSION/tools/linux_x86

    GRPC_CSHARP_PLUGIN_PATH=$GRPC_TOOLS_PATH/grpc_csharp_plugin

    PROTOC_PATH=$GRPC_TOOLS_PATH/protoc

    OUTPUT_DIR=$CSHARP_DIR

    if [ ! -e $OUTPUT_DIR ]; then
        mkdir $OUTPUT_DIR
    fi

    if [ -e $PROTOC_PATH ]; then
        $PROTOC_PATH -I $PROTO_DIR --csharp_out $OUTPUT_DIR --grpc_out $OUTPUT_DIR $PROTO_FILE --plugin=protoc-gen-grpc=$GRPC_CSHARP_PLUGIN_PATH
        echo Done! The generated filed are available on $OUTPUT_DIR.
    else
        echo Coundn\'t find protoc tools, please check if the script ran properly.
    fi
else
    echo "It seems that nuget is not installed. Please install dotnet core and nuget to run this script."
fi
