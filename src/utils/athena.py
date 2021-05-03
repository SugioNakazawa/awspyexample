from logging import getLogger, DEBUG
import boto3
import time
import pandas as pd
import io
import os

logger = getLogger('wfrpt.'+__name__)

RETRY_COUNT = 100
athena = boto3.client('athena')


def exec_athena(sql, conf):
    '''SQLを渡すと実行結果をpandasのDataFrameで返却。
    エラーの時はException
    '''
    database = conf.get('ATHENA_DB_NAME')
    out_bucket = str(conf.get('ATHENA_RESULT_BUCKET'))
    data_prefix = str(conf.get('ATHENA_RESULT_KEY'))
    # SQL実行
    exec_run = athena.start_query_execution(
        QueryString=sql,
        QueryExecutionContext={'Database': database},
        ResultConfiguration={'OutputLocation': 's3://' + out_bucket+'/'+data_prefix})
    query_execution_id = exec_run['QueryExecutionId']
    # 完了待ち
    result = wait_for_done(query_execution_id)
    # DataFrameへ変換
    data_file_name = f'{exec_run["QueryExecutionId"]}.csv'
    object = os.path.join(data_prefix, data_file_name)
    # S3から直接pandasへ
    s3 = boto3.resource('s3')
    s3obj = s3.Object(conf.get('bucket_name'),
                      data_prefix + '/' + data_file_name)
    body_in = s3obj.get()['Body'].read().decode('utf-8')
    buffer_in = io.StringIO(body_in)
    df = pd.read_csv(buffer_in, lineterminator='\n', header=None)
    return df


def wait_for_done(query_execution_id):
    '''実行されたSQLが完了するまで待ち、結果のresultを返す。
    エラーの時はException
    '''
    for i in range(1, 1 + RETRY_COUNT):
        query_status = athena.get_query_execution(
            QueryExecutionId=query_execution_id)
        query_execution_status = query_status['QueryExecution']['Status']['State']
        if query_execution_status == 'SUCCEEDED':
            logger.info("STATUS:" + query_execution_status)
            break
        if query_execution_status == 'FAILED':
            logger.error(query_status)
            raise Exception("STATUS:" + query_execution_status)
        else:
            logger.info("STATUS:" + query_execution_status)
            time.sleep(i)
    else:
        athena.stop_query_execution(QueryExecutionId=query_execution_id)
        raise Exception('TIME OVER')

    return athena.get_query_results(QueryExecutionId=query_execution_id)


# start only test
# DEBUGでこのモジュールを実行するため
if (__name__ == '__main__'):
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '.'))
    import config
    ret = exec_athena("select year,month,day,ave,max,min from dev_table where month=1",
                      config.get_config())
    print(ret)
# end only test
