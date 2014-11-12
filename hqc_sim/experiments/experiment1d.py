# -*- coding: utf-8 -*-
"""
"""
import logging
import enaml
import numpy as np
from atom.api import Str

from .base_experiment import BaseExperiment
with enaml.imports():
    from .experiment1d_panel import Experiment1DItem


class Experiment1D(BaseExperiment):
    """
    """
    #: Name of the attribute of the sq model used as x axis.
    x_axis = Str().tag(pref=True)

    def request_recomputation(self, stage, size=False):
        """

        """
        try:
            self.model.recompute(stage)
        except Exception as e:
            err = 'Exp {} : recomputation failed : {}'.format(self.name, e)
            logger = logging.getLogger(__name__)
            logger.error(err)

    def get_data(self, member_name, indexes):
        """
        """
        if not self.model.initialized:
            return np.array([])
        if not self.model.hyste:
            if len(indexes) == 1:
                i, = indexes
                return getattr(self.model, member_name)[:, i]
            elif len(indexes) == 0:
                return getattr(self.model, member_name)[:]
            elif len(indexes) == 2:
                i, j = indexes
                return getattr(self.model, member_name)[:, i, j]
        else:
            raise NotImplementedError()

    @classmethod
    def build_view(cls, name, exp, area):
        """ Build a new experiment using the provided configuration.

        """
        return Experiment1DItem(area, exp=exp, name=name)

    def _set_plot_axis(self, plot):
        """
        """
        plot.x_axis = self.vars_meta[self.x_axis]['label']

    def _post_setattr_model(self, old, new):
        """
        """
        super(Experiment1D, self)._post_setattr_model(old, new)

        if new:
            self.x_axis = sorted([k for k in self.vars_meta
                                  if self.vars_meta[k]['varying']])[0]

    def _post_setattr_x_axis(self, old, new):
        """
        """
        self.model.varyings = [new]
        # This should be handled at the plot level (thinking of permutted axis)
        for plot in self.plots:
            plot.x_axis = self.vars_meta[new]['label']
        if self.auto_update:
            self.request_recomputation('field', True)

    def _update_plots(self, sig):
        """
        """
        stage, size = sig
        model = self.model
        if size:
            x = getattr(model, self.x_axis).linspace
        for plot in self.plots:
            if size:
                plot.data.set_data('x', x)
            plot.update_data(stage)
