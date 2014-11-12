# -*- coding: utf-8 -*-
"""
Created on Thu Oct 30 18:36:06 2014

@author: dartiailh
"""
import enaml
import numba
import logging
import datetime
import sys
from enaml.qt.qt_application import QtApplication

from hqc_sim.control_center import ControlCenter
with enaml.imports():
    from hqc_sim.main_window import HQCSimWindow


class StreamToLogger(object):
    """
    Fake file-like stream object that redirects writes to a logger instance.
    """
    def __init__(self, logger, log_level=logging.INFO):
        self.logger = logger
        self.log_level = log_level
        self.linebuf = ''

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())

if __name__ == '__main__':
    filename = 'logs/hqc_sim{}.log'.format(datetime.datetime.now())
    f = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(filename=filename, level=logging.DEBUG,
                        format=f)

    # define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    # set a format which is simpler for console use
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    # tell the handler to use this format
    console.setFormatter(formatter)
    # add the handler to the root logger
    logging.getLogger('').addHandler(console)

    logging.captureWarnings(True)

    stderr_logger = logging.getLogger('STDERR')
    sl = StreamToLogger(stderr_logger, logging.ERROR)
    sys.stderr = sl

    logging.info('Logger parametrized')

    app = QtApplication()

    cc = ControlCenter()
    view = HQCSimWindow(model=cc)

    view.show()
    view.maximize()
    app.start()

    logging.info('Shutting down')
