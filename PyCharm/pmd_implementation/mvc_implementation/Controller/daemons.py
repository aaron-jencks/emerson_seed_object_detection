from mvc_implementation.data_structures.transitions_state_machine import SocketedStateMachine, JMsg
from mvc_implementation.display_util.daemons import PointCloudDisplayMachine
from mvc_implementation.cam_util.daemons import CamCtrl
from mvc_implementation.data_util.daemons import DataDaemon

from mvc_implementation.dependencies.display_util.string_display_util import *
from mvc_implementation.display_util.display_util import get_yn_dialog_dict, get_file_dialog_dict

import pyqtgraph as pg

import pyximport; pyximport.install()
import mvc_implementation.data_util.cy_scatter as ct

import sys
import traceback

import multiprocessing as mp


class Controller(SocketedStateMachine):
    """Used to separate all of the different modules from the main GUI Thread."""

    slider_scale = 1000
    slider_max = 1
    slider_min = 0
    depth_slider_scale = 100
    depth_scale_max = 4

    def __init__(self, disp_mgr: PointCloudDisplayMachine, **kwargs):
        super().__init__(**kwargs)

        # self.state_exec_mgr.use_idle_state = False

        self.pmd = False
        self.full = False
        self.use_roi = False
        self.roi = None
        self.roi_coords = None
        self.cmap_low = 0
        self.cmap_mid = 1.5
        self.cmap_up = 3
        self.center_x = 0
        self.center_y = 0
        self.center_z = 0
        self.cmap_up_to_date = True
        self.scale = 1.0
        self.prev_skipped = False
        self.frame_count = 1

        self.states['frame_update'] = self.frame_update
        self.states['process_update'] = self.cloud_update
        self.states['buffer_full'] = self.flag_buffer
        self.states['buffer_good'] = self.unflag_buffer
        self.states['init_cam'] = self.init_cam
        self.states['slider cmap_max value'] = self.set_up
        self.states['slider cmap_mid value'] = self.set_mid
        self.states['slider cmap_min value'] = self.set_low
        self.states['slider dmp_scale value'] = self.set_scale
        self.states['toggle_roi'] = self.toggle_roi
        self.states['update_roi'] = self.update_roi
        self.states['enable_roi'] = self.set_roi_coords
        self.states['disable_roi'] = self.unset_roi_coords
        self.states['init_sliders'] = self.init_sliders
        self.states['yes_no_dialog_response'] = self.recording_prompt_response
        self.states['file_dialog_response'] = self.recording_file_response

        # region Sets up the socket  connections

        self.disp_mgr = disp_mgr
        self.disp_ctrl = self.disp_mgr.rx.put
        self.rx = self.disp_mgr.tx
        # self.disp_mgr.tx.connect(self.rx)

        self.cam_tx_q = mp.Queue()
        self.cam_rx_q = mp.Queue()
        self.cam_mgr = CamCtrl(self.rx, self.cam_rx_q)
        self.cam_ctrl = self.cam_mgr.rx.put
        # self.cam_mgr.tx.connect(self.rx)
        self.cam_mgr.start()

        self.data_rx_q = mp.Queue()
        self.data_mgr = DataDaemon(tx_q=self.rx, rx_q=self.data_rx_q)
        self.data_ctrl = self.data_rx_q.put
        # self.data_mgr.tx.connect(self.rx)
        self.data_mgr.start()

        # endregion

        self.append_states(['init_cam', 'init_sliders', 'update_roi'])

    def init_states(self):
        self.states.extend([
            'frame update',
            'process frame',
            'process update',
            'buffer status update',
            'slider value update',
            'roi status update',
            'roi value update',
            'yes/no dialog response',
            'file dialog response'
        ])

        self.transitions.extend([
            {'trigger': 'frame_update', 'source': 'receive message', 'dest': 'frame update', 'after': 'process_frame'},

            {'trigger': 'process_depth', 'source': 'frame update', 'dest': 'process frame',
             'after': 'send_coords_to_proc'},

            {'trigger': 'processor_update', 'source': 'receive message', 'dest': 'process update',
             'after': 'cloud_update'},

            {'trigger': 'buffer_status', 'source': 'receive message', 'dest': 'buffer status update',
             'after': 'buffer_status_update'},

            {'trigger': 'slider_value_update', 'source': 'receive message', 'dest': 'slider value update',
             'after': 'slider_update'},

            {'trigger': 'roi_status_update', 'source': 'receive message', 'dest': 'roi status update',
             'after': 'roi_status'},
        ])

    def buffer_status_update(self, status: bool):
        self.full = status

    # TODO Remove

    def flag_buffer(self):
        self.full = True

    def unflag_buffer(self):
        self.full = False

    def process_frame(self, frames):
        if frames is None:
            print_warning("Trying to display empty frame")

        img = frames[0]
        depth = frames[1]

        self.disp_ctrl(JMsg('display_image', img))

        if not self.full:
            if self.use_roi:
                self.disp_ctrl(JMsg('process_roi', img))
            else:
                self.append_states(['disable_roi'])

            self.process_depth(depth)
            if self.prev_skipped:
                print()
                self.prev_skipped = False
                self.frame_count = 1
                self.disp_ctrl(JMsg('reset_status'))
        else:
            not_string = "Data processor buffer full, skipping {} frames!".format(self.frame_count)

            print_notification(not_string, begin='\r' if self.prev_skipped else '', end='')
            self.disp_ctrl(JMsg('status', not_string))

            self.prev_skipped = True
            self.frame_count += 1

    def cloud_update(self, point_data):
        dmp_avg, dmp_min, dmp_max = ct.average_depth(point_data['vectors'])
        self.disp_ctrl(JMsg('update_slider_label', {'name': 'dmp_avg_lbl',
                                                    'value': 'Average depth: {} m'.format(round(dmp_avg, 2))}))
        self.disp_ctrl(JMsg('update_slider_label', {'name': 'dmp_min_lbl',
                                                    'value': 'Minimum depth: {} m'.format(round(dmp_min, 2))}))
        self.disp_ctrl(JMsg('update_slider_label', {'name': 'dmp_max_lbl',
                                                    'value': 'Maximum depth: {} m'.format(round(dmp_max, 2))}))

        point_data['vectors'] = ct.apply_depth_scale(point_data['vectors'], self.scale)
        self.disp_ctrl(JMsg('display_cloud', point_data))

    def send_coords_to_proc(self, frame):
        self.data_ctrl(JMsg('frame', {
            'roi_coords': self.roi_coords,
            'frame': frame,
            'cmap_low': self.cmap_low,
            'cmap_mid': self.cmap_mid,
            'cmap_up': self.cmap_up
        }))

    # region Point cloud display states
    
    # TODO set_slider_limits after cmap is updated for any of them

    # region Colormap states

    def slider_update(self, data: dict):
        name = data['name']
        value = data['value']
        if name == 'cmap_min':
            self.set_low(value)
        elif name == 'cmap_mid':
            self.set_mid(value)
        elif name == 'cmap_max':
            self.set_up(value)
        else:
            self.set_scale(value)
        
    def set_low(self, value: float):
        self.cmap_low = value
        self.cmap_up_to_date = True

    def set_mid(self, value: float):
        self.cmap_mid = value
        self.cmap_up_to_date = True

    def set_up(self, value: float):
        self.cmap_up = value
        self.cmap_up_to_date = True

    # endregion

    def set_scale(self, value: float):
        self.scale = 10 ** (value / self.disp_mgr.depth_slider_scale)
        self.cmap_up_to_date = True

    def set_roi_coords(self, coords):
        self.roi_coords = coords
        self.use_roi = True

    def unset_roi_coords(self):
        self.roi_coords = None
        self.use_roi = False
        
    def update_roi(self):
        """Triggered when the ROI of the image changes"""

        if not self.use_roi:
            self.disp_ctrl(JMsg('status', "Enabling ROI"))
            self.use_roi = True
            if self.roi is None:
                points = [[10, 10], [20, 200], [100, 300], [300, 100]]

                self.disp_ctrl(JMsg('roi', points))

        self.disp_ctrl(JMsg('status', "Flagging ROI update"))
        self.roi_coords = None  # Flags for the generation of coords on the next frame.
        self.disp_ctrl(JMsg('reset_status'))

    def toggle_roi(self):
        self.use_roi = not self.use_roi

    # endregion

    def init_sliders(self):
        self.disp_ctrl(JMsg('update_slider_value', 
                            {'name': 'cmap_max', 'value': self.cmap_up * self.slider_scale}))
        
        self.disp_ctrl(JMsg('update_slider_value',
                            {'name': 'cmap_mid', 'value': self.cmap_mid * self.slider_scale}))
        
        self.disp_ctrl(JMsg('update_slider_value',
                            {'name': 'cmap_min', 'value': self.cmap_low * self.slider_scale}))
        
        self.disp_ctrl(JMsg('update_slider_value',
                            {'name': 'cmap_max', 'value': (self.slider_min * self.slider_scale,
                                                           self.slider_max * self.slider_scale)}))
        
        self.disp_ctrl(JMsg('update_slider_value',
                            {'name': 'cmap_mid', 'value': (self.slider_min * self.slider_scale,
                                                           self.slider_max * self.slider_scale)}))
        
        self.disp_ctrl(JMsg('update_slider_value',
                            {'name': 'cmap_min', 'value': (self.slider_min * self.slider_scale,
                                                           self.slider_max * self.slider_scale)}))

    def init_cam(self):
        """Initializes the camera connecting to one if possible,
        this is where adjustments need to be made if you want to change the settings."""

        self.change_cam_type()

        if not self.pmd:
            self.cam_ctrl(JMsg('configure_cam', {'ir_stream': {}, 'depth_stream': {}}))

        try:
            self.cam_ctrl(JMsg('start_cam'))
        except Exception as e:
            et, ev, tb = sys.exc_info()
            exc = "Exception was thrown: {}\n".format(e)
            for l in traceback.format_exception(et, ev, tb):
                exc += l
            print_warning(exc)
            self.disp_ctrl(JMsg('yes/no', get_yn_dialog_dict(
                'No Cameras found! Would you like to open a recording instead?')))

    def recording_prompt_response(self, response: bool):
        if response:
            self.disp_ctrl(JMsg('file_dialog', get_file_dialog_dict('Select a recording',
                                                                    valid_files='Royale Recording Files (*.rrf)'
                                                                    if self.pmd else
                                                                    'Realsense Recording Files (*.bak)')))
        else:
            print_notification('Trying to open camera, again.')
            self.append_states(['init_cam'])

    def recording_file_response(self, filename: str):
        self.cam_ctrl('filename', filename)
        print_notification('Opening recording file')
        self.disp_ctrl('status', 'Opening recording file')
        self.append_states(['init_cam'])

    def change_cam_type(self):
        self.cam_ctrl(JMsg('pmd_update', self.pmd))
