# -*- coding: utf-8 -*-
"""
"""
from atom.api import (Typed, Str, Enum, Value, Float)
from chaco.api\
    import (ColorBar, LinearMapper, HPlotContainer,
            GridDataSource, ImagePlot, CMapImagePlot, ContourPolyPlot)

from chaco.tools.api\
    import PanTool

from chaco.default_colormaps import color_map_name_dict, Greys

from numpy import cosh, exp, linspace, meshgrid, tanh

from ..base_plot import BasePlot
from ..data_infos import AbstractInfo
from .chaco_renderer import ChacoPlot2D


class Plot2D(BasePlot):
    """
    """
    #: Colorbar of the plot (ideally this should be abstracted away)
    colorbar = Typed(ColorBar)

    #: Container for Chaco components
    container = Typed(HPlotContainer)

    #: Infos object used to retrieve the data.
    c_info = Typed(AbstractInfo)

    #: Bounds of the plot.
    x_min = Float()
    x_max = Float(1.0)
    y_min = Float()
    y_max = Float(1.0)

    #: Axis labels.
    x_axis = Str()
    y_axis = Str()
    c_axis = Str()

    #: Known colormaps from which the user can choose.
    colormap = Enum(*sorted(color_map_name_dict.keys())).tag(pref=True)

    #: Currently selected colormap.
    _cmap = Value(Greys)

    def __init__(self, **kwargs):

        super(Plot2D, self).__init__(**kwargs)

        self.renderer = ChacoPlot2D(self.data)
        self.renderer.padding = (80, 50, 10, 40)

        # Dummy plot so that the color bar can be correctly initialized
        xs = linspace(-2, 2, 600)
        ys = linspace(-1.2, 1.2, 300)
        x, y = meshgrid(xs, ys)
        z = tanh(x*y/6)*cosh(exp(-y**2)*x/3)
        z = x*y
        self.data.set_data('c', z)
        self.renderer.img_plot(('c'), name='c',
                               colormap=self._cmap,
                               xbounds=(self.x_min, self.x_max),
                               ybounds=(self.y_min, self.y_max))

        # Create the colorbar, the appropriate range and colormap are handled
        # at the plot creation
        mapper = LinearMapper(range=self.renderer.color_mapper.range)
        self.colorbar = ColorBar(index_mapper=mapper,
                                 color_mapper=self.renderer.color_mapper,
                                 plot=self.renderer,
                                 orientation='v',
                                 resizable='v',
                                 width=20,
                                 padding=10)

        self.colorbar.padding_top = self.renderer.padding_top
        self.colorbar.padding_bottom = self.renderer.padding_bottom

        self.container = HPlotContainer(self.renderer,
                                        self.colorbar,
                                        use_backbuffer=True,
                                        bgcolor="lightgray")

        # Add pan and zoom tools to the colorbar
        self.colorbar.tools.append(PanTool(self.colorbar,
                                           constrain_direction="y",
                                           constrain=True)
                                   )

        self.colormap = 'Blues'

    # For the time being stage is unused (will try to refine stuff if it is
    # needed)
    def update_data(self, stage):
        """
        """
        exp = self.experiment
        if self.c_info:
            data = self.c_info.gather_data(exp)
            self.data.set_data('c', data)

    def update_plots_index(self):
        if 'c' in self.data.list_data():
            array = self.data.get_data('c')
            xs = linspace(self.x_min, self.x_max, array.shape[1] + 1)
            ys = linspace(self.y_min, self.y_max, array.shape[0] + 1)
            self.renderer.range2d.remove(self.renderer.index)
            self.renderer.index = GridDataSource(xs, ys,
                                                 sort_order=('ascending',
                                                             'ascending'))
            self.renderer.range2d.add(self.renderer.index)
            for plots in self.renderer.plots.itervalues():
                for plot in plots:
                    plot.index = GridDataSource(xs, ys,
                                                sort_order=('ascending',
                                                            'ascending'))

    def _post_setattr_x_axis(self, old, new):
        self.renderer.x_axis.title = new
        self.container.request_redraw()

    def _post_setattr_y_axis(self, old, new):
        self.renderer.y_axis.title = new
        self.container.request_redraw()

    def _post_setattr_c_axis(self, old, new):
        self.colorbar._axis.title = new
        self.container.request_redraw()

    def _post_setattr_colormap(self, old, new):
        self._cmap = color_map_name_dict[new]
        for plots in self.renderer.plots.itervalues():
            for plot in plots:
                if isinstance(plot, ImagePlot) or\
                        isinstance(plot, CMapImagePlot) or\
                        isinstance(plot, ContourPolyPlot):
                    value_range = plot.color_mapper.range
                    plot.color_mapper = self._cmap(value_range)
                    self.renderer.color_mapper = self._cmap(value_range)

        self.container.request_redraw()

    def _post_setattr_x_min(self, old, new):
        """
        """
        self.update_plots_index()

    def _post_setattr_x_max(self, old, new):
        """
        """
        self.update_plots_index()

    def _post_setattr_y_min(self, old, new):
        """
        """
        self.update_plots_index()

    def _post_setattr_y_max(self, old, new):
        """
        """
        self.update_plots_index()
