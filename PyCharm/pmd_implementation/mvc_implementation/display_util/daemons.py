from mvc_implementation.data_structures.state_machine import SocketedStateMachine, JMsg
from mvc_implementation.display_util.display_util import *

import pyqtgraph as pg
import pyqtgraph.opengl as pgl

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import *

import numpy as np

import sys


class DisplayWindow(QMainWindow):

    def __init__(self):
        super().__init__()

class BetterDisplayMachine(SocketedStateMachine):

    def __init__(self, app: QApplication):
        super().__init__()
        self.app = app
        self.window = QMainWindow()
        self.grid = QGridLayout()
        self.widgets = {}

        # Sets up the grid layout
        # self.grid = QGridLayout()
        self.grid.setSpacing(10)

        # Creates basic layout widget
        widg = QWidget()
        widg.setLayout(self.grid)
        self.set_widget(JMsg("", widg))

        self.window.setGeometry(300, 300, 500, 400)
        self.window.setWindowTitle('Depth Averaging Utility')
        self.window.statusBar().showMessage('Ready')
        self.window.show()

        # region Sets up the states dict

        self.states['set_widget'] = self.set_widget
        self.states['status'] = self.set_status
        self.states['title'] = self.set_title
        self.states['show'] = self.window.show
        self.states['hide'] = self.window.hide
        self.states['create_button'] = self.create_button
        self.states['create_label'] = self.create_label
        self.states['create_text_entry'] = self.create_line_edit
        self.states['create_slider'] = self.create_slider
        self.states['create_widget'] = self.create_widget

        # endregion

    def set_widget(self, data: QWidget):
        """Changes the central widget of the display contained in this window"""
        self.window.setCentralWidget(data)
        self.window.show()

    def set_status(self, data: str):
        """Changes the status bar message of this display's window"""
        self.window.statusBar().showMessage(data)

    def set_title(self, data: str):
        """Changes the window title"""
        self.window.setWindowTitle(data)

    def __create_widget(self, widg: QWidget, data: dict):
        """Creates a new widget object"""

        if 'tip' in data:
            widg.setToolTip(data['tip'])

        widg.resize(widg.sizeHint())

        self.widgets[data['id']] = widg
        self.grid.addWidget(widg, data['row'], data['col'], data['rowSpan'], data['columnSpan'])

        return widg

    def create_widget(self, data: dict):
        """Creates a custom widget based on the arguments and type given"""
        if 'kwargs' in data:
            temp = data['type'](**data['kwargs'], parent=self.window)
        else:
            temp = data['type'](parent=self.window)

        self.__create_widget(temp, data)

    def create_button(self, data: dict):
        """Creates a new button with the given arguments"""
        data['type'] = QPushButton
        data['kwargs'] = {'text': data['text']}
        self.create_widget(data)

    def create_label(self, data: dict):
        """Creates a new label with the given arguments"""
        data['type'] = QLabel
        data['kwargs'] = {'text': data['text']}
        self.create_widget(data)

    def create_line_edit(self, data: dict):
        """Creates a new lineEdit (text entry) box with the given arguments"""
        data['type'] = QLineEdit
        self.create_widget(data)

    def create_slider(self, data: dict):
        """Creates a new slider with the given arguments"""
        data['type'] = QSlider
        data['kwargs'] = {'orientation': data['orient']}
        self.create_widget(data)

    # endregion


