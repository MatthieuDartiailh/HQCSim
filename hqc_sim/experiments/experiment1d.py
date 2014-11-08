# -*- coding: utf-8 -*-
"""
"""
import logging
import enaml
import cPickle
from atom.api import Dict, Str, Bool, List, Value
from enaml.layout.api import InsertItem

from ..utils.has_pref_atom import HasPrefAtom, tagged_members
from ..models.abstract_model import Varying
with enaml.imports():
    from .experiment1d_panel import Experiment1DItem


class Experiment1D(HasPrefAtom):
    """
    """
    #: Name of the experiment used for identification purposes.
    name = Str().tag(pref=True)

    #: Reference to the view for which this acts as a controller (needed for
    #: persistence purposes mainly).
    view = Value()

    #: Object describing the whole physic of the simulated model.
    model = Value().tag(pref=True)

    # Here store plots.
    plots = List()

    # Name of the attribute of the sq model used as x axis.
    x_axis = Str().tag(pref=True)

    #: List of the parameters used to manipulate the graph
    manipulate_vars = Dict().tag(pref=True)

    #: Metadata of the different variables as identified from the model.
    vars_meta = Dict()

    #: Main plottable data of the model.
    plottable_data = Dict()

    #: Flag indicating whether or not to aumatically update.
    auto_update = Bool()

    #:
    exp_class = Str().tag(pref=True)

    def request_recomputation(self, stage, size=False):
        """

        """
#        try:
        self.model.recompute(stage)
#        except Exception as e:
#            print e
#            err = 'Exp {} : recomputation failed : {}'.format(self.name, e)
#            logging.info(err)

    def get_data(self, member_name, indexes):
        """
        """
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

    def add_plot(self, plot, view, name=None):
        """
        """
        self.plots.append(plot)
        plot.x_axis = self.x_axis
        if not name:
            name = self._find_new_item_id()
            view.name = name
        view.set_parent(self.view.area)
        view.parent.update_layout(InsertItem(item=view.name, target='log',
                                             position='top'))

    def preferences_from_members(self):
        """
        """
        config = super(Experiment1D, self).preferences_from_members()
        for i, plot in enumerate(self.plots):
            config['plot_{}'.format(i)] = plot.preferences_from_members()

        layout = self.view.area.save_layout()
        config['plots_layout'] = cPickle.dumps(layout, 0).decode('latin1')

        return config

    @classmethod
    def build_experiment(cls, ccenter, name, model, area, config=None):
        """ Build a new experiment using the provided configuration.

        """
        exp = Experiment1D(model=model, name=name)
        exp.view = Experiment1DItem(area, exp=exp, name=name)
        if config:
            exp.update_members_from_preferences(config)
            exp.model.recompute()
            i = 0
            while True:
                aux = 'plot_{}'.format(i)
                i += 1
                if aux in config:
                    plot, view = ccenter.build_plot(config[aux]['plot_class'],
                                                    exp, config[aux])
                    exp.add_plot(plot, view)
                    continue
                break

            # Currently does not work
            try:
                layout = cPickle.loads(config['plots_layout'].encode('latin1'))
                exp.view.area.apply_layout(layout)
            except Exception:
                pass

        return exp

    def _post_setattr_model(self, old, new):
        """
        """
        if old:
            old.unobserve('recomputed', self._update_plots)
        if new:
            new.observe('recomputed', self._update_plots)
            adj_vars = tagged_members(new, 'stage')
            self.vars_meta = {k: {'varying': isinstance(getattr(new, k),
                                                        Varying),
                                  'stage': m.metadata['stage'],
                                  'label': m.metadata['label'],
                                  'desc': m.metadata['desc'],
                                  'def_range': m.metadata['def_range']}
                              for k, m in adj_vars.iteritems()}

            self.x_axis = sorted([k for k in self.vars_meta
                                  if self.vars_meta[k]['varying']])[0]

            plt_d = tagged_members(new, 'name')
            self.plottable_data = {m.metadata['name']:
                                   {'m_name': k,
                                    'symbol': m.metadata.get('symbol', k),
                                    'dim': m.metadata['dim'],
                                    'map': m.metadata.get('map'),
                                    'dtype': m.metadata.get('dtype', 'float')}
                                   for k, m in plt_d.iteritems()}

    def _post_setattr_x_axis(self, old, new):
        """
        """
        self.model.varyings = [new]
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

    def _find_new_item_id(self):
        """
        """
        area = self.view.area
        existing_ids = [item.name for item in area.dock_items()]
        for i in range(len(existing_ids)):
            aux = 'item_{}'.format(i)
            if aux not in existing_ids:
                return aux

        return 'item_{}'.format(len(existing_ids))

    def _default_exp_class(self):
        return self.__class__.__name__
