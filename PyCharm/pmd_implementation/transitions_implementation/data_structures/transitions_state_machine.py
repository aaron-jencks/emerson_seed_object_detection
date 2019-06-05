from mvc_implementation.dependencies.display_util.string_display_util import print_notification, print_warning

# from transitions import Machine
from transitions.extensions import GraphMachine as Machine
from transitions.extensions.states import Timeout

from PyQt5.QtCore import pyqtSignal, QObject
from collections import deque

import io
from PIL import Image
import matplotlib.pyplot as plt
from IPython.display import display, display_png
import numpy as np
import cv2


class JMsg:
    """Used to send information from one daemon to another."""

    def __init__(self, message: str, data: object = None):
        self.message = message
        self.data = data

    def __str__(self):
        return "{}: {}".format(self.message, str(self.data))


class StateMachine:
    def __init__(self, **kwargs):
        self.states = []
        self.transitions = []
        self.isStopping = False

        self.init_states()

        self.machine = Machine(model=self, states=self.states, transitions=self.transitions, initial='initial',
                               queued=True,
                               auto_transitions=True, title="Queued State Machine", show_conditions=True)

    @property
    def isRunning(self):
        return not self.isStopping

    # region State Definitions

    def init_states(self):
        """Initializes the states and transitions specified in the state machine."""
        self.states.extend(['initial', 'idle', 'stop', 'final state'])

        self.transitions.extend([
            {'trigger': 'initial', 'source': 'initial', 'dest': 'idle'},
            {'trigger': 'stop', 'source': 'idle', 'dest': 'stop'},
            {'trigger': 'final', 'source': 'stop', 'dest': 'final state'},
        ])

    # endregion

    def show_graph(self, **kwargs):
        """Displays the graph on a small window"""
        stream = io.BytesIO()
        self.get_graph(**kwargs).draw(stream, prog='dot', format='png')
        Image.open(stream).show()
        # plt.imshow(Image.open(stream))
        # plt.show()
        # plt.pause(0.001)

    # region States

    def on_exit_initial(self):
        """The first state to be executed by the state machine"""
        pass

    def on_enter_idle(self):
        """This state does nothing, it is used when the machine has nowhere else to go"""
        pass

    def on_enter_final_state(self):
        """This is the final state executed by the state machine."""
        self.isStopping = True

    # endregion


class SocketedStateMachine(QObject, StateMachine):

    tx = pyqtSignal(JMsg)
    rx = pyqtSignal(JMsg)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.msgs = deque()
        self.rx.connect(self.__stash_msg)

    # region States definition

    def init_states(self):
        super().init_states()

        self.states.extend(['receive message', 'send message'])

        self.transitions.extend([
            {'trigger': 'rcv', 'source': 'idle', 'dest': 'receive message'}
        ])

    # endregion

    def __stash_msg(self, msg: JMsg):
        self.msgs.append(msg)

    # region States

    def on_enter_idle_state(self):
        if len(self.msgs) > 0:
            self.rcv(self.msgs.popleft())
        else:
            super().idle_state()

    def on_enter_receive_message(self, msg: JMsg):
        """Triggers the transition from wherever the machine is, to execute the newly received message"""
        self.trigger(msg.message, msg.data)

    def send_msg(self, msg: JMsg):
        """Sends out a message to the rest of the world"""
        self.tx.emit(msg)

    # endregion


class Controller(SocketedStateMachine):
    def init_states(self):
        super().init_states()

        self.states.extend([
            'process a frame',
            'display image',
            'process depth',
            'display depth',
            'update slider',
            'update cmap slider',
            'low',
            'mid',
            'high',
            'update depth slider',
        ])

        self.transitions.extend([
            ['process_frame', 'receive message', 'process a frame'],
            ['cloudify', 'process a frame', 'process depth'],
            ['display_image', 'process a frame', 'display image'],
            ['display_cloud', 'receive message', 'display depth'],
            ['update_slider', 'receive message', 'update slider'],
            ['cmap', 'update slider', 'update cmap slider'],
            ['update_low', 'update cmap slider', 'low'],
            ['update_mid', 'update cmap slider', 'mid'],
            ['update_high', 'update cmap slider', 'high'],
            ['update_depth', 'update slider', 'update depth slider'],
            ['tx', ['display image', 'process depth', 'display depth'], 'send message'],
            ['reset', ['send message', 'update depth slider', 'high', 'mid', 'low'], 'idle'],
        ])


if __name__ == "__main__":
    sm = Controller()
    sm.show_graph()
