#!/bin/bash
# Lambdaレイヤ用のS3バケットの作成。
BUCKET_ID=$(dd if=/dev/random bs=8 count=1 2>/dev/null | od -An -tx1 | tr -d ' \t\n')
BUCKET_NAME=lambda-artifacts-$BUCKET_ID
echo $BUCKET_NAME > build/bucket-name.txt
aws s3 mb s3://$BUCKET_NAME