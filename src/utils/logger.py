from logging import getLogger, StreamHandler, Formatter


def get_logger(name, log_level):
    '''各関数のLoggerの初期化を共通化
    '''
    logger = getLogger(name)
    logger.setLevel(log_level)
    logger.propagate = False

    handler = StreamHandler()
    handler.setLevel(log_level)
    logger.addHandler(handler)

    format = Formatter('%(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(format)

    return logger