import boto3
import time

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
from utils.config import get_config     # noqa: E402


"""athena db prepare
config.iniの設定に従いathena dbを作成します。
DEFAULTセクションではbucket name,db nameにosのユーザー名が付与されます。
作成されるテーブルはdev_table、データは10年分の最低、最高、平均気温。
"""
conf = get_config()
bucket_name = conf.get('BUCKET_NAME')
db_name = conf.get('ATHENA_DB_NAME')
athena_data_bucket = conf.get('ATHENA_DATA_BUCKET')
athena_result_bucket = conf.get('ATHENA_RESULT_BUCKET')
athena_result_key = conf.get('ATHENA_RESULT_KEY')
table_name = 'dev_table'

s3 = boto3.resource('s3')
s3_client = boto3.client('s3')
athena_client = boto3.client('athena')


def execute_athena(sql_str):
    '''クエリ実行
    '''
    print('query = ' + sql_str)
    queryid = athena_client.start_query_execution(
        QueryString=sql_str,
        ResultConfiguration={
            'OutputLocation': 's3://'
            + athena_result_bucket + '/' + athena_result_key
        }
    )
    return queryid


def check_result(qid):
    '''実行完了まで待機
    '''
    for i in range(12):
        status = athena_client.get_query_execution(
            QueryExecutionId=qid
        )
        if status['QueryExecution']['Status']['State'] == 'SUCCEEDED':
            print(status['QueryExecution']['Status']['State'])
            break
        elif status['QueryExecution']['Status']['State'] == 'FAILED':
            print('クエリ実行に失敗しました。')
            raise Exception
        else:
            time.sleep(1)


def create_database():
    sql_str = 'CREATE DATABASE IF NOT EXISTS ' + db_name
    queryid = execute_athena(sql_str)
    check_result(queryid['QueryExecutionId'])
    print('create database = ' + db_name)


def create_table():
    sql_str = "CREATE EXTERNAL TABLE IF NOT EXISTS " \
        + db_name + "." + table_name \
        + "(`year` int,`month` tinyint,`day` tinyint,`ave` float," \
        + "`max` float,`min` float) " \
        + "ROW FORMAT SERDE " \
        + "'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe' " \
        + "WITH SERDEPROPERTIES ('serialization.format' = ','," \
        + "'field.delim' = ',' ) " \
        + "LOCATION 's3://" + athena_data_bucket + "/" + table_name \
        + "/' TBLPROPERTIES ('has_encrypted_data'='false');"
    queryid = execute_athena(sql_str)
    check_result(queryid['QueryExecutionId'])
    print('created table = ' + table_name)


def upload_data():
    upload_file = __file__.replace('prepare_athena.py', 'datas/weather.csv')
    print(upload_file)
    s3.Object(athena_data_bucket, table_name + '/weather.csv') \
        .upload_file(upload_file)
    print('SUCCEEDED UPLOAD')


if(__name__ == "__main__"):
    create_database()
    create_table()
    upload_data()
    print('prepared database, table, data')
