# -*- coding: utf-8 -*-
"""
Created on Wed Nov  5 11:19:06 2014

@author: dartiailh
"""
import numpy as np
from atom.api import (Atom, Str, Unicode, Tuple, Value)


# Here use a visitor pattern, where each infos know how to
# build the data by visiting the experiment.
class AbstractCurve1DInfos(Atom):
    """
    """
    id = Unicode()

    color = Value('auto')

    type = Value('line')

    def gather_data(self, experiment):
        """
        """
        raise NotImplementedError()


class SimpleCurve1DInfos(AbstractCurve1DInfos):
    """
    """
    m_name = Str()

    indexes = Tuple()

    def gather_data(self, experiment):
        """
        """
        if self.m_name:
            return experiment.get_data(self.m_name, self.indexes)

        return np.array([])


class SumCurve1DInfos(AbstractCurve1DInfos):
    """
    """
    pass


CURVE_INFOS = {SimpleCurve1DInfos: 'Simple', SumCurve1DInfos: 'Sum'}
