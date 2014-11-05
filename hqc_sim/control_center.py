# -*- coding: utf-8 -*-
"""
"""

from atom.api import Atom, List, Str
from .experiments.factories import FACTORIES as E_FACTORIES
from .models.factories import FACTORIES as M_FACTORIES


class ControlCenter(Atom):
    """
    """
    experiments = List(Str(), E_FACTORIES.keys())

    running_exps = List()

    models = List(Str(), M_FACTORIES.keys())

    def create_experiment(self, name, exp_type, model_type, area):
        """
        """
        model = M_FACTORIES[model_type]()
        exp, view = E_FACTORIES[exp_type](name, model, self, area)

        self.running_exps.append(exp)
        return exp, view

    def destroy_experiment(self, exp):
        """
        """
        self.running_exps.remove(exp)

    # Should also implement persistence.
