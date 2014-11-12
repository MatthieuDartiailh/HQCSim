# -*- coding: utf-8 -*-
"""
"""
import enaml
from chaco.api import Plot
from atom.api import (List, Str)

from ..base_plot import BasePlot
from .curves import CURVE_INFOS
with enaml.imports():
    from .plot_views import Plot1DItem


def exp1d():
    from ...experiments.experiment1d import Experiment1D
    return Experiment1D


class Plot1D(BasePlot):
    """
    """
    #: Name of the x axis used for labelling the plot.
    x_axis = Str()

    #: Infos caracterising the plotted data.
    #: Should not be manipulated by user code.
    y_infos = List()

    def __init__(self, **kwargs):
        super(Plot1D, self).__init__(**kwargs)
        self.renderer = Plot()
        self.renderer.data = self.data
        exp = self.experiment
        self.data.set_data('x', getattr(exp.model, exp.x_axis).linspace)
        # Add basic tools and ways to activate them in public API

    @classmethod
    def build_view(cls, plot):
        """
        """
        return Plot1DItem(plot=plot)

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

    def preferences_from_members(self):
        """
        """
        d = super(Plot1D, self).preferences_from_members()
        for i, c in enumerate(self.infos):
            d['curve_{}'.format(i)] = c.preferences_from_members()

        return d

    def update_members_from_preferences(self, config):
        """
        """
        super(Plot1D, self).update_members_from_preferences(config)
        infos = []
        i = 0
        while True:
            aux = 'curve_{}'.format(i)
            i += 1
            if aux in config:
                c_config = config[aux]
                curve = [c for c in CURVE_INFOS
                         if c.__name__ == c_config['curve_class']][0]()
                curve.update_members_from_preferences(c_config)
                infos.append(curve)
                continue
            break

        self.add_curves(infos)

    def _update_graph(self, added=[], removed=[]):
        """
        """
        exp = self.experiment
        # First we clean the old graphs
        self.renderer.delplot(*[c.id for c in removed])
        for r in removed:
            self.data.del_data(r.id)

        # Then we add new ones (this avoids messing up when replacing a graph)
        for a in added:
            y_data = a.gather_data(exp)
            name = a.id
            self.data.set_data(name, y_data)
            self.renderer.plot(('x', name), name=name, type=a.type,
                               color=a.color)

    def _post_setattr_x_axis(self, old, new):
        """
        """
        self.renderer.x_axis.title = new

    def _default_renderer(self):
        return Plot()
