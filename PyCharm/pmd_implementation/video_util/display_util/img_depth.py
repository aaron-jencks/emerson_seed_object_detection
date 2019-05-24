from data_structures.lists import LinkedList
# Required even though it's never used, it registers the '3d' perspective for plt.axes
from mpl_toolkits.mplot3d import Axes3D
import pyximport; pyximport.install()
import matplotlib.widgets as widg
from matplotlib.path import Path as MPth
import matplotlib.pyplot as plt
import numpy as np
from array import array

import video_util.display_util.cy_scatter as ct

from PyQt5 import QtGui
import pyqtgraph as pg


processor = None


def create_qt_window():
    app = QtGui.QGuiApplication([])

    w = QtGui.QWidget()

    roi_btn = QtGui.QPushButton('roi')
    exit_btn = QtGui.QPushButton('exit')

    image = pg.PlotWidget()
    pointcloud = pg.PlotWidget()

    layout = QtGui.QGridLayout()
    w.setLayout(layout)

    layout.addWidget(roi_btn, 2, 2)
    layout.addWidget(exit_btn, 2, 2)

    layout.addWidget(image, 1, 0)
    layout.addWidget(pointcloud, 1, 2)

    w.show()

    app.exec_()

    return image, pointcloud, roi_btn, exit_btn


def generate_side_by_side(fig_size: iter = None) -> tuple:
    """Creates a plt.figure with two subplots, one for displaying grayscale images,
    and a 3d plot for displaying the pointcloud.

    fig_size: [optional] represents the size of the figure window desired. Default is 10\" by 5\".

    Returns: returns a tuple containing the figure, image axes, and pointcloud axes."""

    if fig_size is None:
        fig_size = [10, 5]

    fig = plt.figure(figsize=fig_size)

    img = fig.add_subplot(121)

    dpc = fig.add_subplot(122, projection='3d')

    return fig, img, dpc


def display_grayscale(ax, frame, cmap: str = 'gray', init: bool = False):
    """Displays the given image onto the axes using the pcolormesh with the given colormap.

    ax: The plt.axes to draw on.

    frame: The 2D array to display

    cmap: [optional] A string describing the type of colormap to use for the image, default is 'gray'."""

    if init:
        ax = ax.imshow(frame, cmap=cmap)
    else:
        ax.set_data(frame)
    # ax.invert_yaxis()

    return ax


def draw_3d_scatter(ax, depths, validator=lambda r, c: True, h: int = -1, w: int = -1,
                    interpolation: int = 10, init: bool = False):
    """Creates 3 arrays of points the correspond to valid depth points on the image,
    then plots them onto the given axis.

    ax: The plt.axes to draw on.

    depths: The depth frame to use for the z axis.

    validator: [optional] Lambda expression used to determine if a point should be included in the cloud or not,
        default is 'lambda r, c: True' (all points are plotted)

    h: [optional] height of the region to draw for, default is the entire image
    w: [optional] width of the region to draw for, default is the entire image

    interpolation: [optional] The number of pixels to skip between points, default is 10"""

    x, y, z = ct.scatter_data(depths.astype(float), validator, h, w, interpolation)

    # Plots the points
    if init:
        ax, = pg.plot(x, y, z)  # , c=z, cmap='plasma', vmin=0, vmax=max(z))
    else:
        ax.xdata = x
        ax.ydata = y
        ax.zdata = z

    return ax


def scale_display(ax: plt.axes, x_dims: iter = None, y_dims: iter = None, z_dims: iter = None):
    """Scales the given axes to fit the given dimensions, if a given dimension is not provided,
    then the axis is not scaled.

    x_dims: [optional] x-axis limits to use in the form of [xmin, xmax], default is None
    y_dims: [optional] y-axis limits to use in the form of [ymin, ymax], default is None
    z_dims: [optional] z-axis limits to use in the form of [zmin, zmax], default is None"""

    if x_dims is not None:
        ax.set_xlim(x_dims)

    if y_dims is not None:
        ax.set_ylim(y_dims)

    if z_dims is not None:
        ax.set_zlim(z_dims)


def create_generic_button(start_left: float, start_top: float, text: str, callback) -> widg.Button:
    """Creates a generic matplotlib Button using a width of 0.1 and height of 0.075.

    start_left: where on the figure you want to start the button at.
    start_top: where on the figure you want to start the button at.

    text: The text to display on the button.

    callback: a method with one argument that is executed when the button is clicked."""

    but_ax = plt.axes(arg=[start_left, start_top, 0.1, 0.075])
    button = widg.Button(but_ax, text)
    button.on_clicked(callback)

    return button
