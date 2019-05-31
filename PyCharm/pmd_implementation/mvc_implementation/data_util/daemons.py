import numpy as np
import pyximport; pyximport.install(setup_args={"include_dirs":np.get_include()})
from mvc_implementation.data_structures.state_machine import ThreadedSocketedStateMachine, JMsg
import mvc_implementation.data_util.cy_scatter as ct
import pyqtgraph as pg
import time

from PyQt5.QtCore import QObject, pyqtSignal


class DataDaemon(ThreadedSocketedStateMachine):

    buffer_limit = 10

    def __init__(self):
        super().__init__()

        self.states['frame'] = self.process

    def process(self, parsing_data: dict):
        if not parsing_data['roi']:

            if parsing_data['roi_coords'] is None:
                result = ct.scatter_data(parsing_data['frame'])
            else:
                result = ct.apply_roi(parsing_data['frame'], parsing_data['roi_coords'])

            colors = ct.create_color_data(result,
                                          parsing_data['cmap_low'], parsing_data['cmap_mid'], parsing_data['cmap_up'])

            self.tx.emit(JMsg('process_update', {'vectors': result, 'colors': colors}))
