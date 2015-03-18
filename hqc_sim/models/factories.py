# -*- coding: utf-8 -*-
"""Collect all the factories defined in subpackages.

"""
import os
from importlib import import_module

FACTORIES = {}

dir_path = os.path.dirname(__file__)
for pack in os.listdir(dir_path):
    path = os.path.join(dir_path, pack)
    if os.path.isdir(path):
        if os.path.isfile(os.path.join(path, 'factories.py')):
            try:
                mod = import_module('.'+pack+'.factories', 'hqc_sim.models')
                FACTORIES.update(mod.FACTORIES)
            except ImportError:
                pass
