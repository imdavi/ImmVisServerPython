#!/bin/bash

SCRIPT_DIR="$( cd "$(dirname "$0")" ; pwd -P )"

ROOT_DIR=$(dirname "$SCRIPT_DIR")

if hash pip 2>/dev/null; then
    pip install -r $ROOT_DIR/requirements.txt
else
    echo "It seems that pip is not installed. Please install Python and PIP to run this script."
fi