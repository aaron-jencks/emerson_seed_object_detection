import numpy as np
import pyximport; pyximport.install(setup_args={"include_dirs":np.get_include()})
from pmd_implementation.data_structures.state_machine import ThreadedSocketedStateMachine, JMsg
import pmd_implementation.data_util.cy_scatter as ct
import pyqtgraph as pg
import time

from PyQt5.QtCore import QObject, pyqtSignal


class DataDaemon(ThreadedSocketedStateMachine):

    buffer_limit = 10

    tx = pyqtSignal(np.ndarray, np.ndarray)

    slider_tx = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.roi = False

        # region Color map stuff

        self.cmap_low = 0
        self.cmap_mid = 1.5
        self.cmap_up = 3
        # self.curve_a = 0
        # self.curve_b = 0
        # self.curve_c = 0
        self.center_x = 0
        self.center_y = 0
        self.center_z = 0
        self.cmap_up_to_date = True

        # endregion

        # region roi stuff

        self.roi_coords = None

        # endregion

        self.scale = 1.0

        self.states['frame'] = self.process
        self.states['up'] = self.set_up
        self.states['mid'] = self.set_mid
        self.states['low'] = self.set_low
        self.states['scale'] = self.set_scale
        self.states['enable_roi'] = self.set_roi_coords
        self.states['disable_roi'] = self.unset_roi_coords

    def __recieve_msg(self, msg: JMsg):
        self.state_queue.append(msg)

    def initial_state(self):
        # self.find_curve()
        pass

    def set_low(self):
        self.cmap_low = self.data.data
        self.cmap_up_to_date = True
        # self.find_curve()

    def set_mid(self):
        self.cmap_mid = self.data.data
        self.cmap_up_to_date = True
        # self.find_curve()

    def set_up(self):
        self.cmap_up = self.data.data
        self.cmap_up_to_date = True
        # self.find_curve()

    def set_scale(self):
        self.scale = self.data.data
        self.cmap_up_to_date = True

    def set_roi_coords(self):
        self.roi_coords = self.data.data

    def unset_roi_coords(self):
        self.roi_coords = None

    # def find_curve(self):
    #     self.curve_a, self.curve_b, self.curve_c = ct.find_formula(self.cmap_low, self.cmap_mid, self.cmap_up)

    def process(self):
        if not self.roi:
            # start = time.time()

            # bits = ct.split_data(self.data.data, self.data.data.shape[0], self.data.data.shape[1], 4)
            # points, counts = ct.convert_to_points(bits, self.data.data.shape[0], self.data.data.shape[1], 1)
            # result = ct.concatenate_bits(points, counts)

            if self.roi_coords is None:
                # print(self.data.data.shape)
                result = ct.scatter_data(self.data.data)
            else:
                # print(self.data.data.shape)
                result = ct.apply_roi(self.data.data, self.roi_coords)

            colors = ct.create_color_data(result, self.cmap_low, self.cmap_mid, self.cmap_up)

            # print("Frame took {} seconds to process".format(round(time.time() - start, 3)))
            self.tx.emit(result, colors)
