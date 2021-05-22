from logging import getLogger
import boto3
import pandas as pd
import io

logger = getLogger('wfrpt.'+__name__)


class S3Util:
    """s3アクセスツール"""
    def __init__(self):
        self.s3 = boto3.resource('s3')

    def get_bucket(self, bucket_name):
        """bucket objectを取得。"""
        bucket = self.s3.Bucket(bucket_name)
        return bucket
    
    def get_s3_object(self, bucket_name, key):
        """s3 objectを取得。"""
        s3obj = self.s3.Object(bucket_name, key)
        return s3obj

    def get_df_from_s3object(self, s3obj):
        """csvのs3objectからpandas。DataFrameを生成。"""
        body_in = s3obj.get()['Body'].read().decode('utf-8')
        buffer_in = io.StringIO(body_in)
        df_in = pd.read_csv(buffer_in, lineterminator='\n', header=None)
        return df_in
    
    def put_s3_from_df(self, df_out, bucket_name, key):
        """pandas.DataFrameをs3へpurする。"""
        buffer_out = io.StringIO()
        df_out.to_csv(buffer_out, index=False)
        body_out = buffer_out.getvalue()
        dest_obj = self.s3.Object(bucket_name, key)
        dest_obj.put(Body=body_out)
        logger.debug('output file = '+dest_obj.key)
