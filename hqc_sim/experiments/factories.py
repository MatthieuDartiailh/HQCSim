# -*- coding: utf-8 -*-
"""

"""
import enaml

from .experiment1d import Experiment1D
with enaml.imports():
    from .experiment1d_panel import Experiment1DItem

FACTORIES = {}


def experiment_1d(name, model, ccenter, area):

    exp = Experiment1D(model=model, name=name)
    return exp, Experiment1DItem(area, exp=exp, name=name)

FACTORIES["Experiment 1D"] = experiment_1d
