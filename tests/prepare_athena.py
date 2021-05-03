import boto3
import time

from src.utils.config import get_config

conf = get_config()
print(conf.get('BUCKET_NAME'))

bucket_name = 'bucket_name'
db_name = 'dev_database'
table_name = 'dev_table'
athena_result = 'result'

s3 = boto3.resource('s3')
s3_client = boto3.client('s3')
client = boto3.client('athena')


def execute_athena(sql_str):
    '''クエリ実行
    '''
    print('query = ' + sql_str)
    queryid = client.start_query_execution(
        QueryString=sql_str,
        ResultConfiguration={
            'OutputLocation': 's3://' + bucket_name + '/' + athena_result
        }
    )
    return queryid


def check_result(qid):
    '''実行完了まで待機
    '''
    for i in range(12):
        status = client.get_query_execution(
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


def create_table():
    sql_str = "CREATE EXTERNAL TABLE IF NOT EXISTS "+db_name+"." + table_name + \
        "(`year` int,`month` tinyint,`day` tinyint,`ave` float,`max` float,`min` float) " + \
        "ROW FORMAT SERDE " + \
        "'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe' " + \
        "WITH SERDEPROPERTIES (" + \
        "'serialization.format' = ','," + \
        "'field.delim' = ',' ) LOCATION 's3://com.nautilus-technologies.nakazawa.sample/" + \
        table_name + "/' TBLPROPERTIES ('has_encrypted_data'='false');"
    queryid = execute_athena(sql_str)
    check_result(queryid['QueryExecutionId'])


def upload_data():
    upload_file = __file__.replace('create_athena.py', 'datas/weather.csv')
    print(upload_file)
    s3.Object(bucket_name, table_name + '/weather.csv').upload_file(
        upload_file)
    print('SUCCEEDED UPLOAD')


if(__name__ == "__main__"):
    create_database()
    create_table()
    upload_data()
    print('prepared database, table, data')
