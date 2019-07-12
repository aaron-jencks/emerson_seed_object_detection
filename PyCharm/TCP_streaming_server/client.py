import socket
import numpy as np
import matplotlib.pyplot as plt
import time
import json
from multiprocessing import Process, Queue
import base64
import struct
import array
from PIL.ImageQt import ImageQt

import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QThread

from server_util.datapacket_util import VideoStreamDatagram, VideoInitDatagram
from server_util.client import readline
from video_util.data import VideoStreamType
import video_util.cy_collection_util as cu


host = 'localhost'
residual_data = ''
scale = 0.001


def frame_socket(port: int, output_q: Queue):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))

        streams = None
        device = None
        name = None
        frame = None
        dtype = None
        iteration = 0
        avg = 0

        first = True
        while True:
            iteration += 1

            start = time.time()
            data = readline(sock)

            # elapsed = time.time() - start
            # print('\rProcessing at {} fps'.format(round((1 / elapsed) if elapsed != 0 else np.inf, 3)), end='')

            if data != '':
                # start = time.time()
                if first:
                    first = False
                    streams = VideoInitDatagram.from_json(data)
                else:
                    device, name, frame, dtype = VideoStreamDatagram.from_json(data, streams.streams[0].resolution)
                    if dtype == VideoStreamType.Z16:
                        avg, _, _ = cu.average_depth(frame)
                        avg *= scale * 39.3701

                if device is not None:
                    output_q.put(VideoStreamDatagram(device, name, frame, dtype, False))

                elapsed = time.time() - start
                print('\rProcessing at {} fps, avg depth {}'.format(round((1 / elapsed) if elapsed != 0 else np.inf, 3),
                                                                    round(avg, 3)), end='')


class WindowUpdater(QThread):
    def __init__(self, cam_q: Queue, img_control: pg.ImageView, **kwargs):
        super().__init__(**kwargs)

        self.q = cam_q
        self.c = img_control

    def run(self) -> None:
        while True:
            timg = self.q.get()
            self.c.setImage(timg.frame)


class RGBWindowUpdater(QThread):
    def __init__(self, cam_q: Queue, img_control: QLabel, **kwargs):
        super().__init__(**kwargs)

        self.q = cam_q
        self.c = img_control

    def run(self) -> None:
        while True:
            timg = self.q.get()
            pix = QPixmap.fromImage(ImageQt(timg.convert('RGBA')))
            self.c.setPixmap(pix)


if __name__ == '__main__':
    import sys

    # TODO Ask how many servers to connect to, then ask for ports and hosts for each one.  Store these into a list
    # TODO that the next section will use to start clients to handle the servers.

    depth_qs = []
    rgb_qs = []
    # processes = []

    d_q = Queue()
    rgb_q = Queue()

    processes = [
                    Process(target=frame_socket, args=(int(input('RGB Port Number: ')), rgb_q)),
                    Process(target=frame_socket, args=(int(input('Depth Port Number: ')), d_q)),
                ]

    for p in processes:
        p.start()

    # region Qt Window

    app = QApplication(sys.argv)
    window = QMainWindow()

    grid = QGridLayout()
    grid.setSpacing(10)
    widg = QWidget()
    widg.setLayout(grid)
    window.setCentralWidget(widg)
    window.show()

    window.setGeometry(300, 300, 500, 400)
    window.setWindowTitle('Remote Viewing Utility')
    window.statusBar().showMessage('Ready')
    window.show()

    # TODO Auto add widgets in a grid fashion, one server per row

    d_img = pg.ImageView(window)
    rgb_img = pg.ImageView(window)  # QLabel(window)
    grid.addWidget(d_img, 0, 0)
    grid.addWidget(rgb_img, 0, 1)
    d_img_item = pg.ImageItem()
    rgb_img_item = pg.ImageItem()  # !
    d_img.addItem(d_img_item)
    rgb_img.addItem(rgb_img_item)  # !

    threads = [WindowUpdater(d_q, d_img), WindowUpdater(rgb_q, rgb_img)]

    for t in threads:
        t.start()

    app.exec_()

    # endregion

    for p in processes:
        p.kill()
