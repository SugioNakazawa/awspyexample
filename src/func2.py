import boto3
import io
import pandas as pd

from utils.config import get_config
from utils.logger import get_logger

# 環境定数
conf = get_config()
# ロガー
logger = get_logger('wfrpt', conf.get('LOG_LEVEL'))

bucket_name = conf.get('bucket_name')
s3 = boto3.resource('s3')


def lambda_handler(event, context):
    """call from lambda
    key=datakey で渡されたディレクトリ（S3オブジェクトの接頭）にマッチする
    オブジェクト（CSVファイル）を取得し、変換してS3に同じファイルで出力（上書き）する。
    """
    preffix = event['datakey']
    execute(preffix)


def execute(preffix):
    """指定ディレクトリ内のファイルを変換してs3へ出力。
    """
    bucket = s3.Bucket(bucket_name)
    logger.debug('bucket name = ' + bucket.name)
    for obj in bucket.objects.all():
        if (obj.key.startswith(preffix)
                and len(obj.key) > len(preffix) + 1
                and not obj.key.endswith('.out')):
            logger.debug('read file = ' + obj.key)
            s3obj = s3.Object(bucket_name, obj.key)
            exec_file_pd(s3obj)


def exec_file_pd(s3obj):
    body_in = s3obj.get()['Body'].read().decode('utf-8')
    buffer_in = io.StringIO(body_in)
    df_in = pd.read_csv(buffer_in, lineterminator='\n', header=None)
    logger.debug('df_in')
    logger.debug(df_in)
    # ここで編集　カラム３が1000以上のみにする
    df_out = df_in[df_in[3] > 1000]
    logger.debug('df_out')
    logger.debug(df_out)
    # 書き込み
    buffer_out = io.StringIO()
    df_out.to_csv(buffer_out, index=False)
    body_out = buffer_out.getvalue()
    dest_obj = s3.Object(bucket_name, s3obj.key+'.out')
    dest_obj.put(Body=body_out)
    logger.info('output file = '+dest_obj.key)


if __name__ == "__main__":
    bucket = lambda_handler({'datakey': 'datakey'}, '')
