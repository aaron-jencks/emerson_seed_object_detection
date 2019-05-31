from pmd_implementation.data_structures.state_machine import StateMachine, JMsg
from pmd_implementation.data_structures.Q import DequeManager
from pmd_implementation.display_util.daemons import DisplayMachine
from pmd_implementation.display_util.display_util import *
from pmd_implementation.cam_util.daemons import CamCtrl
from pmd_implementation.data_util.daemons import DataDaemon
from pmd_implementation.dependencies.display_util.string_display_util import print_notification, print_warning

from PyQt5.QtCore import Qt, QThread
from PyQt5.QtWidgets import QApplication
import pyqtgraph as pg
import pyqtgraph.opengl as pgl

import numpy as np

import pyximport
pyximport.install(setup_args={"include_dirs": np.get_include()})
import pmd_implementation.data_util.cy_scatter as ct

import queue


class DepthAverager(QThread, StateMachine):
    """Manages the depth averaging for this application"""

    slider_scale = 1000
    slider_max = 1
    slider_min = 0
    depth_slider_scale = 100
    depth_scale_max = 4
    # filename = "/media/aaron/JET TFER/GPM Seed Placement/May Testing Trip to GPM/5.6.2019 AM/" \
    #            "royale_20190506_111114.rrf"

    def __init__(self, disp_daemon: DisplayMachine):
        super().__init__()

        if self.slider_max * self.slider_scale - self.slider_min * self.slider_scale < 3:
            raise AssertionError('Slider extremes must be at least 3 apart.')

        # region Display Daemon

        self.disp_ctrl_update = disp_daemon.update
        self.disp_ctrl = disp_daemon
        self.scatter = None
        self.gray = None
        self.use_roi = False
        self.roi = None
        self.roi_coords = None
        self.set_status('Loading...')
        self.init_widget()

        # endregion

        # region Camera Daemon

        self.cam_ctrl = CamCtrl(parent=self.disp_ctrl.window)
        self.cam_ctrl_tx = self.cam_ctrl.rx
        self.cam_ctrl.tx.connect(self.plot_data)
        self.cam_ctrl.start()
        # self.cam_ctrl_tx.emit(JMsg('filename', self.filename))
        self.init_camera()

        # endregion

        # region Processor

        self.data_proc = DataDaemon()
        self.data_proc.start()
        self.data_proc.tx.connect(self.plot_cloud)

        # endregion

        # region Hooks up the UI

        # region Hooks up the ImageItem

        self.img_item = pg.ImageItem()
        self.disp_ctrl.widgets['img'].addItem(self.img_item)

        # endregion

        # region Hooks up the slider bars

        # Max bar
        self.disp_ctrl.widgets['cmap_max'].setValue(self.data_proc.cmap_up)

        self.disp_ctrl.widgets['cmap_max'].valueChanged.connect(lambda v:
                                                                self.disp_ctrl.widgets['cmap_max_lbl_val'].setText(
                                                                    '{} m'.format(round(v / self.slider_scale, 3))))

        self.disp_ctrl.widgets['cmap_max'].sliderReleased.connect(lambda: self.update_slider(
            self.disp_ctrl.widgets['cmap_max'].value(), 'up'))

        # Mid bar
        self.disp_ctrl.widgets['cmap_mid'].setValue(self.data_proc.cmap_mid)

        self.disp_ctrl.widgets['cmap_mid'].valueChanged.connect(lambda v:
                                                                self.disp_ctrl.widgets['cmap_mid_lbl_val'].setText(
                                                                    '{} m'.format(round(v / self.slider_scale, 3))))

        self.disp_ctrl.widgets['cmap_mid'].sliderReleased.connect(lambda: self.update_slider(
            self.disp_ctrl.widgets['cmap_mid'].value(), 'mid'))

        # Min bar
        self.disp_ctrl.widgets['cmap_min'].setValue(self.data_proc.cmap_low)

        self.disp_ctrl.widgets['cmap_min'].valueChanged.connect(lambda v:
                                                                self.disp_ctrl.widgets['cmap_min_lbl_val'].setText(
                                                                    '{} m'.format(round(v / self.slider_scale, 3))))

        self.disp_ctrl.widgets['cmap_min'].sliderReleased.connect(lambda: self.update_slider(
            self.disp_ctrl.widgets['cmap_min'].value(), 'low'))

        # Sets the limits of the bar
        self.disp_ctrl.widgets['cmap_max'].setRange(self.slider_min * self.slider_scale,
                                                    self.slider_max * self.slider_scale)

        self.disp_ctrl.widgets['cmap_mid'].setRange(self.slider_min * self.slider_scale,
                                                    self.slider_max * self.slider_scale)

        self.disp_ctrl.widgets['cmap_min'].setRange(self.slider_min * self.slider_scale,
                                                    self.slider_max * self.slider_scale)

        # region Handles the Depth Scale bar

        self.disp_ctrl.widgets['dmp_scale'].setRange(1 * self.depth_slider_scale,
                                                     self.depth_scale_max * self.depth_slider_scale)
        self.disp_ctrl.widgets['dmp_scale'].setValue(self.depth_scale_max >> 1)

        self.disp_ctrl.widgets['dmp_scale'].valueChanged.connect(lambda v:
                                                                 self.disp_ctrl.widgets['dmp_scale_lbl'].setText(
                                                                     'Depth Scale: {} x'.format(
                                                                         round(v / self.depth_slider_scale, 1))))

        self.disp_ctrl.widgets['dmp_scale'].sliderReleased.connect(lambda: self.update_slider(
            10**(self.disp_ctrl.widgets['dmp_scale'].value() / self.depth_slider_scale), 'scale'))

        self.update_slider(self.disp_ctrl.widgets['dmp_scale'].value(), 'scale')

        # endregion

        # Initializes the sliders to the values of the data processor
        self.init_slider()

        # endregion

        # region Hooks up the ROI button

        self.disp_ctrl.widgets['roi_btn'].clicked.connect(self.toggle_roi)

        self.update_roi(True)

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

        if msg.data is None:
            print_warning('Trying to display empty frame!')
            return

        img = msg.data[0]
        depth = msg.data[1]
        # print(depth.shape[0], ", ", depth.shape[1])

        img_disp = self.disp_ctrl.widgets['img']
        img_disp.setImage(img)

        if len(self.data_proc.state_queue) < self.data_proc.buffer_limit:

            if self.use_roi:

                # Generates the roi coordinates only if the roi has been changed, this takes a long time (~50 ms)
                if self.roi_coords is None:
                    self.roi_coords = self.roi.getArrayRegion(ct.get_roi_coords_matrix(img.shape[0], img.shape[1]),
                                                              img_disp.getImageItem())
                    self.data_proc.rx.emit(JMsg('enable_roi', self.roi_coords))

            else:
                self.data_proc.rx.emit(JMsg('disable_roi'))

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

    def plot_cloud(self, data, colors):
        """Plots the pointcloud onto the window."""
        # dimg = ct.create_color_depth_image(data, colors, self.cam_ctrl.height, self.cam_ctrl.width)
        # self.disp_ctrl.widgets['dimg'].setImage(dimg)
        dmp_avg, dmp_min, dmp_max = ct.average_depth(data)
        self.disp_ctrl.widgets['dmp_avg_lbl'].setText('Average depth: {} m'.format(round(dmp_avg, 2)))
        self.disp_ctrl.widgets['dmp_min_lbl'].setText('Minimum depth: {} m'.format(round(dmp_min, 2)))
        self.disp_ctrl.widgets['dmp_max_lbl'].setText('Maximum depth: {} m'.format(round(dmp_max, 2)))

        data = ct.apply_depth_scale(data, self.data_proc.scale)
        self.scatter.setData(pos=data, color=colors)

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

        self.disp_ctrl_update.emit(JMsg('create_button',
                                   get_text_widg_dict('roi', 'roi_btn', 0, 1, col_span=3,
                                                      tip='Create a new <b>ROI</b> (region of interest)' +
                                                      ' or edit the current one.')))
        #
        # self.disp_ctrl_update.emit(JMsg('create_button',
        #                            get_text_widg_dict('Exit', 'exit_btn', 2, 1, 'Exit the program')))
        # self.disp_ctrl.widgets['exit_btn'].clicked.connect(self.stop)

        # endregion

        # region Sets up the colormap sliders

        self.disp_ctrl_update.emit(JMsg('create_label',
                                   get_text_widg_dict('Max', 'cmap_max_lbl', 4, 1)))
        self.disp_ctrl_update.emit(JMsg('create_slider',
                                   get_slider_widg_dict(Qt.Vertical, 'cmap_max', 5, 1,
                                                        tip='Adjusts the upper saturation limit of the colormap')))
        self.disp_ctrl_update.emit(JMsg('create_label',
                                        get_text_widg_dict('3.0 m', 'cmap_max_lbl_val', 6, 1)))

        self.disp_ctrl_update.emit(JMsg('create_label',
                                   get_text_widg_dict('Mid', 'cmap_mid_lbl', 4, 2)))
        self.disp_ctrl_update.emit(JMsg('create_slider',
                                   get_slider_widg_dict(Qt.Vertical, 'cmap_mid', 5, 2,
                                                        tip='Adjusts the mid-point of the colormap')))
        self.disp_ctrl_update.emit(JMsg('create_label',
                                        get_text_widg_dict('1.5 m', 'cmap_mid_lbl_val', 6, 2)))

        self.disp_ctrl_update.emit(JMsg('create_label',
                                   get_text_widg_dict('Min', 'cmap_min_lbl', 4, 3)))
        self.disp_ctrl_update.emit(JMsg('create_slider',
                                   get_slider_widg_dict(Qt.Vertical, 'cmap_min', 5, 3,
                                                        tip='Adjusts the lower saturation limit of the colormap')))
        self.disp_ctrl_update.emit(JMsg('create_label',
                                        get_text_widg_dict('0.0 m', 'cmap_min_lbl_val', 6, 3)))

        self.disp_ctrl_update.emit(JMsg('create_label',
                                        get_text_widg_dict('Depth Scale: {} x'.format(self.depth_scale_max >> 1),
                                                           'dmp_scale_lbl', 7, 0)))
        self.disp_ctrl.widgets['dmp_scale_lbl'].setAlignment(Qt.AlignLeft)
        self.disp_ctrl_update.emit(JMsg('create_slider',
                                        get_slider_widg_dict(Qt.Horizontal, 'dmp_scale', 6, 0)))

        # endregion

        # region Sets up the depth data labels

        self.disp_ctrl_update.emit(JMsg('create_label',
                                        get_text_widg_dict('Average depth: 0.0 m', 'dmp_avg_lbl', 1, 1, 1, 3)))
        self.disp_ctrl_update.emit(JMsg('create_label',
                                        get_text_widg_dict('Minimum depth: 0.0 m', 'dmp_min_lbl', 2, 1, 1, 3)))
        self.disp_ctrl_update.emit(JMsg('create_label',
                                        get_text_widg_dict('Maximum depth: 0.0 m', 'dmp_max_lbl', 3, 1, 1, 3)))

        # endregion

        # region Sets up the plots

        self.disp_ctrl_update.emit(JMsg('create_label',
                                   get_text_widg_dict('Grayscale', 'img_lbl', 0, 0)))
        self.disp_ctrl_update.emit(JMsg('create_widget',
                                   get_custom_widg_dict(pg.ImageView, 'img', 1, 0, 3, 1)))

        # self.disp_ctrl_update.emit(JMsg('create_label',
        #                                 get_text_widg_dict('Depth Image', 'dimg_lbl', 0, 1)))
        # args = get_custom_widg_dict(pg.ImageView, 'dimg', 1, 1, 1, 3)
        # self.disp_ctrl_update.emit(JMsg('create_widget',
        #                                 args))

        self.disp_ctrl_update.emit(JMsg('create_label',
                                   get_text_widg_dict('Point Cloud', 'dmp_lbl', 4, 0)))
        self.disp_ctrl_update.emit(JMsg('create_widget',
                                   get_custom_widg_dict(pgl.GLViewWidget, 'dmp', 5, 0)))

        self.scatter = pgl.GLScatterPlotItem(pos=np.zeros(shape=(307200, 3), dtype=float), size=3)
        self.disp_ctrl.widgets['dmp'].addItem(self.scatter)

        # region view formatting

        self.scatter.rotate(180, 0, 0, 0)
        self.scatter.setGLOptions('opaque')
        widg = self.disp_ctrl.widgets['dmp']
        # widg.mouseReleaseEvent = lambda v: self.update_center_display()
        widg.pan(-320, -240, 0)
        widg.setCameraPosition(distance=1746, elevation=43, azimuth=-479)

        # endregion

        # endregion

        # Sets up the filename bar

        self.disp_ctrl_update.emit(JMsg('create_text_entry',
                                        get_text_entry_widg_dict('file_entry', 7, 1, 1, 3,
                                                                 tip='Enter a video filename to load in.')))

    # def update_center_display(self):
    #     opts = self.disp_ctrl.widgets['dmp'].opts
    #     self.set_status("Ready pos: {}, {}, {}".format(opts['distance'], opts['elevation'], opts['azimuth']))

    def init_slider(self):
        self.disp_ctrl.widgets['cmap_max'].setValue(self.data_proc.cmap_up * self.slider_scale)
        self.disp_ctrl.widgets['cmap_mid'].setValue(self.data_proc.cmap_mid * self.slider_scale)
        self.disp_ctrl.widgets['cmap_min'].setValue(self.data_proc.cmap_low * self.slider_scale)

    def update_slider(self, value: int, slider: str):
        """Updates the value of the adjusted slider"""

        if slider != 'scale':
            value /= self.slider_scale

        self.set_status('Updating slider bars')
        self.data_proc.cmap_up_to_date = False
        self.data_proc.rx.emit(JMsg(slider, value))

        q = queue.Queue()

        def linker():
            global q
            q.put(True)

        sl = self.data_proc.slider_tx.connect(linker)

        q.get()

        self.data_proc.slider_tx.disconnect(sl)

        self.set_slider_limits()
        self.reset_status()

    def update_roi(self, enable: bool = True):
        """Triggered when the ROI of the image changes"""

        if enable:
            if not self.use_roi:
                self.set_status("Enabling ROI")
                self.use_roi = True
                if self.roi is None:
                    self.roi = pg.PolyLineROI([[10, 10], [20, 200], [100, 300], [300, 100]],
                                              closed=True, movable=True, removable=True)
                    self.roi.sigRegionChangeFinished.connect(self.update_roi)
                    # self.roi.sigRemoveRequested.connect(lambda: self.update_roi(False))
                self.disp_ctrl.widgets['img'].getView().addItem(self.roi)
            self.set_status("Flagging ROI update")
            self.roi_coords = None  # Flags for the generation of coords on the next frame.
            self.reset_status()

        if not enable and self.use_roi:
            self.set_status("Disabling ROI")
            self.use_roi = False
            self.disp_ctrl.widgets['img'].getView().removeItem(self.roi)
            self.reset_status()

    def toggle_roi(self):
        self.use_roi = not self.use_roi
        self.update_roi(self.use_roi)

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

    def reset_status(self):
        self.set_status('Ready')


if __name__ == "__main__":
    import sys
    import roypy_sample_utils
    import argparse

    app = QApplication(sys.argv)

    # mgr = DequeManager()
    # mgr.start()

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
