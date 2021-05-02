#!/bin/bash
if [ $# -ne 2 ]; then
    echo 'param1 is pkg name'
    echo 'param2 is function name'
    exit 1
fi
# ディレクトリ名がバッチID、ファイル名は固定。
python -m ${1}.src.${2}
