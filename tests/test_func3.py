import unittest
from unittest import mock
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
from src import func3


class TestFunc3(unittest.TestCase):
    def test_sample(self):
        df = func3.exec('7')
        # 結果件数のチェック
        self.assertEqual(df.shape[0], 11)


if __name__ == '__main__':
    unittest.main()
