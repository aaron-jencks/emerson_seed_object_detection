import numpy as np
import pyximport; pyximport.install(setup_args={"include_dirs":np.get_include()})
from mvc_implementation.data_structures.state_machine import ThreadedSocketedStateMachine, JMsg
import mvc_implementation.data_util.cy_scatter as ct


class DataDaemon(ThreadedSocketedStateMachine):

    buffer_limit = 10

    def __init__(self):
        super().__init__()

        self.full = False

        self.states['frame'] = self.process

    def __recieve_msg(self, msg: JMsg):
        if len(self.state_queue) >= self.buffer_limit:
            self.full = True
            self.tx.emit(JMsg('buffer_full'))
        else:
            super().__recieve_msg(msg)

    def process(self, parsing_data: dict):

        if self.full and len(self.state_queue) < self.buffer_limit:
            self.tx.emit(JMsg('buffer_good'))
            self.full = False

        if parsing_data['roi_coords'] is None:
            result = ct.scatter_data(parsing_data['frame'])
        else:
            result = ct.apply_roi(parsing_data['frame'], parsing_data['roi_coords'])

        colors = ct.create_color_data(result,
                                      parsing_data['cmap_low'], parsing_data['cmap_mid'], parsing_data['cmap_up'])

        self.tx.emit(JMsg('process_update', {'vectors': result, 'colors': colors}))
