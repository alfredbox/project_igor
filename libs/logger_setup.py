import logging
import time


def setup():
    logging.basicConfig(filename='logs/igor_log_{}.log'.format(
                        time.strftime('%Y-%m-%d-%H-%M-%S')))


def get_logger():
    l = logging.getLogger('igor')
    l.setLevel(logging.DEBUG)
    return l
