from utils.config import get_config
from utils.mylogger import MyLogger
from src.utils.athenaaccess import AthenaAccess

# 定数
conf = get_config()
# ロガー
logger = MyLogger('wfrpt')


def lambda_handler(event, context):
    """eventから対象月を取得し対象データを取得。

    Args:
        event['target_month'](int): 対象月

    Returns：
        抽出データの件数(int)
    """
    target_month = event['target_month']
    df = exec(target_month)
    return df.shape[0]


def exec(target_month):
    """athenaから対象月のデータを取得。

    Args:
        target_month: 対象月

    Returns:
        対象月のデータ(DataFrame)
    """
    logger.debug('target_month = {}'.format(target_month))
    athena = AthenaAccess()
    # athenaテーブル:temtureからデータ取得
    sql = 'select year,month,avg(min),avg(ave),avg(max) ' + \
        'from dev_table where month=' + target_month + \
        ' group by year,month order by year,month'
    logger.debug('sql = ' + sql)
    df = athena.execute(sql)
    logger.debug('data = ' + df)
    return df
