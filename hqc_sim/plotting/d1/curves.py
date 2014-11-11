# -*- coding: utf-8 -*-
"""
"""
from atom.api import (Str)
from ...utils.has_pref_atom import HasPrefAtom
from ..data_infos import SimpleInfo, SumInfo


# Here use a visitor pattern, where each infos know how to
# build the data by visiting the experiment.
class CurveMixin(HasPrefAtom):
    """
    """
    color = Str('auto').tag(pref=True)

    type = Str('line').tag(pref=True)


class SimpleCurve1DInfos(CurveMixin, SimpleInfo):
    """
    """
    pass


class SumCurve1DInfos(CurveMixin, SumInfo):
    """
    """
    pass

CURVE_INFOS = {SimpleCurve1DInfos: 'Simple', SumCurve1DInfos: 'Sum'}
