import boto3
import time

bucket_name = 'com.nautilus-technologies.nakazawa.sample'
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


def drop_database():
    sql_str = 'DROP DATABASE IF EXISTS ' + db_name + ' CASCADE'
    queryid = execute_athena(sql_str)
    check_result(queryid['QueryExecutionId'])


if(__name__ == "__main__"):
    drop_database()
    print('dropped database')
