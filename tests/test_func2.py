import unittest
import boto3
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

from src import func2
from src.utils.config import get_config


class TestFunc2(unittest.TestCase):

    # bucket_name = 'sanmle-bucket-' + str(uuid.uuid4())    # バケットを自動作成する場合の名前
    conf = get_config()
    csv_file_name = 'datakey/data1.csv'
    bucket_name = conf.get('BUCKET_NAME')

    @classmethod
    def setUpClass(cls):
        # バケットを作成するケース
        # s3 = boto3.client('s3')
        # s3.create_bucket(Bucket=TestFunction2.bucket_name, CreateBucketConfiguration={
        #                  'LocationConstraint': 'ap-northeast-1'})

        # datakey/data1.csv をアップロード
        s3 = boto3.resource('s3')
        upload_file = __file__.replace('test_func2.py','datas/data1.csv')
        print(upload_file)
        s3.Object(TestFunc2.bucket_name, TestFunc2.csv_file_name).upload_file(
            upload_file)
        print('upload s3 object = ' + TestFunc2.csv_file_name)

    @classmethod
    def tearDownClass(cls):
        # 作ったバケットの削除
        # s3 = boto3.client('s3')
        # response = s3.delete_bucket(Bucket=TestFunction2.bucket_name)

        # アップロードしたdata1.csvを削除
        # client = boto3.client('s3')
        # client.delete_object(Bucket=TestFunc2.conf.get(
        #     'BUCKET_NAME'), Key=TestFunc2.csv_file_name)
        print('delete s3 object = ' + TestFunc2.csv_file_name)

    def test_lambda_handler(self):
        """ケース1 正常系テスト
        """
        func2.lambda_handler({'datakey': 'datakey'}, {'key2', 'value2'})
        # 結果ファイルの確認
        s3 = boto3.resource('s3')
        obj = s3.Object(TestFunc2.bucket_name,
                        TestFunc2.csv_file_name+'.out').get()
        body_in = obj['Body'].read().decode('utf-8')
        self.assertEqual(body_in, '0,1,2,3\nB,2,2.2,2000\nC,3,3.3,3000\n')

    # def test_execute(self):
    #     try:
    #         function2.execute('nhk')
    #         self.fail()
    #     except ValueError as err:
    #         print(err)
    #         self.assertEqual(str(err), 'not exist file, suffix = nhk')


if __name__ == '__main__':
    unittest.main()
