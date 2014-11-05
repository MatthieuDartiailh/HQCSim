# -*- coding: utf-8 -*-
"""
"""
import logging
from atom.api import Dict, Str, Bool, List, Value

from ..utils.has_pref_atom import HasPrefAtom, tagged_members
from ..models.spin_qubit_model import Varying


class Experiment1D(HasPrefAtom):
    """
    """
    #: Name of the experiment used for identification purposes.
    name = Str()

    #: Object describing the whole physic of the spinqubit.
    sqmodel = Value()

    # Here store plots.
    plots = List()

    # Name of the attribute of the sq model used as x axis.
    x_axis = Str()

    #: List of the parameters used to manipulate the graph
    manipulate_vars = Dict()

    #: Metadata of the different variables as identified from the sqmodel.
    vars_meta = Dict()

    #: Main plottable data of the sqmodel.
    plottable_data = Dict()

    #: Flag indicating whether or not to aumatically update.
    auto_update = Bool()

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

    def _post_setattr_sqmodel(self, old, new):
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
                                    'map': m.metadata.get('map')}
                                   for k, m in plt_d.iteritems()}

    def _post_setattr_x_axis(self, old, new):
        """
        """
        self.model.varyings = [new]
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


# OUTDATED STUFF (HOPEFULLY)

# TODO use Y for the name of the data
# TODO refactor to simply return data
#def _update_angle(y, model, plot, i):
#    """
#    """
#    if y.endswith('phi'):
#        if not model.hyste:
#            plot.data.set_data('y{}'.format(i), model.c_phi)
#        else:
#            plot.data.set_data('y{}'.format(i), model.c_phi[0])
#            plot.data.set_data('y{}d'.format(i), model.c_phi[1])
#    else:
#        if not model.hyste:
#            plot.data.set_data('y{}'.format(i), model.c_theta)
#        else:
#            plot.data.set_data('y{}'.format(i), model.c_theta[0])
#            plot.data.set_data('y{}d'.format(i), model.c_theta[1])
#
#
#def _update_energy(y, model, plot, i):
#    """
#    """
#    i = int(y[1])
#    if not model.hyste:
#        plot.data.set_data('y{}'.format(i), model.einenergies[:, i])
#    else:
#        plot.data.set_data('y{}'.format(i), model.einenergies[0][:, i])
#        plot.data.set_data('y{}d'.format(i), model.einenergies[1][:, i])
#
#
#def _update_frequency(y, model, plot, i):
#    """
#    """
#    i = int(y[1])
#    j = int(y[2])
#    eine = model.einenergies
#    if not model.hyste:
#        plot.data.set_data('y{}'.format(i), eine[:, j] - eine[:, i])
#    else:
#        plot.data.set_data('y{}'.format(i), eine[0][:, j] - eine[0][:, i])
#        plot.data.set_data('y{}d'.format(i), eine[1][:, j] - eine[1][:, i])
#
#
#MAP = {'01': 0, '02': 1, '03': 0, '12': 4, '13': 5, '23': 6}
#
#
#def _update_couplings(y, model, plot, i):
#    """
#    """
#    i = MAP[y[1:]]
#    if not model.hyste:
#        plot.data.set_data('y{}'.format(i), model.couplings[:, i])
#    else:
#        plot.data.set_data('y{}'.format(i), model.couplings[0][:, i])
#        plot.data.set_data('y{}d'.format(i), model.couplings[1][:, i])
#
#
#def _update_dephasing(y, model, plot, i):
#    """
#    """
#    i = MAP[y[1:]]
#    if not model.hyste:
#        plot.data.set_data('y{}'.format(i), model.dephasing_rates[:, i])
#    else:
#        plot.data.set_data('y{}'.format(i), model.couplings[0][:, i])
#        plot.data.set_data('y{}d'.format(i), model.couplings[1][:, i])
#
#
#def _update_susceptibilities(y, model, plot, i):
#    """
#    """
#    i = MAP[y[1:]]
#    if not model.hyste:
#        plot.data.set_data('y{}'.format(i), model.susceptibilities[:, i])
#    else:
#        plot.data.set_data('y{}'.format(i), model.susceptibilities[0][:, i])
#        plot.data.set_data('y{}d'.format(i), model.susceptibilities[1][:, i])
#
#
#HMAP = {'LU': 0, 'LD': 1, 'RU': 2, 'RD': 3}
#
#
#def _update_populations(y, model, plot, i):
#    """
#    """
#    i = int(y[1])
#    j = HMAP(y[-2:])
#    einv = model.eigenvectors
#    if not model.hyste:
#        plot.data.set_data('y{}'.format(i), einv[:, j, i]**2)
#    else:
#        plot.data.set_data('y{}'.format(i), einv[0][:, j, i]**2)
#        plot.data.set_data('y{}d'.format(i), einv[1][:, j, i]**2)
#
#DATA_MAP = {'S': lambda m: m.susceptibilities,
#            'G': lambda m: m.dephasing_rates,
#            'C': lambda m: m.couplings}
#
#
#def _update_sum(y, model, plot, i):
#    """
#    """
#    aux = y[4:].split('_')
#    data = DATA_MAP[aux[0][0]](model)
#    if not model.hyste:
#        p_data = np.zeros(data.shape[0])
#        for a in aux:
#            p_data += data[:, MAP[aux[1:]]]
#        plot.data.set_data(y.format(i), p_data)
#    else:
#        p_data_i = np.zeros(data[0].shape[0])
#        p_data_d = np.zeros(data[0].shape[0])
#        for a in aux:
#            p_data_i += data[0][:, MAP[aux[1:]]]
#            p_data_d += data[1][:, MAP[aux[1:]]]
#        plot.data.set_data(y.format(i), p_data_i)
#        plot.data.set_data(y + 'd'.format(i), p_data_d)
#
#UPDATERS = {'c': _update_angle, 'E': _update_energy,
#            'F': _update_frequency, 'G': _update_dephasing,
#            'C': _update_couplings, 'S': _update_susceptibilities,
#            'P': _update_populations, 's': _update_sum}
#
#
