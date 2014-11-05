# -*- coding: utf-8 -*-
"""
"""
from chaco.api import Plot, ArrayPlotData
from atom.api import (Atom, Typed, List, Str, ForwardTyped)

from .curves import AbstractCurve1DInfos


def exp1d():
    from ..experiments.experiment1d import Experiment1D
    return Experiment1D


class Plot1D(Atom):
    """
    """
    #: Reference to the experiment managing this plot.
    experiment = ForwardTyped(exp1d)

    #: Data actually driving the plot.
    data = Typed(ArrayPlotData, ())

    #: Chaco component doing the heavy work.
    renderer = Typed(Plot, ())

    #: Name of the x axis currently used.
    x_name = Str()

    #: Infos caracterising the plotted data.
    #: Should not be manipulated by user code.
    y_infos = List(AbstractCurve1DInfos)

    def __init__(self, **kwargs):
        super(Plot1D, self).__init__(**kwargs)
        self.renderer.data = self.data
        exp = self.experiment
        self.data.set_data('x', getattr(exp.model, exp.x_axis).linspace)
        # Add basic tools and ways to activate them in public API

    def add_curves(self, curves):
        """
        """
        self.y_infos.extend(curves)
        self._update_graph(added=curves)

    def remove_curves(self, curves):
        """
        """
        for c in curves:
            self.y_infos.remove(c)
        self._update_graph(removed=curves)

    def replace_curve(self, old, new):
        """
        """
        self.y_infos.remove(old)
        self.y_infos.append(new)
        self._update_graph([new], [old])

    # For the time being stage is unused (will try to refine stuff if it is
    # needed)
    def update_data(self, stage):
        """
        """
        exp = self.experiment
        for info in self.y_infos:
            data = info.gather_data(exp)
            self.data.set_data(info.id, data)

    def _update_graph(self, added=[], removed=[]):
        """
        """
        exp = self.experiment
        for a in added:
            y_data = a.gather_data(exp)
            name = a.id
            self.data.set_data(name, y_data)
            self.renderer.plot(('x', name), name=name, type=a.type,
                               color=a.color)

        self.renderer.delplot(*removed)
        for r in removed:
            self.data.del_data(r.id)
