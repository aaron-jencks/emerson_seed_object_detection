from mvc_implementation.data_structures.state_machine import SocketedStateMachine, JMsg
from mvc_implementation.display_util.display_util import *

import pyximport; pyximport.install()
import mvc_implementation.data_util.cy_scatter as ct

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
        self.set_widget(widg)

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
    
    slider_scale = 1000
    slider_max = 1
    slider_min = 0
    depth_slider_scale = 100
    depth_scale_max = 4
    
    tx = pyqtSignal([JMsg])
    
    def __init__(self, app: QApplication):
        super().__init__(app)

        self.roi = None
        
        self.states['reset_status'] = self.reset_status
        self.states['update_slider_value'] = self.update_slider_val
        self.states['update_slider_range'] = self.update_slider_range
        self.states['update_slider_callback_valueChanged'] = self.update_slider_callback_valueChanged
        self.states['update_slider_callback_sliderReleased'] = self.update_slider_callback_sliderReleased
        self.states['update_widget_alignment'] = self.update_widget_alignment
        self.states['update_label_text'] = self.update_label_text
        self.states['point_cloud_iniitalize'] = self.dmp_init
        self.states['image_initialize'] = self.img_init
        self.states['roi'] = self.insert_roi
        self.states['process_roi'] = self.process_roi
        self.states['display_image'] = self.display_img
        self.states['display_cloud'] = self.display_cloud

        self.append_states([

            # region Sets up the roi and exit buttons

            ('create_button', get_text_widg_dict('roi', 'roi_btn', 0, 1, col_span=3,
                                                 tip='Create a new <b>ROI</b> (region of interest)' +
                                                     ' or edit the current one.')),
            #
            # ('create_button',
            #                            get_text_widg_dict('Exit', 'exit_btn', 2, 1, 'Exit the program')))
            # self.widgets['exit_btn'].clicked.connect(self.stop)

            # endregion

            # region Sets up the colormap sliders

            ('create_label', get_text_widg_dict('Max', 'cmap_max_lbl', 4, 1)),
            ('create_slider', get_slider_widg_dict(Qt.Vertical, 'cmap_max', 5, 1,
                                                   tip='Adjusts the upper saturation limit of the colormap')),
            ('create_label', get_text_widg_dict('3.0 m', 'cmap_max_lbl_val', 6, 1)),

            ('create_label', get_text_widg_dict('Mid', 'cmap_mid_lbl', 4, 2)),
            ('create_slider', get_slider_widg_dict(Qt.Vertical, 'cmap_mid', 5, 2,
                                                   tip='Adjusts the mid-point of the colormap')),
            ('create_label', get_text_widg_dict('1.5 m', 'cmap_mid_lbl_val', 6, 2)),

            ('create_label', get_text_widg_dict('Min', 'cmap_min_lbl', 4, 3)),
            ('create_slider', get_slider_widg_dict(Qt.Vertical, 'cmap_min', 5, 3,
                                                   tip='Adjusts the lower saturation limit of the colormap')),
            ('create_label', get_text_widg_dict('0.0 m', 'cmap_min_lbl_val', 6, 3)),

            ('create_label', get_text_widg_dict('Depth Scale: {} x'.format(self.depth_scale_max >> 1),
                                                'dmp_scale_lbl', 7, 0)),

            ('create_slider', get_slider_widg_dict(Qt.Horizontal, 'dmp_scale', 6, 0)),

            ('create_label', get_text_widg_dict('Max', 'cmap_max_lbl', 4, 1)),
            ('create_slider', get_slider_widg_dict(Qt.Vertical, 'cmap_max', 5, 1,
                                                   tip='Adjusts the upper saturation limit of the colormap')),
            ('create_label', get_text_widg_dict('3.0 m', 'cmap_max_lbl_val', 6, 1)),

            ('create_label', get_text_widg_dict('Mid', 'cmap_mid_lbl', 4, 2)),
            ('create_slider', get_slider_widg_dict(Qt.Vertical, 'cmap_mid', 5, 2,
                                                   tip='Adjusts the mid-point of the colormap')),
            ('create_label', get_text_widg_dict('1.5 m', 'cmap_mid_lbl_val', 6, 2)),

            ('create_label', get_text_widg_dict('Min', 'cmap_min_lbl', 4, 3)),
            ('create_slider', get_slider_widg_dict(Qt.Vertical, 'cmap_min', 5, 3,
                                                   tip='Adjusts the lower saturation limit of the colormap')),
            ('create_label', get_text_widg_dict('0.0 m', 'cmap_min_lbl_val', 6, 3)),

            ('create_label', get_text_widg_dict('Depth Scale: {} x'.format(self.depth_scale_max >> 1),
                                                'dmp_scale_lbl', 7, 0)),
            ('create_slider', get_slider_widg_dict(Qt.Horizontal, 'dmp_scale', 6, 0)),

            # endregion

            # region Sets up the depth data labels

            ('create_label', get_text_widg_dict('Average depth: 0.0 m', 'dmp_avg_lbl', 1, 1, 1, 3)),
            ('create_label', get_text_widg_dict('Minimum depth: 0.0 m', 'dmp_min_lbl', 2, 1, 1, 3)),
            ('create_label', get_text_widg_dict('Maximum depth: 0.0 m', 'dmp_max_lbl', 3, 1, 1, 3)),

            # endregion

            # region Sets up the plots

            ('create_label', get_text_widg_dict('Grayscale', 'img_lbl', 0, 0)),
            ('create_widget', get_custom_widg_dict(pg.ImageView, 'img', 1, 0, 3, 1)),

            # ('create_label',
            #                                 get_text_widg_dict('Depth Image', 'dimg_lbl', 0, 1)))
            # args = get_custom_widg_dict(pg.ImageView, 'dimg', 1, 1, 1, 3)
            # ('create_widget',
            #                                 args))

            ('create_label', get_text_widg_dict('Point Cloud', 'dmp_lbl', 4, 0)),
            ('create_widget', get_custom_widg_dict(pgl.GLViewWidget, 'dmp', 5, 0)),

            # endregion

            ('update_widget_alignment',
             {
                 'name': 'dmp_scale_lbl',
                 'alignment': Qt.AlignLeft
             }),

        ])

        self.scatter = pgl.GLScatterPlotItem(pos=np.zeros(shape=(307200, 3), dtype=float), size=3)
        self.img_item = pg.ImageItem()

        self.append_states(['point_cloud_initialize', 'image_initialize'])

        # region Hooks up the slider bars

        # Max bar
        self.append_states([
            
            # region Sets up the callback functions for the sliders
            
            ('update_slider_callback_valueChanged', 
             {
                 'name': 'cmap_max', 
                 'method': lambda v: 
                 self.append_states([('update_label_text', {'name': 'cmap_max_lbl_val',
                                                            'value': '{} m'.format(round(v / self.slider_scale, 3))})])
             }),
            ('update_slider_callback_sliderReleased',
             {
                 'name': 'cmap_max',
                 'method': lambda: self.tx.emit('slider cmap_max value', self.widgets['cmap_max'].value())
             }),
            
            ('update_slider_callback_valueChanged',
             {
                 'name': 'cmap_mid',
                 'method': lambda v:
                 self.append_states([('update_label_text', {'name': 'cmap_mid_lbl_val',
                                                            'value': '{} m'.format(round(v / self.slider_scale, 3))})])
             }),
            ('update_slider_callback_sliderReleased',
             {
                 'name': 'cmap_mid',
                 'method': lambda: self.tx.emit('slider cmap_mid value', self.widgets['cmap_mid'].value())
             }),
            
            ('update_slider_callback_valueChanged',
             {
                 'name': 'cmap_min',
                 'method': lambda v:
                 self.append_states([('update_label_text', {'name': 'cmap_min_lbl_val',
                                                            'value': '{} m'.format(round(v / self.slider_scale, 3))})])
             }),
            ('update_slider_callback_sliderReleased',
             {
                 'name': 'cmap_min',
                 'method': lambda: self.tx.emit('slider cmap_min value', self.widgets['cmap_min'].value())
             }),

            ('update_slider_callback_valueChanged',
             {
                 'name': 'dmp_scale',
                 'method': lambda v:
                 self.widgets['dmp_scale_lbl'].setText('Depths Scale: {} x'.format(round(v / self.depth_slider_scale, 
                                                                                         3)))
             }),
            ('update_slider_callback_sliderReleased',
             {
                 'name': 'dmp_scale',
                 'method': lambda: self.tx.emit('slider dmp_scale value', self.widgets['dmp_scale'].value())
             }),
            
            # endregion
            
            # region Sets the depth scale slider range and value
            
            ('update_slider_range',
             {
                 'name': 'dmp_scale',
                 'value': (1 * self.depth_slider_scale, self.depth_slider_scale_max * self.depth_slider_scale)
             }),
            
            ('update_slider_value',
             {
                 'name': 'dmp_scale',
                 'value': self.depth_scale_max >> 1
             })
            
            # endregion
        ])

        # endregion

    def reset_status(self):
        self.window.statusBar().showMessage('Ready')

    def display_img(self, img):
        self.widgets['img'].setImage(img)

    def display_cloud(self, data: dict):
        self.scatter.setData(pos=data['vectors'], color=data['colors'])

    def insert_roi(self, points: list):
        self.roi = pg.PolyLineROI(points, closed=True, movable=True, removable=False)
        self.widgets['img'].getView().addItem(self.roi)

    def process_roi(self, img):
        if self.roi is not None:
            roi_coords = self.roi.getArrayRegion(ct.get_roi_coords_matrix(img.shape[0], img.shape[1]),
                                                 self.img_item)
            self.tx.emit(JMsg('enable_roi', roi_coords))
        else:
            self.tx.emit(JMsg('disable_roi'))

    def img_init(self):
        self.widgets['img'].addItem(self.img_item)

    def dmp_init(self):
        widg = self.widgets['dmp']
        widg.addItem(self.scatter)
        self.scatter.rotate(180, 0, 0, 0)
        self.scatter.setGLOptions('opaque')
        widg.pan(-320, -240, 0)
        widg.setCameraPosition(distance=1746, elevation=43, azimuth=-479)

    def update_label_text(self, data: dict):
        name = data['name']
        value = data['value']
        self.widgets[name].setText(value)

    def update_widget_alignment(self, data):
        name = data['name']
        alignment = data['alignment']
        self.widgets[name].setAlignment(alignment)
        
    def update_slider_callback_sliderReleased(self, data: dict):
        name = data['name']
        cb = data['method']
        self.widgets[name].sliderReleased.connect(cb)
        self.tx.emit(JMsg('slider ' + name + ' sliderReleased', cb))
        
    def update_slider_callback_valueChanged(self, data: dict):
        name = data['name']
        cb = data['method']
        self.widgets[name].valueChanged.connect(cb)
        self.tx.emit(JMsg('slider ' + name + ' valueChanged', cb))
        
    def update_slider_range(self, data: dict):
        name = data['name']
        mn = data['min']
        mx = data['max']
        self.widgets[name].setRange(mn, mx)
        self.tx.emit(JMsg('slider ' + name + ' range', (mn, mx)))

    def update_slider_val(self, data: dict):
        name = data['name']
        value = data['value']
        self.widgets[name].setValue(value)
        self.tx.emit(JMsg('slider ' + name + ' value', value))

