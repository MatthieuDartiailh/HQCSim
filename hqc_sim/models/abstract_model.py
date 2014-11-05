# -*- coding: utf-8 -*-
"""

"""
import numpy as np
from atom.api import Float, Property, Bool, Signal, List

from ..utils.has_pref_atom import HasPrefAtom


class Varying(HasPrefAtom):
    """ Specialized object used to represent a quantity which either be a
    number or an array.

    """
    #: Static value used when the varying is not varied.
    value = Float(1).tag(pref=True)

    #: Minimal value to use when varying.
    minimum = Float().tag(pref=True)

    #: Maximal value to use when varying.
    maximum = Float(10).tag(pref=True)

    #: Step to use when varying.
    step = Float(1).tag(pref=True)

    #: Number of points.
    points = Property(cached=True)

    #: Array of points.
    linspace = Property(cached=True)

    def __init__(self, value, **kwargs):
        super(Varying, self).__init__(**kwargs)
        self.value = value

    def _get_points(self):
        return int(round((self.maximum-self.minimum)/self.step)) + 1

    def _get_linspace(self):
        points = int(round((self.maximum-self.minimum)/self.step)) + 1
        return np.linspace(self.minimum, self.maximum, points)

    def _post_setattr_minimum(self, old, new):
        self._clear_cache()

    def _post_setattr_maximum(self, old, new):
        self._clear_cache()

    def _post_setattr_step(self, old, new):
        self._clear_cache()

    def _clear_cache(self):
        p = self.get_member('points')
        p.reset(self)
        p = self.get_member('linspace')
        p.reset(self)


class AbstractModel(HasPrefAtom):
    """ Base model for use in in HQCSim.

    The user should define the physical parameters of the problems using either
    usual members or Typed(Varying). Those paarmeters should be tagged with
    pref=True, a label (specifying their unit), a desc giving further infos,
    a stage used in the recompuation and a default_range used when
    manipulating.
    It should also define a number of computed quantites (as Value) which can
    numpy arrays in the absence of hysteresis or tuple of such arrays. They
    should be tagged with a name, a dim specifying the last dimensions of the
    arrays, and optionally a symbol (short name version) and a map (tuple of
    names identifying the array last dimensions).

    """
    # =========================================================================
    # Physical parameters
    # =========================================================================

    #: When checked all the computed values are assumed to be hysteretic and
    #: should then be stored as pairs of increasing decreasing value.
    hyste = Bool(False).tag(pref=True)

    # =========================================================================
    # Workflow control
    # =========================================================================

    #: List of all used varyings. The order determine the shape of the matrixes
    varyings = List()

    #: Signal notifying that a recomputation occured, and specifying at which
    #: level.
    recomputed = Signal()

    def recompute(self, stage, size):
        """ Recompute some physical quantities.

        This method will be called each time the user ask for it of modify
        a parameter. Once the computation is over and all the computed
        quantities have been updated the recomputed signal should be raised as
        self.recomputed(stage, size).

        Parameters
        ----------
        stage : str
            Stage of the variable which changed and led to the recompuation
            being triggered it should be used to limitate the number of
            recomputation being performed.

        size : bool
            Whether or not the size of the computed quantity is assumed to have
            changed by the user. This should be double checked during
            recomputation and updated accordingly before emmitting the
            recomputed signal.

        """
        raise NotImplementedError()
