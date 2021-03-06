# -*- coding: utf-8 -*-
"""
"""
import enaml
from atom.api import (Typed, Str, Enum, Value, Float)
from chaco.api\
    import (ColorBar, LinearMapper, HPlotContainer,
            GridDataSource, ImagePlot, CMapImagePlot, ContourPolyPlot)

from chaco.tools.api\
    import PanTool, BetterSelectingZoom

from chaco.default_colormaps import color_map_name_dict, Greys

from numpy import cosh, exp, linspace, meshgrid, tanh, savetxt

from ..base_plot import BasePlot
from ..data_infos import AbstractInfo, DATA_INFOS
from .chaco_renderer import ChacoPlot2D
from .zoom_bar import zoom_bar, ZoomBar
with enaml.imports():
    from .plot2d_views import Plot2DItem


class Plot2D(BasePlot):
    """
    """
    #: Colorbar of the plot (ideally this should be abstracted away)
    colorbar = Typed(ColorBar)

    zoom_colorbar = Typed(ZoomBar)

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

        # Add basic tools and ways to activate them in public API
        zoom = BetterSelectingZoom(self.renderer, tool_mode="box",
                                   always_on=False)
        self.renderer.overlays.append(zoom)
        self.renderer.tools.append(PanTool(self.renderer,
                                           restrict_to_data=True))

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
        self.zoom_colorbar = zoom_bar(self.colorbar,
                                      box=False,
                                      reset=True,
                                      orientation='vertical'
                                      )
        self.colormap = 'Blues'

    def export_data(self, path):
        """
        """
        if not path.endswith('.dat'):
            path += '.dat'
        header = self.experiment.make_header()
        header += '\n' + self.c_info.make_header(self.experiment)
        arr = self.data.get_data('c')

        with open(path, 'wb') as f:
            header = ['#' + l for l in header.split('\n') if l]
            f.write('\n'.join(header) + '\n')
            savetxt(f, arr, fmt='%.6e', delimiter='\t')

    def auto_scale(self):
        """
        """
        self.renderer.range2d.set_bounds(('auto', 'auto'), ('auto', 'auto'))
        self.renderer.color_mapper.range.set_bounds('auto', 'auto')

    # For the time being stage is unused (will try to refine stuff if it is
    # needed)
    def update_data(self, stage):
        """
        """
        exp = self.experiment
        if self.c_info:
            data = self.c_info.gather_data(exp)
            if len(data.shape) == 2:
                self.data.set_data('c', data.T)
                self.update_plots_index()

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

    @classmethod
    def build_view(cls, plot):
        """
        """
        return Plot2DItem(plot=plot)

    def preferences_from_members(self):
        """
        """
        d = super(Plot2D, self).preferences_from_members()
        d['c_info'] = self.c_info.preferences_from_members()

        return d

    def update_members_from_preferences(self, config):
        """
        """
        super(Plot2D, self).update_members_from_preferences(config)
        c_config = config['c_info']
        info = [c for c in DATA_INFOS
                if c.__name__ == c_config['info_class']][0]()
        info.update_members_from_preferences(c_config)

        self.c_info = info
        self.update_data(None)

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
