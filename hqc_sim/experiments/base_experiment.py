# -*- coding: utf-8 -*-
"""
"""
import cPickle
from atom.api import Dict, Str, Bool, List, Value
from enaml.layout.api import InsertItem

from ..utils.has_pref_atom import HasPrefAtom, tagged_members
from ..models.abstract_model import Varying


class BaseExperiment(HasPrefAtom):
    """
    """
    #: Name of the experiment used for identification purposes.
    name = Str().tag(pref=True)

    #: Reference to the view for which this acts as a controller (needed for
    #: persistence purposes mainly).
    view = Value()

    #: Object describing the whole physic of the simulated model.
    model = Value().tag(pref=True)

    #: Here store plots.
    plots = List()

    #: List of the parameters used to manipulate the graph
    manipulate_vars = Dict().tag(pref=True)

    #: Metadata of the different variables as identified from the model.
    vars_meta = Dict()

    #: Main plottable data of the model.
    plottable_data = Dict()

    #: Flag indicating whether or not to aumatically update.
    auto_update = Bool()

    #: Class of the experiment used for persistence purposes.
    exp_class = Str().tag(pref=True)

    def request_recomputation(self, stage, size=False):
        """

        """
        raise NotImplementedError()

    def get_data(self, member_name, indexes):
        """

        """
        raise NotImplementedError()

    def add_plot(self, plot, view, name=None):
        """
        """
        self.plots.append(plot)
        self._set_plot_axis(plot)
        if not name:
            name = self._find_new_item_id()
            view.name = name
        view.set_parent(self.view.area)
        view.parent.update_layout(InsertItem(item=view.name, target='log',
                                             position='top'))

    def preferences_from_members(self):
        """
        """
        config = super(BaseExperiment, self).preferences_from_members()
        for i, plot in enumerate(self.plots):
            config['plot_{}'.format(i)] = plot.preferences_from_members()

        layout = self.view.area.save_layout()
        config['plots_layout'] = cPickle.dumps(layout, 0).decode('latin1')

        return config

    @classmethod
    def build_experiment(cls, ccenter, name, model, area, config=None):
        """ Build a new experiment using the provided configuration.

        """
        exp = cls(model=model, name=name)
        if config:
            exp.update_members_from_preferences(config)
            exp.model.recompute()

        exp.view = cls.build_view(name, exp, area)

        if config:
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

            plt_d = tagged_members(new, 'name')
            self.plottable_data = {m.metadata['name']:
                                   {'m_name': k,
                                    'symbol': m.metadata.get('symbol', k),
                                    'dim': m.metadata['dim'],
                                    'map': m.metadata.get('map'),
                                    'dtype': m.metadata.get('dtype', 'float')}
                                   for k, m in plt_d.iteritems()}

            for met in self.plottable_data.values():
                if isinstance(met['map'], callable):
                    met['map'] = met['map'](new)

    def _set_plot_axis(self, plot):
        """
        """
        raise NotImplementedError()

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
