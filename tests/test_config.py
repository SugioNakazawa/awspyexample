import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
from src.utils import config


class TestConfig(unittest.TestCase):
    def test_getconfig_no_env(self):
        os.environ.pop('WFR_ENV', None)
        conf = config.get_config()
        self.assertEqual(conf.get('NAME'), 'DEFAULT')

    def test_getconfig_staging(self):
        os.environ['WFR_ENV'] = 'STAGING'
        conf = config.get_config()
        self.assertEqual(conf.get('NAME'), 'STAGING')

    def test_getconfig_production(self):
        os.environ['WFR_ENV'] = 'PRODUCTION'
        conf = config.get_config()
        self.assertEqual(conf.get('NAME'), 'PRODUCTION')