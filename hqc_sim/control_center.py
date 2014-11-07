# -*- coding: utf-8 -*-
"""
"""
from atom.api import Atom, ContainerList, Str, Dict, List
from configobj import ConfigObj
from .experiments import EXPERIMENTS
from .plotting import PLOTS
from .models.factories import FACTORIES as M_FACTORIES


class ControlCenter(Atom):
    """
    """

    experiments = Dict(Str(), default={e.__name__: e for e in EXPERIMENTS})

    running_exps = ContainerList()

    models = List(Str(), M_FACTORIES.keys())

    def build_experiment(self, name, exp_type, model_type, area, config=None):
        """
        """
        model = M_FACTORIES[model_type][1]()
        exp = self.experiments[exp_type].build_experiment(self, name, model,
                                                          area, config)
        self.running_exps.append(exp)
        return exp, exp.view

    def save_experiment(self, path, experiment):
        """
        """
        conf = ConfigObj(experiment.preferences_from_members(),
                         encoding='utf8')
        with open(path, 'wb') as f:
            conf.write(f)

    def load_experiment(self, path, area):
        """
        """
        conf = ConfigObj(path, default_encoding='utf8')
#        try:
        models = {v[0]: v[1] for v in M_FACTORIES.values()}
        model = models[conf['model']['model_class']]()
        exp_class = [e for e in EXPERIMENTS
                     if e.__name__ == conf['exp_class']][0]
        name = conf.pop('name')
        if name in [e.name for e in self.running_exps]:
            name = self.default_exp_name()
        exp = exp_class.build_experiment(self, name, model,
                                         area, conf)

        self.running_exps.append(exp)
        return exp, exp.view

#        except Exception as e:
#            print e
#            return None, None

    def destroy_experiment(self, exp):
        """
        """
        self.running_exps.remove(exp)

    def default_exp_name(self):
        """
        """
        i = 0
        def_name = 'Experiment {}'
        exp_names = [e.name for e in self.running_exps]
        while True:
            if def_name.format(i) not in exp_names:
                return def_name.format(i)
            i += 1

    def build_plot(self, class_name, exp, config):
        """
        """
        cls = PLOTS[class_name]
        new, view = cls.build_plot(exp, config)
        return new, view

    # Should also implement persistence.
