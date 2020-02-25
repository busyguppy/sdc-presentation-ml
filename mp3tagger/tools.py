import logging
from os.path import dirname, join

PROJECT_DIRECTORY = dirname(dirname(__file__))


def path(*path):
    return join(PROJECT_DIRECTORY, *path).replace("\\", "/")


def temp_file(filename):
    return join(tempdir, filename).replace("\\", "/")


def data_file(filename):
    return join(datadir, filename).replace("\\", "/")


def __setup_custom_logger(name, level):
    formatter = logging.Formatter(fmt='[DEBUG][%(module)s] %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger


logger = __setup_custom_logger('root', level=logging.DEBUG)
datadir = path('data')
tempdir = path('temp')