class PointCloudDisplayMachine(BetterDisplayMachine):
    
    tx = pyqtSignal([JMsg])
    
    def __init__(self, app: QApplication):
        super().__init__(app)
        
        self.states['reset_status'] = self.reset_status
        self.states['update_slider_value'] = self.update_slider_val

        # region Sets up the roi and exit buttons

        self.update.emit(JMsg('create_button',
                              get_text_widg_dict('roi', 'roi_btn', 0, 1, col_span=3,
                                                 tip='Create a new <b>ROI</b> (region of interest)' +
                                                     ' or edit the current one.')))
        #
        # self.update.emit(JMsg('create_button',
        #                            get_text_widg_dict('Exit', 'exit_btn', 2, 1, 'Exit the program')))
        # self.widgets['exit_btn'].clicked.connect(self.stop)

        # endregion

        # region Sets up the colormap sliders

        self.update.emit(JMsg('create_label',
                              get_text_widg_dict('Max', 'cmap_max_lbl', 4, 1)))
        self.update.emit(JMsg('create_slider',
                              get_slider_widg_dict(Qt.Vertical, 'cmap_max', 5, 1,
                                                   tip='Adjusts the upper saturation limit of the colormap')))
        self.update.emit(JMsg('create_label',
                              get_text_widg_dict('3.0 m', 'cmap_max_lbl_val', 6, 1)))

        self.update.emit(JMsg('create_label',
                              get_text_widg_dict('Mid', 'cmap_mid_lbl', 4, 2)))
        self.update.emit(JMsg('create_slider',
                              get_slider_widg_dict(Qt.Vertical, 'cmap_mid', 5, 2,
                                                   tip='Adjusts the mid-point of the colormap')))
        self.update.emit(JMsg('create_label',
                              get_text_widg_dict('1.5 m', 'cmap_mid_lbl_val', 6, 2)))

        self.update.emit(JMsg('create_label',
                              get_text_widg_dict('Min', 'cmap_min_lbl', 4, 3)))
        self.update.emit(JMsg('create_slider',
                              get_slider_widg_dict(Qt.Vertical, 'cmap_min', 5, 3,
                                                   tip='Adjusts the lower saturation limit of the colormap')))
        self.update.emit(JMsg('create_label',
                              get_text_widg_dict('0.0 m', 'cmap_min_lbl_val', 6, 3)))

        self.update.emit(JMsg('create_label',
                              get_text_widg_dict('Depth Scale: {} x'.format(self.depth_scale_max >> 1),
                                                 'dmp_scale_lbl', 7, 0)))
        self.widgets['dmp_scale_lbl'].setAlignment(Qt.AlignLeft)
        self.update.emit(JMsg('create_slider',
                              get_slider_widg_dict(Qt.Horizontal, 'dmp_scale', 6, 0)))

        # endregion

        # region Sets up the depth data labels

        self.update.emit(JMsg('create_label',
                              get_text_widg_dict('Average depth: 0.0 m', 'dmp_avg_lbl', 1, 1, 1, 3)))
        self.update.emit(JMsg('create_label',
                              get_text_widg_dict('Minimum depth: 0.0 m', 'dmp_min_lbl', 2, 1, 1, 3)))
        self.update.emit(JMsg('create_label',
                              get_text_widg_dict('Maximum depth: 0.0 m', 'dmp_max_lbl', 3, 1, 1, 3)))

        # endregion

        # region Sets up the plots

        self.update.emit(JMsg('create_label',
                              get_text_widg_dict('Grayscale', 'img_lbl', 0, 0)))
        self.update.emit(JMsg('create_widget',
                              get_custom_widg_dict(pg.ImageView, 'img', 1, 0, 3, 1)))

        # self.update.emit(JMsg('create_label',
        #                                 get_text_widg_dict('Depth Image', 'dimg_lbl', 0, 1)))
        # args = get_custom_widg_dict(pg.ImageView, 'dimg', 1, 1, 1, 3)
        # self.update.emit(JMsg('create_widget',
        #                                 args))

        self.update.emit(JMsg('create_label',
                              get_text_widg_dict('Point Cloud', 'dmp_lbl', 4, 0)))
        self.update.emit(JMsg('create_widget',
                              get_custom_widg_dict(pgl.GLViewWidget, 'dmp', 5, 0)))

        self.scatter = pgl.GLScatterPlotItem(pos=np.zeros(shape=(307200, 3), dtype=float), size=3)
        self.widgets['dmp'].addItem(self.scatter)

        # region view formatting

        self.scatter.rotate(180, 0, 0, 0)
        self.scatter.setGLOptions('opaque')
        widg = self.widgets['dmp']
        # widg.mouseReleaseEvent = lambda v: self.update_center_display()
        widg.pan(-320, -240, 0)
        widg.setCameraPosition(distance=1746, elevation=43, azimuth=-479)

        # endregion

        # endregion

        # region Hooks up the UI

        # region Hooks up the ImageItem

        self.img_item = pg.ImageItem()
        self.widgets['img'].addItem(self.img_item)

        # endregion

        # region Hooks up the slider bars

        # Max bar
        self.widgets['cmap_max'].setValue(self.data_proc.cmap_up)

        self.widgets['cmap_max'].valueChanged.connect(lambda v:
                                                                self.widgets['cmap_max_lbl_val'].setText(
                                                                    '{} m'.format(round(v / self.slider_scale, 3))))

        self.widgets['cmap_max'].sliderReleased.connect(lambda: self.update_slider(
            self.widgets['cmap_max'].value(), 'up'))

        # Mid bar
        self.widgets['cmap_mid'].setValue(self.data_proc.cmap_mid)

        self.widgets['cmap_mid'].valueChanged.connect(lambda v:
                                                                self.widgets['cmap_mid_lbl_val'].setText(
                                                                    '{} m'.format(round(v / self.slider_scale, 3))))

        self.widgets['cmap_mid'].sliderReleased.connect(lambda: self.update_slider(
            self.widgets['cmap_mid'].value(), 'mid'))

        # Min bar
        self.widgets['cmap_min'].setValue(self.data_proc.cmap_low)

        self.widgets['cmap_min'].valueChanged.connect(lambda v:
                                                                self.widgets['cmap_min_lbl_val'].setText(
                                                                    '{} m'.format(round(v / self.slider_scale, 3))))

        self.widgets['cmap_min'].sliderReleased.connect(lambda: self.update_slider(
            self.widgets['cmap_min'].value(), 'low'))

        # Sets the limits of the bar
        self.widgets['cmap_max'].setRange(self.slider_min * self.slider_scale,
                                                    self.slider_max * self.slider_scale)

        self.widgets['cmap_mid'].setRange(self.slider_min * self.slider_scale,
                                                    self.slider_max * self.slider_scale)

        self.widgets['cmap_min'].setRange(self.slider_min * self.slider_scale,
                                                    self.slider_max * self.slider_scale)

        # region Handles the Depth Scale bar

        self.widgets['dmp_scale'].setRange(1 * self.depth_slider_scale,
                                                     self.depth_scale_max * self.depth_slider_scale)
        self.widgets['dmp_scale'].setValue(self.depth_scale_max >> 1)

        self.widgets['dmp_scale'].valueChanged.connect(lambda v:
                                                                 self.widgets['dmp_scale_lbl'].setText(
                                                                     'Depth Scale: {} x'.format(
                                                                         round(v / self.depth_slider_scale, 1))))

        self.widgets['dmp_scale'].sliderReleased.connect(lambda: self.update_slider(
            10 ** (self.widgets['dmp_scale'].value() / self.depth_slider_scale), 'scale'))

        self.update_slider(self.widgets['dmp_scale'].value(), 'scale')

        # endregion

        # Initializes the sliders to the values of the data processor
        self.init_slider()

        # endregion

    def reset_status(self, msg: JMsg):
        self.window.statusBar().showMessage('Ready')

    def update_slider_val(self, msg: JMsg):

