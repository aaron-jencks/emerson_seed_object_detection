from mvc_implementation.dependencies.display_util.string_display_util import print_notification, print_warning

# from transitions import Machine
from transitions.extensions import GraphMachine as Machine
from transitions.extensions.states import Timeout

from PyQt5.QtCore import pyqtSignal, QObject
from collections import deque

import io
from PIL import Image
import matplotlib.pyplot as plt


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
        plt.imshow(Image.open(stream))
        plt.show()
        plt.pause(0.001)

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


if __name__ == "__main__":
    sm = SocketedStateMachine()
    sm.show_graph()
