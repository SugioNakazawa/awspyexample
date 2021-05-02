import boto3
import time
import pandas as pd
import os
import io
import pprint

from utils.config import get_config
from utils.logger import get_logger

# 環境定数
conf = get_config()
# ロガー
logger = get_logger(__name__, conf.get('LOG_LEVEL'))

DATABASE_NAME = 'mydatabase'
SQL_STR = 'select year,month,day,avetmp1,maxtmp1,mintmp1 from tempture'
OUTPUT_BUCKET = 'com.nautilus-technologies.nakazawa.sample'
ATHENA_PREFIX = 'result'
RETRY_COUNT = 300

athena = boto3.client('athena')


exec_run = athena.start_query_execution(
    QueryString=SQL_STR,
    QueryExecutionContext={'Database': DATABASE_NAME},
    ResultConfiguration={'OutputLocation': 's3://' + OUTPUT_BUCKET+'/'+ATHENA_PREFIX})

query_execution_id = exec_run['QueryExecutionId']
print(query_execution_id)

for i in range(1, 1 + RETRY_COUNT):

    # get query execution
    query_status = athena.get_query_execution(
        QueryExecutionId=query_execution_id)
    query_execution_status = query_status['QueryExecution']['Status']['State']

    if query_execution_status == 'SUCCEEDED':
        print("STATUS:" + query_execution_status)
        break

    if query_execution_status == 'FAILED':
        raise Exception("STATUS:" + query_execution_status)

    else:
        print("STATUS:" + query_execution_status)
        time.sleep(i)
else:
    athena.stop_query_execution(QueryExecutionId=query_execution_id)
    raise Exception('TIME OVER')

results = athena.get_query_results(QueryExecutionId=query_execution_id)
count = 0
for row in results['ResultSet']['Rows']:
    count += 1
    # print(row)
print('row count = {}'.format(count))

data_file_name = f'{exec_run["QueryExecutionId"]}.csv'
object = os.path.join(ATHENA_PREFIX, data_file_name)
# S3から直接pandasへ
s3 = boto3.resource('s3')
s3obj = s3.Object(conf.get('bucket_name'), ATHENA_PREFIX + '/' + data_file_name)
body_in = s3obj.get()['Body'].read().decode('utf-8')
buffer_in = io.StringIO(body_in)
df = pd.read_csv(buffer_in, lineterminator='\n', header=None)
# ローカルにダウンロードするパターン
# s3 = boto3.client('s3')
# s3.download_file(OUTPUT_BUCKET, object, data_file_name)
# df = pd.read_csv(data_file_name)
print(df.shape)
