#!/bin/bash
set -eo pipefail
rm -rf build/package
mkdir -p build/package

# local os is amazonlinux
# pipenv lock -r > requirements.txt
# pip install --target ./package/python -r requirements.txt

# local os is others
cd build
tar xvzf ../package.tar