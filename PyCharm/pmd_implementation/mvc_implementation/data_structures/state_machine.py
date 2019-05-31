import time
import sys
import traceback

import threading
from PyQt5.QtCore import pyqtSignal, QObject, QThread

from collections import deque

from mvc_implementation.dependencies.display_util.string_display_util import print_warning

from colorama import Fore


class JMsg:
    """Used to send information from one daemon to another."""

    def __init__(self, message: str, data: object = None):
        self.message = message
        self.data = data

    def __str__(self):
        return "{}: {}".format(self.message, str(self.data))


class StateMachine(QObject):
    """Represents a state machine that can be ran on another thread."""

    state_queue = pyqtSignal([str, JMsg])

    def __init__(self, auto_start: bool = False, **kwargs):
        super().__init__(**kwargs)

        self.isStopping = False
        self.state_queue = deque()
        self.states = {'init': self.initial_state, 'STOP': self.final_state, 'idle': self.idle_state}
        self.state_queue.append(JMsg('init'))

        # Used to transfer JMsg data to individual states
        self.data = None

        if auto_start:
            self.run()

    def run(self):
        self.isStopping = False
        while not self.isStopping:
            meth = self.get_next_state()

            # Runs the selected state
            try:
                meth()
            except Exception as e:
                et, ev, tb = sys.exc_info()
                exc = "Exception was thrown: {}\n".format(e)
                for l in traceback.format_exception(et, ev, tb):
                    exc += l
                exc += '\nExitting...'
                print_warning(exc)
                self.stop()

    def stop(self) -> None:
        """Flags the thread to stop running."""
        self.isStopping = True

    def get_next_state(self):
        """Collects the next state from the state_queue, if it doesn't exist, or the queue is empty, goes to idle."""
        if len(self.state_queue) == 0:
            return self.states['idle']
        else:
            msg = self.state_queue.popleft()

            # If the incoming state is a JMsg, append the message data, and set self.data as the JMsg to be handled
            # by the state specified by the JMsg.
            if isinstance(msg, JMsg):
                self.data = msg
                msg = msg.message

            return self.states[msg]

    # region States

    def initial_state(self):
        """The first state executed by the state machine."""
        pass

    def idle_state(self):
        """This state does nothing, it is used when the machine has nowhere else to go."""
        time.sleep(0.1)
        pass

    def final_state(self):
        """This is the final state executed by the state machine."""
        self.isStopping = True

    # endregion


class SocketedStateMachine(StateMachine):
    """Represents a state machine with a queue that connects it with the rest of the world"""

    tx = pyqtSignal([JMsg])
    rx = pyqtSignal([JMsg])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.rx.connect(self.__recieve_msg)

    def __recieve_msg(self, msg: JMsg):
        self.state_queue.append(msg)


class ThreadedStateMachine(QThread, StateMachine):
    """Represents a state machine that can be ran on another thread."""

    def __init__(self, parent=None, auto_start: bool = False, **kwargs):
        super().__init__()  # auto_start)
        StateMachine.__init__(self, auto_start)

        self.isStopping = False
        self.state_queue = deque()
        self.states = {'init': self.initial_state, 'STOP': self.final_state, 'idle': self.idle_state}
        self.state_queue.append('init')
        self.parent = parent

        # Used to transfer JMsg data to individual states
        self.data = None

        if auto_start:
            self.run()

    def join(self, timeout: float = -1) -> None:
        """Flags the thread to stop running."""
        self.stop()
        super().join(timeout)


class ThreadedSocketedStateMachine(ThreadedStateMachine):
    """Represents a state machine with a queue that connects it with the rest of the world"""

    tx = pyqtSignal([JMsg])
    rx = pyqtSignal([JMsg])

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.rx.connect(self.__recieve_msg)

    def __recieve_msg(self, msg: JMsg):
        self.state_queue.append(msg)
