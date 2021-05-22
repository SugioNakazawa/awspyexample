from logging import getLogger, StreamHandler, Formatter
from utils.config import get_config


class MyLogger:
    """logging.gloggerのWrapperクラス
    出力メッセージを共通的に変換可能にする。ただし、strのみ。
    """

    logger = None

    def __init__(self, name):
        """定数 LOG_STREAM=LOCALの時のみStreamHandlerを付加する。
        """
        log_level = get_config().get('LOG_LEVEL', 'INFO')
        self.logger = getLogger(name)
        self.logger.setLevel(log_level)
        if (get_config().get('LOGGER_HANDLER', 'LAMBDA') == 'LOCAL'):
            # for execute on local
            handler = StreamHandler()
            handler.setLevel(log_level)
            # option
            format = Formatter(
                '%(asctime)-15s %(name)s %(levelname)s %(message)s'
            )
            handler.setFormatter(format)
            self.logger.addHandler(handler)

    def error(self, msg):
        self.logger.error(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def info(self, msg):
        self.logger.info(msg)

    def debug(self, msg):
        self.logger.debug(msg)
