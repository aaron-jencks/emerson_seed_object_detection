import socket
from multiprocessing import Lock, Process, Queue
import time

# import pyqtgraph as pg
# from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QLabel
# from PyQt5.QtCore import pyqtSlot

from dependencies.queue_ops import lossy_enqueue


buffsize = 3072000


class SocketInfo:
    """Contains a socket object as well as the port and hostname"""
    def __init__(self, port: int, hostname: str, auto_connect: bool = True):
        self.port = port
        self.host = hostname
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.is_connected = False
        self.residual_data = ''

        if auto_connect:
            self.connect()

    def __del__(self):
        self.sock.close()

    def connect(self):
        self.sock.connect((self.host, self.port))
        self.is_connected = True

    def readline(self) -> str:
        """Continuously calls read on the given socket until a '\n' is found,
        then saves the residual and returns the string"""

        if not self.is_connected:
            self.connect()

        if '~~~\n' in self.residual_data:
            index = self.residual_data.find('~~~\n')

            temp = self.residual_data[:index]

            if index < len(self.residual_data) - 4:
                self.residual_data = self.residual_data[index + 4:]
            else:
                self.residual_data = ''

            return temp

        result = self.residual_data

        data_read = self.sock.recv(buffsize).decode('latin-1')
        while data_read != '' and '~~~\n' not in data_read:
            result += data_read
            data_read = self.sock.recv(buffsize).decode('latin-1')

        if data_read != '':
            index = data_read.find('~~~\n')
            result += data_read[:index]
            if index < len(data_read) - 4:
                self.residual_data = data_read[index + 4:]
            else:
                self.residual_data = ''

        return result


class InterwovenSocketReader(Process):
    """Reads data from multiple sockets equally, ensuring equal framerates coming from multiple cameras."""

    stop_q = Queue(1)

    def __init__(self, sockets: list, qs: list):
        super().__init__()
        self.sockets = sockets
        self.qs = qs

    def join(self, **kwargs):
        self.stop_q.put(True)
        super().join(**kwargs)

    def run(self) -> None:
        while self.stop_q.empty():
            for i in range(len(self.sockets)):
                s = self.sockets[i]
                q, fq = self.qs[i]

                start = time.time()
                data = s.readline()

                lossy_enqueue(q, data)
                elapsed = time.time() - start

                if fq is not None:
                    lossy_enqueue(fq, (1 / elapsed) if elapsed > 0 else 0)


# class ClientWidget(QWidget):
#     def __init__(self, hosts: list, depth_qs: dict, rgb_qs: dict):
#         super().__init__()
#
#         self.hosts = hosts
#         self.dqs = depth_qs
#         self.cqs = rgb_qs
#
#         self.grid = QGridLayout()
#         self.grid.setSpacing(10)
#         self.setLayout(self.grid)
