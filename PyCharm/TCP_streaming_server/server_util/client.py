import socket
from multiprocessing import Lock, Process, Queue
import time
import numpy as np

# import pyqtgraph as pg
# from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QLabel
from PyQt5.QtCore import pyqtSignal, QThread

from dependencies.queue_ops import lossy_enqueue
from video_util.data import VideoStreamType
from server_util.datapacket_util import VideoStreamDatagram, VideoInitDatagram


buffsize = 3072000


class SocketInfo:
    """Contains a socket object as well as the port and hostname"""

    # imageChanged = pyqtSignal(np.ndarray)

    def __init__(self, port: int, hostname: str, types: list, auto_connect: bool = True):
        self.port = port
        self.host = hostname
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.is_connected = False
        self.first = True
        self.residual_data = []
        self.stream_types = types

        if auto_connect:
            self.connect()

    def __del__(self):
        self.sock.close()

    def connect(self):
        if self.is_connected:
            self.sock.close()
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.sock.connect((self.host, self.port))
        if self.first:
            self.first = False
            print('Successfully connected to {}'.format(self.host))
        self.is_connected = True

    def read_all_available(self) -> str:

        if not self.is_connected:
            self.connect()

        result = ''
        data_read = self.sock.recv(buffsize).decode('latin-1')
        while data_read != '':
            result += data_read
            data_read = self.sock.recv(buffsize).decode('latin-1')
        return result

    @staticmethod
    def split_lines(data: str) -> list:
        return data.split('~~~\n')

    def readline(self) -> str:
        """Continuously calls read on the given socket until a '\n' is found,
        then saves the residual and returns the string"""

        if not self.is_connected:
            self.connect()

        if len(self.residual_data) > 1:
            return self.residual_data.pop(0)
        elif len(self.residual_data) == 1:
            result = self.residual_data.pop(0)
        else:
            result = ''

        self.residual_data.extend(self.split_lines(self.read_all_available()))
        result += self.residual_data.pop(0)

        return result


class InterwovenSocketReader(QThread):
    """Reads data from multiple sockets equally, ensuring equal framerates coming from multiple cameras."""

    dataCollected = pyqtSignal(str, VideoInitDatagram)
    imgCollected = pyqtSignal(str, VideoStreamDatagram)
    fpsCollected = pyqtSignal(str, int, float)

    stop_q = Queue(1)

    def __init__(self, sockets: list):  # , qs: list):
        super().__init__()
        self.sockets = sockets
        self.first = [True for _ in sockets]
        self.streams = [None for _ in sockets]
        # self.qs = qs

    def join(self, **kwargs):
        self.stop_q.put(True)
        super().join(**kwargs)

    def run(self) -> None:
        while self.stop_q.empty():
            for i in range(len(self.sockets)):
                device = None
                name = None
                frame = None
                dtype = None

                s = self.sockets[i]
                s.connect()
                # q, fq = self.qs[i]

                start = time.time()
                data = s.readline()

                if data != '':
                    # if self.first[i]:
                    #     self.first[i] = False
                    #     self.streams[i] = VideoInitDatagram.from_json(data)
                    #     self.dataCollected.emit(s.host, self.streams[i])
                    # else:
                    #     device, name, frame, dtype = VideoStreamDatagram.from_json(data,
                    #                                                                self.streams[i].streams[0].resolution)

                    # self.first[i] = False
                    self.streams[i] = VideoInitDatagram.from_json(data)
                    self.dataCollected.emit(s.host, self.streams[i])

                data = s.readline()
                if data != '':
                    device, name, frame, dtype = VideoStreamDatagram.from_json(data,
                                                                               self.streams[i].streams[0].resolution)

                    if device is not None:
                        d = VideoStreamDatagram(device, name, frame, dtype, False)
                        # lossy_enqueue(q, d)
                        self.imgCollected.emit(s.host, d)

                    elapsed = time.time() - start

                    fps = (1 / elapsed) if elapsed > 0 else 0

                    # if fq is not None:
                    #     lossy_enqueue(fq, fps)

                    self.fpsCollected.emit(s.host, s.port, fps)


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
