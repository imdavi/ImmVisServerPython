#!/bin/bash

SCRIPT_DIR="$( cd "$(dirname "$0")" ; pwd -P )"

ROOT_DIR=$(dirname "$SCRIPT_DIR")

sudo apt install python3-pip python3-setuptools python3-wheel

if hash python3 2>/dev/null; then
    python3 -m pip install -r $ROOT_DIR/requirements.txt
else
    echo "It seems that pip is not installed. Please install Python and PIP to run this script."
fi