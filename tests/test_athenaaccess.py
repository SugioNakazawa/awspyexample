import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
from src.utils.athenaaccess import AthenaAccess
from src.utils import athenaaccess


class TestAthena(unittest.TestCase):

    @classmethod
    def tearDownClass(cls):
        """他のテストケースのためRETRY_COUNTを100にもどす
        """
        athenaaccess.RETRY_COUNT = 100

    def test_execute(self):
        """正常SQL
        """
        obj = AthenaAccess()
        sql = "select year,month,day,ave,max,min from dev_table where month=1"
        res = obj.execute(sql)
        # 行列の数でチェック
        self.assertEqual(res.shape, (311, 6))

    def test_execute_err_sql(self):
        """SQLエラーのチェック。
        """
        with self.assertRaises(Exception, msg='STATUS:FAILED'):
            obj = AthenaAccess()
            sql = "select year,month,day,ave,max,min from hoge where month=1"
            obj.execute(sql)

    def test_execute_err_timeover(self):
        """SQLタイムオーバー
        """
        with self.assertRaises(Exception, msg='TIME OVER athena query'):
            obj = AthenaAccess()
            athenaaccess.RETRY_COUNT = 1
            sql = "select year,month,day,ave,max,min from dev_table where day=5"
            obj.execute(sql)
