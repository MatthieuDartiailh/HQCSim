# -*- coding: utf-8 -*-
"""
"""
import numpy as np
from atom.api import (Str, Unicode, Tuple, List, Enum)
from ..utils.has_pref_atom import HasPrefAtom


# Here use a visitor pattern, where each infos know how to
# build the data by visiting the experiment.
class AbstractInfo(HasPrefAtom):
    """
    """
    id = Unicode().tag(pref=True)

    info_class = Str().tag(pref=True)

    def make_header(self, experiment):
        """Make a header line describing the plotted quantities.

        """
        raise NotImplementedError()

    def gather_data(self, experiment):
        """
        """
        raise NotImplementedError()

    def _default_info_class(self):
        return self.__class__.__name__


class SimpleInfo(AbstractInfo):
    """
    """
    m_name = Str().tag(pref=True)

    indexes = Tuple().tag(pref=True)

    part = Enum('float', 'real', 'imag', 'mag', 'phase').tag(pref=True)

    def make_header(self, experiment):
        """
        """
        h = 'Simple ' + self.m_name
        if self.part != 'float':
            h += ' ' + self.part
        return h

    def gather_data(self, experiment):
        """
        """
        if self.m_name:
            data = experiment.get_data(self.m_name, self.indexes)
            if self.part == 'float':
                return data
            elif self.part == 'real':
                return np.real(data)
            elif self.part == 'imag':
                return np.imag(data)
            elif self.part == 'mag':
                return np.abs(data)
            else:
                return np.angle(data, True)

        return np.array([])


class SumInfo(AbstractInfo):
    """
    """
    m_name = Str().tag(pref=True)

    indexes = List(Tuple()).tag(pref=True)

    part = Enum('float', 'real', 'imag', 'mag', 'phase').tag(pref=True)

    def make_header(self, experiment):
        """
        """
        metas = {m['m_name']: m for m in experiment.plottable_data.values()}
        meta = metas[self.m_name]['map']
        name = (self.m_name if self.part == 'float'
                else self.m_name + ' ' + self.part)
        h = 'Sum {} : {}'.format(name, [meta[i[0]]
                                        for i in sorted(self.indexes)])
        return h

    def gather_data(self, experiment):
        """
        """
        if self.m_name:
            data = 0
            data += reduce(np.add, [experiment.get_data(self.m_name, index)
                                    for index in self.indexes])
            if self.part == 'float':
                return data
            elif self.part == 'real':
                return np.real(data)
            elif self.part == 'imag':
                return np.imag(data)
            elif self.part == 'mag':
                return np.abs(data)
            else:
                return np.angle(data, True)

        return np.array([])

DATA_INFOS = {SimpleInfo: 'Simple', SumInfo: 'Sum'}
