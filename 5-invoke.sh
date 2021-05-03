#!/bin/bash
set -eo pipefail
if [ $# -ne 1 ]; then
    echo 'param1 is function name'
    exit 1
fi
FUNCTION=$(aws cloudformation describe-stack-resource --stack-name ${1}-stack --logical-resource-id function --query 'StackResourceDetail.PhysicalResourceId' --output text)
aws lambda invoke --function-name $FUNCTION --payload file://conf/${1}/event.json out.json
