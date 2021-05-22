from utils.config import get_config
from utils.mylogger import MyLogger
from utils.s3util import S3Util

# 定数
conf = get_config()
# ロガー
logger = MyLogger('wfrpt')

s3util = S3Util()
bucket_name = conf.get('bucket_name')


def lambda_handler(event, context):
    """key=datakey で渡されたディレクトリ（S3オブジェクトの接頭）にマッチする
    オブジェクト（CSVファイル）を取得し、変換してS3に同じファイルで出力（上書き）する。

    Args:
        event['datakey']: 処理対象とするファイルの格納フォルダ名
    
    Returns:
        None
    """
    preffix = event['datakey']
    execute(preffix)


def execute(preffix):
    """指定ディレクトリ内のcsvファイルを変換してs3へ出力。
    """
    bucket = s3util.get_bucket(bucket_name)
    logger.debug('bucket name = ' + bucket.name)
    for obj in bucket.objects.all():
        if (obj.key.startswith(preffix)
                and len(obj.key) > len(preffix) + 1
                and obj.key.endswith('.csv')):
            logger.info('read file = ' + obj.key)
            # s3obj = s3.Object(bucket_name, obj.key)
            s3obj = s3util.get_s3_object(bucket_name, obj.key)
            exec_file_pd(s3obj)


def exec_file_pd(s3obj):
    df_in = s3util.get_df_from_s3object(s3obj)
    logger.debug('df_in = ')
    logger.debug(df_in)
    # ここで編集　カラム３が1000以上のみにする
    df_out = df_in[df_in[3] > 1000]
    logger.debug('df_out')
    logger.debug(df_out)
    # 書き込み
    s3util.put_s3_from_df(df_out, bucket_name, s3obj.key+'.out')
