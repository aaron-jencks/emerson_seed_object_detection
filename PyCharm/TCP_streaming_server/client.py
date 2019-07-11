import socket
import numpy as np
import matplotlib.pyplot as plt
import time
import json
from multiprocessing import Process, Queue
import base64
import struct
import array

import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget
from PyQt5.QtCore import pyqtSignal, QThread

from server_util.datapacket_util import VideoStreamDatagram, VideoInitDatagram
from video_util.data import VideoStreamType
import video_util.cy_collection_util as cu


host = '10.42.0.76'
buffsize = 3072000
residual_data = ''


def readline(sock: socket.socket) -> str:
    """Continuously calls read on the given socket until a '\n' is found,
    then saves the residual and returns the string"""

    global residual_data

    if '~~~\n' in residual_data:
        index = residual_data.find('~~~\n')

        temp = residual_data[:index]

        if index < len(residual_data) - 4:
            residual_data = residual_data[index + 4:]
        else:
            residual_data = ''

        return temp

    result = residual_data

    data_read = sock.recv(buffsize).decode('latin-1')
    while data_read != '' and '~~~\n' not in data_read:
        result += data_read
        data_read = sock.recv(buffsize).decode('latin-1')

    if data_read != '':
        index = data_read.find('~~~\n')
        result += data_read[:index]
        if index < len(data_read) - 4:
            residual_data = data_read[index + 4:]
        else:
            residual_data = ''

    return result


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

                if device is not None:
                    start = time.time()

                    # plt.clf()
                    # plt.imshow(frame)
                    # plt.draw()
                    # plt.pause(0.001)

                    output_q.put(frame)

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
            self.c.setImage(timg)


if __name__ == '__main__':
    import sys

    d_q = Queue()
    rgb_q = Queue()

    processes = [
                    # Process(target=frame_socket, args=(int(input('RGB Port Number: ')), rgb_q)),
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

    d_img = pg.ImageView(window)
    rgb_img = pg.ImageView(window)
    grid.addWidget(d_img, 0, 0)
    grid.addWidget(rgb_img, 0, 1)
    d_img_item = pg.ImageItem()
    rgb_img_item = pg.ImageItem()
    d_img.addItem(d_img_item)
    rgb_img.addItem(rgb_img_item)

    threads = [WindowUpdater(d_q, d_img), WindowUpdater(rgb_q, rgb_img)]

    for t in threads:
        t.start()

    app.exec_()

    # endregion

    for p in processes:
        p.kill()
