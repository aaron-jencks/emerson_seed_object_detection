from pmd_implementation.data_structures.state_machine import StateMachine, JMsg
from pmd_implementation.data_structures.Q import DequeManager
from pmd_implementation.display_util.daemons import DisplayMachine
from pmd_implementation.display_util.display_util import *
from pmd_implementation.cam_util.daemons import CamCtrl
from pmd_implementation.data_util.daemons import DataDaemon
from pmd_implementation.dependencies.display_util.string_display_util import print_notification

from PyQt5.QtCore import Qt, QThread
from PyQt5.QtWidgets import QApplication, QSlider
import pyqtgraph as pg
import pyqtgraph.opengl as pgl

import numpy as np

import pyximport; pyximport.install()


class DepthAverager(QThread, StateMachine):
    """Manages the depth averaging for this application"""

    slider_max = 300
    slider_min = 0

    def __init__(self, disp_daemon: DisplayMachine):
        super().__init__()

        if self.slider_max - self.slider_min < 3:
            raise AssertionError('Slider extremes must be at least 3 apart.')

        # region Display Daemon

        self.disp_ctrl_update = disp_daemon.update
        self.disp_ctrl = disp_daemon
        self.scatter = None
        self.set_status('Loading...')
        self.init_widget()

        # endregion

        # region Camera Daemon

        self.cam_ctrl = CamCtrl()
        self.cam_ctrl_tx = self.cam_ctrl.rx
        self.cam_ctrl.tx.connect(self.plot_data)
        self.init_camera()
        self.cam_ctrl.start()

        # endregion

        # region Processor

        self.data_proc = DataDaemon()
        self.data_proc.start()
        self.data_proc.tx.connect(self.plot_cloud)

        # region Hooks up the slider bars

        # Max bar
        self.disp_ctrl.widgets['cmap_max'].setValue(self.data_proc.cmap_up)
        self.disp_ctrl.widgets['cmap_max'].valueChanged.connect(lambda v: self.update_slider(v, 'up'))

        # Mid bar
        self.disp_ctrl.widgets['cmap_mid'].setValue(self.data_proc.cmap_mid)
        self.disp_ctrl.widgets['cmap_mid'].valueChanged.connect(lambda v: self.update_slider(v, 'mid'))

        # Min bar
        self.disp_ctrl.widgets['cmap_min'].setValue(self.data_proc.cmap_low)
        self.disp_ctrl.widgets['cmap_min'].valueChanged.connect(lambda v: self.update_slider(v, 'low'))

        # Sets the limits of the bar
        self.disp_ctrl.widgets['cmap_max'].setRange(self.slider_min, self.slider_max)
        self.disp_ctrl.widgets['cmap_mid'].setRange(self.slider_min, self.slider_max)
        self.disp_ctrl.widgets['cmap_min'].setRange(self.slider_min, self.slider_max)

        # Initializes the sliders to the values of the data processor
        self.init_slider()

        # endregion

        # endregion

        self.prev_skipped = False
        self.frame_count = 1

    def stop(self):
        self.cam_ctrl.stop_capture()
        self.cam_ctrl.stop()
        super().stop()

    def plot_data(self, msg: JMsg):
        """Plots the frame data onto the window."""

        img = msg.data[0]
        depth = msg.data[1]

        if len(self.data_proc.state_queue) < self.data_proc.buffer_limit:
            self.data_proc.rx.emit(JMsg('frame', depth))
            if self.prev_skipped:
                print()
                self.prev_skipped = False
                self.frame_count = 1
                self.set_status('Ready')
        else:
            not_string = "Data processor buffer full, skipping {} cloud frames!".format(self.frame_count)

            print_notification(not_string, begin='\r' if self.prev_skipped else '', end='')
            self.prev_skipped = True
            self.frame_count += 1

            self.set_status(not_string)

        img_disp = self.disp_ctrl.widgets['img']

        img_disp.setImage(img)

    def plot_cloud(self, data, colors):
        """Plots the pointcloud onto the window."""

        # data = np.array([(a, b, c) for a, b, c in zip(x, y, z)])
        # print(data.size)
        self.scatter.setData(pos=data, color=colors)

        # Sets the center of the camera to the center of the cloud
        # self.disp_ctrl.widgets['dmp'].pan(self.data_proc.center_x,
        #                                   self.data_proc.center_y,
        #                                   self.data_proc.center_z)

    def init_camera(self):
        """Initializes the camera connecting to one if possible,
        this is where adjustments need to be made if you want to change the settings."""

        if not self.cam_ctrl.pmd:
            self.cam_ctrl_tx.emit(JMsg('configure_cam', {'ir_stream': {}, 'depth_stream': {}}))
            # self.cam_ctrl_tx.emit(JMsg('depth_stream'))

        self.cam_ctrl_tx.emit(JMsg('start_cam'))

    def init_widget(self):
        """Creates the window layout for the main display"""

        # region Sets up the roi and exit buttons

        # self.disp_ctrl_update.emit(JMsg('create_button',
        #                            get_text_widg_dict('roi', 'roi_btn', 2, 0,
        #                                               'Create a new <b>ROI</b> (region of interest)' +
        #                                               ' or edit the current one.')))
        #
        # self.disp_ctrl_update.emit(JMsg('create_button',
        #                            get_text_widg_dict('Exit', 'exit_btn', 2, 1, 'Exit the program')))
        # self.disp_ctrl.widgets['exit_btn'].clicked.connect(self.stop)

        # endregion

        # region Sets up the colormap sliders

        self.disp_ctrl_update.emit(JMsg('create_label',
                                   get_text_widg_dict('Max', 'cmap_max_lbl', 0, 2)))
        self.disp_ctrl_update.emit(JMsg('create_slider',
                                   get_slider_widg_dict(Qt.Vertical, 'cmap_max', 1, 2,
                                                        'Adjusts the upper saturation limit of the colormap')))

        self.disp_ctrl_update.emit(JMsg('create_label',
                                   get_text_widg_dict('Mid', 'cmap_mid_lbl', 0, 3)))
        self.disp_ctrl_update.emit(JMsg('create_slider',
                                   get_slider_widg_dict(Qt.Vertical, 'cmap_mid', 1, 3,
                                                        'Adjusts the mid-point of the colormap')))

        self.disp_ctrl_update.emit(JMsg('create_label',
                                   get_text_widg_dict('Min', 'cmap_min_lbl', 0, 4)))
        self.disp_ctrl_update.emit(JMsg('create_slider',
                                   get_slider_widg_dict(Qt.Vertical, 'cmap_min', 1, 4,
                                                        'Adjusts the lower saturation limit of the colormap')))

        # endregion

        # region Sets up the plots

        self.disp_ctrl_update.emit(JMsg('create_label',
                                   get_text_widg_dict('Grayscale', 'img_lbl', 0, 0)))
        self.disp_ctrl_update.emit(JMsg('create_widget',
                                   get_custom_widg_dict(pg.ImageView, 'img', 1, 0)))

        self.disp_ctrl_update.emit(JMsg('create_label',
                                   get_text_widg_dict('Point Cloud', 'dmp_lbl', 0, 1)))
        self.disp_ctrl_update.emit(JMsg('create_widget',
                                   get_custom_widg_dict(pgl.GLViewWidget, 'dmp', 1, 1)))

        self.scatter = pgl.GLScatterPlotItem(pos=np.zeros(shape=(307200, 3), dtype=float))
        self.disp_ctrl.widgets['dmp'].addItem(self.scatter)
        widg = self.disp_ctrl.widgets['dmp']
        widg.pan(240, 320, 40)
        # TODO Pan camera here to center of image location

        # endregion

    def init_slider(self):
        self.disp_ctrl.widgets['cmap_max'].setValue(self.data_proc.cmap_up)
        self.disp_ctrl.widgets['cmap_mid'].setValue(self.data_proc.cmap_mid)
        self.disp_ctrl.widgets['cmap_min'].setValue(self.data_proc.cmap_low)

    def update_slider(self, value: int, slider: str):
        """Updates the value of the adjusted slider"""
        self.data_proc.rx.emit(JMsg(slider, value / 100))

        # Waits for the cmap value to be updated
        while True:
            if slider == 'up':
                cm = self.data_proc.cmap_up
            elif slider == 'mid':
                cm = self.data_proc.cmap_mid
            else:
                cm = self.data_proc.cmap_low

            if cm == value:
                break

        self.set_slider_limits()

    def set_slider_limits(self):
        """Updates the limits of the slider values so that they don't exceed each other."""
        mx = self.disp_ctrl.widgets['cmap_max'].value()
        md = self.disp_ctrl.widgets['cmap_mid'].value()
        mn = self.disp_ctrl.widgets['cmap_min'].value()

        if mx - mn < 3:
            diff = 3 - (mx - mn)
            if mx < self.slider_max:
                self.disp_ctrl.widgets['cmap_max'].setValue(mx + diff)
            elif mn > self.slider_min:
                self.disp_ctrl.widgets['cmap_min'].setValue(mn - diff)

        if md >= mx:
            self.disp_ctrl.widgets['cmap_mid'].setValue(mx - 1)

        if md <= mn:
            self.disp_ctrl.widgets['cmap_mid'].setValue(mn + 1)

    def set_status(self, message: str):
        """Sets the status bar of the main display"""
        self.disp_ctrl_update.emit(JMsg('status', message))


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)

    mgr = DequeManager()
    mgr.start()

    dsp = DisplayMachine(app)

    avg = DepthAverager(dsp)

    try:
        avg.start()

        dsp.run()

        app.exec_()
    except Exception as e:
        print(e)
    finally:
        avg.stop()
