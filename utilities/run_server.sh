#!/bin/bash

SCRIPT_DIR="$( cd "$(dirname "$0")" ; pwd -P )"

ROOT_DIR=$(dirname "$SCRIPT_DIR")

if hash python 2>/dev/null; then
    (cd $ROOT_DIR; python immvis)
else
    echo "It seems that Python is not installed. Please install Python to run this script."
fi