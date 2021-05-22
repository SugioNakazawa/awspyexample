import unittest
import sys
import os
import logging
import pprint

sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
from src.utils.mylogger import MyLogger


class TestMyLogger(unittest.TestCase):
    def test_error(self):
        logger = logging.getLogger('TEST')
        mylogger = MyLogger(__name__)
        mylogger.logger = logger
        with self.assertLogs(logger=logger, level=logging.DEBUG) as cm:
            mylogger.error('ABCDEF')
        self.assertEqual(cm.output, ['ERROR:TEST:ABCDEF'])

    def test_warning(self):
        logger = logging.getLogger('TEST')
        mylogger = MyLogger(__name__)
        mylogger.logger = logger
        with self.assertLogs(logger=logger, level=logging.DEBUG) as cm:
            mylogger.warning('ABCDEF')
        self.assertEqual(cm.output, ['WARNING:TEST:ABCDEF'])

    def test_info(self):
        logger = logging.getLogger('TEST')
        mylogger = MyLogger(__name__)
        mylogger.logger = logger
        with self.assertLogs(logger=logger, level=logging.DEBUG) as cm:
            mylogger.info('ABCDEF')
        self.assertEqual(cm.output, ['INFO:TEST:ABCDEF'])

    def test_debug(self):
        logger = logging.getLogger('TEST')
        mylogger = MyLogger(__name__)
        mylogger.logger = logger
        with self.assertLogs(logger=logger, level=logging.DEBUG) as cm:
            mylogger.debug('ABCDEF')
        self.assertEqual(cm.output, ['DEBUG:TEST:ABCDEF'])

    def test_default_env(self):
        os.environ.pop('WFR_ENV', None)
        logger = MyLogger('DEFAULT')
        pprint.pprint(len(logger.logger.handlers))
        self.assertEqual(len(logger.logger.handlers), 1)

    def test_staging_env(self):
        os.environ['WFR_ENV'] = 'STAGING'
        logger = MyLogger('STAGING')
        pprint.pprint(len(logger.logger.handlers))
        self.assertEqual(len(logger.logger.handlers), 0)

    def test_production_env(self):
        os.environ['WFR_ENV'] = 'PRODUCTION'
        logger = MyLogger('PRODUCTION')
        pprint.pprint(len(logger.logger.handlers))
        self.assertEqual(len(logger.logger.handlers), 0)
