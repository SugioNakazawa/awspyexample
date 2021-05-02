from logging import getLogger, StreamHandler, Formatter


def get_logger(name, log_level):
    logger = getLogger(name)
    logger.setLevel(log_level)
    logger.propagate = False

    handler = StreamHandler()
    handler.setLevel(log_level)
    logger.addHandler(handler)

    format = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(format)

    return logger
