# -*- coding: utf-8 -*-
"""

"""

FACTORIES = {}


def spin_q_fac():
    from .spin_qubit_model import OddSQModel
    return OddSQModel()

FACTORIES = {'Spin Qubit odd': spin_q_fac}
