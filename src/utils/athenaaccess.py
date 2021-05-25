from logging import getLogger
import boto3
import time
import pandas as pd
import io
from utils.config import get_config

logger = getLogger('wfrpt.'+__name__)
conf = get_config()
RETRY_COUNT = 100


class AthenaAccess:
    """AWS Athenaにアクセスする共通クラス"""

    def __init__(self):
        """コンストラクタ"""
        self.database = conf.get('ATHENA_DB_NAME')
        self.out_bucket = str(conf.get('ATHENA_RESULT_BUCKET'))
        self.data_prefix = str(conf.get('ATHENA_RESULT_KEY'))
        self.result_bucket = 's3://' + self.out_bucket + '/' + self.data_prefix
        self.athena = boto3.client('athena')

    def execute(self, sql):
        """AthenaへのSQL実行

        Args:
            sq;(str): SQL文字列

        Returns:
            結果をpandas.DataFrameに変換されたObject
        """
        exec_run = self.athena.start_query_execution(
            QueryString=sql,
            QueryExecutionContext={'Database': self.database},
            ResultConfiguration={'OutputLocation': self.result_bucket}
        )
        query_execution_id = exec_run['QueryExecutionId']
        # 完了待ち
        self.wait_for_done(query_execution_id)
        # DataFrameへ変換
        data_file_name = f'{exec_run["QueryExecutionId"]}.csv'
        # S3から直接pandasへ
        s3 = boto3.resource('s3')
        s3obj = s3.Object(
            self.out_bucket, self.data_prefix + '/' + data_file_name)
        body_in = s3obj.get()['Body'].read().decode('utf-8')
        buffer_in = io.StringIO(body_in)
        df = pd.read_csv(buffer_in, lineterminator='\n', header=None)
        return df

    def wait_for_done(self, query_execution_id):
        '''実行されたSQLが完了するまで待ち、結果のresultを返す。
        エラーの時はException
        '''
        for i in range(1, 1 + RETRY_COUNT):
            query_status = self.athena.get_query_execution(
                QueryExecutionId=query_execution_id)
            query_execution_status = \
                query_status['QueryExecution']['Status']['State']
            if query_execution_status == 'SUCCEEDED':
                logger.debug("STATUS:" + query_execution_status)
                break
            if query_execution_status == 'FAILED':
                logger.error(query_status)
                raise Exception("STATUS:" + query_execution_status)
            else:
                logger.debug("STATUS:" + query_execution_status)
                time.sleep(i)
        else:
            self.athena.stop_query_execution(
                QueryExecutionId=query_execution_id)
            raise Exception('TIME OVER athena query')

        return self.athena.get_query_results(
            QueryExecutionId=query_execution_id)
