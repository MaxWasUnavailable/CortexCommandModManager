from logging import getLogger, StreamHandler, FileHandler, Formatter, DEBUG, INFO, WARNING, ERROR, CRITICAL

logger = None


def init_logger(file_path=None, level=DEBUG):
    global logger

    logger = getLogger("Cortex Command Mod Manager")
    logger.setLevel(DEBUG)

    formatter = Formatter("[%(asctime)s] %(name)s | %(levelname)s | %(message)s", "%Y-%m-%d %H:%M:%S")

    stream_handler = StreamHandler()
    stream_handler.setLevel(level)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    if file_path is not None:
        file_handler = FileHandler(file_path, mode="w")
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    logger.debug("Logger initialized")

    return logger


def get_logger():
    if logger is None:
        init_logger()
    return logger


if __name__ == '__main__':
    init_logger("log.txt", DEBUG)
    logger = get_logger()

    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
    logger.critical("Critical message")
