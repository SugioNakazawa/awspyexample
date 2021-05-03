#!/bin/bash
set -eo pipefail
if [ $# -ne 1 ]; then
    echo 'param1 is pkg name'
    exit 1
fi
ARTIFACT_BUCKET=$(cat build/bucket-name.txt)
aws cloudformation package --template-file conf/${1}/template.yml --s3-bucket $ARTIFACT_BUCKET --output-template-file out.yml
aws cloudformation deploy --template-file out.yml --stack-name ${1}-stack --capabilities CAPABILITY_NAMED_IAM
