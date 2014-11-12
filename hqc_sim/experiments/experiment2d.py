# -*- coding: utf-8 -*-
"""
"""
import logging
import enaml
import numpy as np
from atom.api import Str
from .base_experiment import BaseExperiment

with enaml.imports():
    from .experiment2d_view import Experiment2DItem


class Experiment2D(BaseExperiment):
    """
    """
    #: Name of the attribute of the sq model used as x axis.
    x_axis = Str().tag(pref=True)

    #: Name of the attribute of the sq model used as y axis.
    y_axis = Str().tag(pref=True)

    def request_recomputation(self, stage, size=False):
        """

        """
        try:
            self.model.recompute(stage)
        except Exception as e:
            print e
            err = 'Exp {} : recomputation failed : {}'.format(self.name, e)
            logging.info(err)
            print

    def get_data(self, member_name, indexes):
        """
        """
        if not self.model.initialized:
            return np.zeros((2, 2))
        if not self.model.hyste:
            if len(indexes) == 1:
                i, = indexes
                return getattr(self.model, member_name)[:, :, i]
            elif len(indexes) == 0:
                return getattr(self.model, member_name)[:, :]
            elif len(indexes) == 2:
                i, j = indexes
                return getattr(self.model, member_name)[:, :, i, j]
        else:
            raise NotImplementedError()

    @classmethod
    def build_view(cls, name, exp, area):
        """ Build a new experiment using the provided configuration.

        """
        return Experiment2DItem(area, exp=exp, name=name)

    def _set_plot_axis(self, plot):
        """
        """
        plot.x_axis = self.vars_meta[self.x_axis]['label']
        plot.y_axis = self.vars_meta[self.y_axis]['label']

    def _post_setattr_model(self, old, new):
        """
        """
        super(Experiment2D, self)._post_setattr_model(old, new)

        if new:
            names = sorted([k for k in self.vars_meta
                            if self.vars_meta[k]['varying']])
            self.x_axis = names[0]
            self.y_axis = names[1]

    def _post_setattr_x_axis(self, old, new):
        """
        """
        self.model.varyings = [new, self.y_axis]
        for plot in self.plots:
            plot.x_axis = self.vars_meta[new]['label']
        if self.auto_update:
            self.request_recomputation('field', True)

    def _post_setattr_y_axis(self, old, new):
        """
        """
        self.model.varyings = [self.x_axis, new]
        for plot in self.plots:
            plot.y_axis = self.vars_meta[new]['label']
        if self.auto_update:
            self.request_recomputation('field', True)

    def _update_plots(self, sig):
        """
        """
        stage, size = sig
        model = self.model
        if size:
            x = getattr(model, self.x_axis).linspace
            y = getattr(model, self.y_axis).linspace
        for plot in self.plots:
            if size:
                plot.x_min = x[0]
                plot.x_max = x[-1]
                plot.y_min = y[0]
                plot.y_max = y[-1]
            plot.update_data(stage)
