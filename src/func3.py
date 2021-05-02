import boto3

from utils.config import get_config
from utils.logger import get_logger
# from logging import getLogger,DEBUG,StreamHandler,Formatter
from utils.athena import exec_athena

# 環境定数
conf = get_config()
# ロガー
logger = get_logger('wfrpt', conf.get('LOG_LEVEL'))


ATHENA_DB_NAME = conf.get('ATHENA_DB_NAME')
ATHENA_RESULT_BUCKET = conf.get('ATHENA_RESULT_BUCKET')
# ATHENA_PREFIX = conf.get('ATHENA_PREFIX')
SQL_STR = 'select year,month,day,ave,max,min from dev_table'
RETRY_COUNT = 300


def lambda_handler(event, context):
    '''handler関数
    引数のeventから対象月を取得。
    '''
    target_month = event['target_month']
    exec(target_month)


def exec(target_month):
    logger.info('target_month = {}'.format(target_month))
    # athenaテーブル:temtureからデータ取得
    sql = 'select year,month,avg(min),avg(ave),avg(max) from dev_table where month='+target_month+' group by year,month order by year,month'
    logger.debug(sql)
    df = exec_athena(sql, conf)
    logger.debug(df)
    return df




if (__name__ == '__main__'):
    lambda_handler({'target_month': '1'}, '')
