import logging
import time


def setup(sim=False):
    subdir = '/sim' if sim else ''
    logging.basicConfig(filename='logs{}/igor_log_{}.log'.format(
                        subdir,
                        time.strftime('%Y-%m-%d-%H-%M-%S')))


def get_logger():
    l = logging.getLogger('igor')
    l.setLevel(logging.DEBUG)
    return l
