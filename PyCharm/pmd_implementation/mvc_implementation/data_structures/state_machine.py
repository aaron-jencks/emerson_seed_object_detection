import time
import sys
import traceback

import threading
import multiprocessing as mp
from PyQt5.QtCore import pyqtSignal, QObject, QThread, QProcess

from collections import deque
from mvc_implementation.data_structures.Q import DequeManager, DictProxy

from mvc_implementation.dependencies.display_util.string_display_util import print_warning, print_notification

from queue import Queue

from colorama import Fore


class JMsg:
    """Used to send information from one daemon to another."""

    def __init__(self, message: str, data: object = None):
        self.message = message
        self.data = data

    def __str__(self):
        return "{}: {}".format(self.message, str(self.data))


class StateManagerModule(QThread):
    """Handles the queueing and unqueueing of events for the state machines, in a non-blocking way."""

    next_state = pyqtSignal(str, object)

    def __init__(self, state_queue: Queue, auto_start: bool = True, block_idle: bool = True):
        super().__init__()

        self.state_queue = state_queue if state_queue is not None else Queue
        self.isStopping = False
        self.use_idle_state = block_idle

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
            else:
                time.sleep(0.5)

    def stop(self):
        self.isStopping = True

    def get_next_state(self):
        """Collects the next state from the state_queue, if it doesn't exist, or the queue is empty, goes to idle."""
        if self.state_queue.qsize() == 0:
            if self.use_idle_state:
                return 'idle', None
        else:
            msg, data = self.state_queue.get()
            return msg, data


class StateMachine:
    """Represents a state machine that can be ran on another thread."""

    def __init__(self, state_manager: DequeManager = None, auto_start: bool = False, **kwargs):
        super().__init__(**kwargs)

        self.isStopping = False
        self.state_queue = Queue()
        self.state_reg_mgr = state_manager if state_manager is not None else DequeManager()

        if state_manager is None:
            self.state_reg_mgr.start()

        self.states = {'init': self.initial_state, 'STOP': self.final_state, 'idle': self.idle_state}
        self.append_states(['init'])

        self.state_exec_mgr = StateManagerModule(self.state_queue, False)
        self.state_exec_mgr.next_state.connect(self.exec_state)

        if auto_start:
            self.run()

    def exec_state(self, meth, data):
        # Runs the selected state
        if meth in self.states:
            try:
                print_notification("Running {} for {}".format(meth, str(self.__class__)))
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
        else:
            print_warning("{} is not a valid state!".format(meth))

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
        time.sleep(0.5)
        pass

    def final_state(self):
        """This is the final state executed by the state machine."""
        self.isStopping = True
        self.state_exec_mgr.stop()

    # endregion


class SocketedStateMachine(StateMachine):
    """Represents a state machine with a queue that connects it with the rest of the world"""

    def __init__(self, tx_q: mp.Queue, rx_q: mp.Queue, **kwargs):
        super().__init__(**kwargs)

        self.tx = tx_q
        self.rx = rx_q

    def __recieve_msg(self, msg: JMsg):
        self.append_states([msg])

    def idle_state(self):
        if not self.rx.empty():
            msg = self.rx.get()
            self.__recieve_msg(msg)
        else:
            super().idle_state()


class ThreadedStateMachine(StateMachine, QThread):  # , mp.Process):  # threading.Thread):
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

    def __init__(self, tx_q: mp.Queue = None, rx_q: mp.Queue = None, parent=None, **kwargs):
        super().__init__(parent=parent, **kwargs)

        self.tx = tx_q if tx_q is not None else mp.Queue()
        self.rx = rx_q if rx_q is not None else mp.Queue()

    # def start(self, tx_q: mp.Queue = None, rx_q: mp.Queue = None):
    #     super().start()
    #     self.tx = tx_q
    #     self.rx = rx_q

    def __recieve_msg(self, msg: JMsg):
        self.append_states([msg])

    def idle_state(self):
        if not self.rx.empty():
            msg = self.rx.get()
            self.__recieve_msg(msg)
        else:
            super().idle_state()
