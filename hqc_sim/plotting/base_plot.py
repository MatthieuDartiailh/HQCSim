# -*- coding: utf-8 -*-
"""
"""
from chaco.api import ArrayPlotData
from atom.api import (Typed, Value, ForwardTyped, Str)

from ..utils.has_pref_atom import HasPrefAtom


def exp():
    from ..experiments.base_experiment import BaseExperiment
    return BaseExperiment


class BasePlot(HasPrefAtom):
    """
    """
    #: Name identifying this plot.
    name = Str().tag(pref=True)

    #: Reference to the experiment managing this plot.
    experiment = ForwardTyped(exp)

    #: Data actually driving the plot.
    data = Typed(ArrayPlotData, ())

    #: Chaco component doing the heavy work.
    renderer = Value()

    #: Name of the class used for persistence purposes.
    plot_class = Str().tag(pref=True)

    @classmethod
    def build_plot(cls, exp, config=None):
        """
        """
        plot = cls(experiment=exp)
        if config:
            plot.update_members_from_preferences(config)
        view = cls.build_view(plot=plot)

        return plot, view

    @classmethod
    def build_view(cls, plot):
        """
        """
        raise NotImplementedError()

    def _default_plot_class(self):
        return self.__class__.__name__
