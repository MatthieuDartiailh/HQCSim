# -*- coding: utf-8 -*-
"""
Created on Wed Nov  5 11:19:06 2014

@author: dartiailh
"""
import numpy as np
from atom.api import (Str, Unicode, Tuple, List, Enum)
from ...utils.has_pref_atom import HasPrefAtom


# Here use a visitor pattern, where each infos know how to
# build the data by visiting the experiment.
class AbstractCurve1DInfos(HasPrefAtom):
    """
    """
    id = Unicode().tag(pref=True)

    color = Str('auto').tag(pref=True)

    type = Str('line').tag(pref=True)

    curve_class = Str().tag(pref=True)

    def gather_data(self, experiment):
        """
        """
        raise NotImplementedError()

    def _default_curve_class(self):
        return self.__class__.__name__


class SimpleCurve1DInfos(AbstractCurve1DInfos):
    """
    """
    m_name = Str().tag(pref=True)

    indexes = Tuple().tag(pref=True)

    part = Enum('float', 'real', 'imag').tag(pref=True)

    def gather_data(self, experiment):
        """
        """
        if self.m_name:
            data = experiment.get_data(self.m_name, self.indexes)
            if self.part == 'float':
                return data
            elif self.part == 'real':
                return np.real(data)
            else:
                return np.imag(data)

        return np.array([])


class SumCurve1DInfos(AbstractCurve1DInfos):
    """
    """
    m_name = Str().tag(pref=True)

    indexes = List(Tuple()).tag(pref=True)

    part = Enum('float', 'real', 'imag').tag(pref=True)

    def gather_data(self, experiment):
        """
        """
        if self.m_name:
            data = 0
            for index in self.indexes:
                data += experiment.get_data(self.m_name, index)
            if self.part == 'float':
                return data
            elif self.part == 'real':
                return np.real(data)
            else:
                return np.imag(data)

        return np.array([])


CURVE_INFOS = {SimpleCurve1DInfos: 'Simple', SumCurve1DInfos: 'Sum'}
