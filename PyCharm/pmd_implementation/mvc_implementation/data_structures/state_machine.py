import time
import sys
import traceback

import threading
from PyQt5.QtCore import pyqtSignal, QObject, QThread

from collections import deque
from mvc_implementation.data_structures.Q import DequeManager, DictProxy

from mvc_implementation.dependencies.display_util.string_display_util import print_warning

from queue import Queue

from colorama import Fore


class JMsg:
    """Used to send information from one daemon to another."""

    def __init__(self, message: str, data: object = None):
        self.message = message
        self.data = data

    def __str__(self):
        return "{}: {}".format(self.message, str(self.data))


class StateManagerModule(threading.Thread):
    """Handles the queueing and unqueueing of events for the state machines, in a non-blocking way."""

    next_state = pyqtSignal(str, object)

    def __init__(self, state_queue: Queue, states: DictProxy, auto_start: bool = True):
        super().__init__()

        self.state_queue = state_queue if state_queue is not None else Queue
        self.isStopping = False
        self.states = {} if states is None else states

        if auto_start:
            self.start()

    def run(self):
        self.isStopping = False
        while not self.isStopping:
            state = self.get_next_state()

            # Skips unknown states
            if state is not None:
                meth, data = state

                # Runs the selected state
                self.next_state.emit(meth, data)

    def stop(self):
        self.isStopping = True

    def get_next_state(self):
        """Collects the next state from the state_queue, if it doesn't exist, or the queue is empty, goes to idle."""
        if self.state_queue.qsize() == 0:
            return 'idle', None
        else:
            msg, data = self.state_queue.get()
            if msg in self.states:
                return msg, data


class StateMachine(QObject):
    """Represents a state machine that can be ran on another thread."""

    def __init__(self, state_manager: DequeManager = None, auto_start: bool = False, **kwargs):
        super().__init__(**kwargs)

        self.isStopping = False
        self.state_queue = Queue()
        self.state_reg_mgr = state_manager if state_manager is not None else DequeManager()
        self.states = self.state_reg_mgr.DictProxy({
            'init': self.initial_state, 'STOP': self.final_state, 'idle': self.idle_state})
        self.append_states(['init'])

        self.state_exec_mgr = StateManagerModule(self.state_queue, self.states, False)
        self.state_exec_mgr.next_state.connect(self.exec_state)

        if auto_start:
            self.run()

    def exec_state(self, meth, data):
        # Runs the selected state
        try:
            if data is not None:
                self.states[meth](data)
            else:
                self.states[meth]()
        except Exception as e:
            et, ev, tb = sys.exc_info()
            exc = "Exception was thrown: {}\n".format(e)
            for l in traceback.format_exception(et, ev, tb):
                exc += l
            exc += '\nExitting...'
            print_warning(exc)
            self.stop()

    def run(self):
        self.state_exec_mgr.start()  # Starts the state event loop

    def stop(self) -> None:
        """Flags the thread to stop running."""
        self.append_states(['STOP'])

    def append_states(self, states: list):
        for state in states:
            if isinstance(state, str):
                self.state_queue.put((state, None))
                continue

            try:
                iter(state)
                self.state_queue.put(state)
                continue
            except TypeError:
                if isinstance(state, JMsg):
                    self.state_queue.put((state.message, state.data))
                    continue
                else:
                    raise TypeError('Type {} cannot be enqueued'.format(type(state)))

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
        self.state_exec_mgr.stop()

    # endregion


class SocketedStateMachine(StateMachine):
    """Represents a state machine with a queue that connects it with the rest of the world"""

    tx = pyqtSignal([JMsg])
    rx = pyqtSignal([JMsg])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.rx.connect(self.__recieve_msg)

    def __recieve_msg(self, msg: JMsg):
        self.append_states([msg])


class ThreadedStateMachine(StateMachine, threading.Thread):
    """Represents a state machine that can be ran on another thread."""

    def __init__(self, parent=None, auto_start: bool = False, **kwargs):
        super().__init__(auto_start=auto_start)
        # StateMachine.__init__(self, auto_start)

        # self.isStopping = False
        # self.state_queue = deque()
        # self.states = {'init': self.initial_state, 'STOP': self.final_state, 'idle': self.idle_state}
        # self.state_queue.append('init')
        self.parent = parent

        # Used to transfer JMsg data to individual states
        # self.data = None

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
        self.append_states([msg])
