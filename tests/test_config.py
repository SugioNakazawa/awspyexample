import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
from src.utils import config  # noqa:E402


class TestConfig(unittest.TestCase):
    def test_getconfig_no_env(self):
        os.environ.pop('WFR_ENV', None)
        user = os.environ.get('USER')
        conf = config.get_config()
        self.assertEqual(conf.get('NAME'), 'DEFAULT')
        self.assertEqual(
            conf.get('BUCKET_NAME'),
            'com.nautilus-technologies.test.' + user)
        self.assertEqual(
            conf.get('ATHENA_DB_NAME'),
            'dev_database_' + user)
        self.assertEqual(
            conf.get('ATHENA_RESULT_BUCKET'),
            'com.nautilus-technologies.test.' + user)
        self.assertEqual(
            conf.get('ATHENA_DATA_BUCKET'),
            'com.nautilus-technologies.test.' + user)

    def test_getconfig_staging(self):
        os.environ['WFR_ENV'] = 'STAGING'
        conf = config.get_config()
        self.assertEqual(conf.get('NAME'), 'STAGING')
        self.assertEqual(
            conf.get('BUCKET_NAME'),
            'com.nautilus-technologies.test')
        self.assertEqual(
            conf.get('ATHENA_DB_NAME'), 'dev_database')
        self.assertEqual(
            conf.get('ATHENA_RESULT_BUCKET'),
            'com.nautilus-technologies.test')
        self.assertEqual(
            conf.get('ATHENA_DATA_BUCKET'),
            'com.nautilus-technologies.test')

    def test_getconfig_production(self):
        os.environ['WFR_ENV'] = 'PRODUCTION'
        conf = config.get_config()
        self.assertEqual(conf.get('NAME'), 'PRODUCTION')
        self.assertEqual(
            conf.get('BUCKET_NAME'),
            'com.nautilus-technologies.test')
        self.assertEqual(
            conf.get('ATHENA_DB_NAME'), 'dev_database')
        self.assertEqual(
            conf.get('ATHENA_RESULT_BUCKET'),
            'com.nautilus-technologies.test')
        self.assertEqual(
            conf.get('ATHENA_DATA_BUCKET'),
            'com.nautilus-technologies.test')
