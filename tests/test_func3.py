import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
from src import func3


class TestFunc3(unittest.TestCase):
    def test_handler(self):
        """正常ケース
        """
        event = {'target_month': '7'}
        context = ''
        res = func3.lambda_handler(event, context)
        # 結果件数のチェック
        self.assertEqual(res, 11)

    def test_exec(self):
        """正常ケース
        """
        df = func3.exec('7')
        # 結果件数のチェック
        self.assertEqual(df.shape[0], 11)


if __name__ == '__main__':
    unittest.main()
