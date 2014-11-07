# -*- coding: utf-8 -*-
"""
Created on Thu Oct 30 18:36:06 2014

@author: dartiailh
"""
import enaml
import numba
from enaml.qt.qt_application import QtApplication

from hqc_sim.control_center import ControlCenter
with enaml.imports():
    from hqc_sim.main_window import HQCSimWindow


if __name__ == '__main__':

    app = QtApplication()

    cc = ControlCenter()
    view = HQCSimWindow(model=cc)

    view.show()
#    view.maximize()
    app.start()
