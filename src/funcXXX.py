import pandas as pd

from utils.config import get_config
from utils.mylogger import MyLogger

# 環境定数
conf = get_config()
# ロガー
logger = MyLogger('wfrpt')


def remove_res100(df):
    return df, df[df['score'] > 100]


df = pd.DataFrame({
    'no': [1, 2, 3],
    'name': ['name1', 'name2', 'name3'],
    'score': [100, 200, 300],
})
logger.info(df)
print('-----------------------------------')

df1, df2 = remove_res100(df)

logger.info(df1)  # origin
logger.info(df2)  # result
