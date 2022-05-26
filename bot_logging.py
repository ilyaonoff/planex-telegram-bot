import logging


def _create_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    log_formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(filename)s:%(funcName)s:%(message)s')
    file_handler = logging.FileHandler('bot.log')
    file_handler.setFormatter(log_formatter)
    logger.addHandler(file_handler)
    return logger


logger = _create_logger()
