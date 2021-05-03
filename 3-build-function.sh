#!/bin/bash
set -eo pipefail
if [ $# -ne 1 ]; then
    echo 'param1 is pkg name'
    exit 1
fi

# build archive function
rm -fr conf/${1}/build/
mkdir conf/${1}/build
cd src
zip -r ../conf/${1}/build/func.zip utils/*
zip ../conf/${1}/build/func.zip ${1}.py
