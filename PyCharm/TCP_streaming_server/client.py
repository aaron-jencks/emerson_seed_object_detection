import socket
import numpy as np
import time
from multiprocessing import Process, Queue
from queue import Empty

import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QLabel
from PyQt5.QtCore import QThread

from server_util.datapacket_util import VideoStreamDatagram, VideoInitDatagram
from server_util.client import readline
from video_util.data import VideoStreamType
import video_util.cy_collection_util as cu


scale = 0.001


def frame_socket(port: int, output_q: Queue, stop_q: Queue, fps_q: Queue, hostname: str = 'localhost'):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((hostname, port))

        print('Successfully connected to {}:{}'.format(hostname, port))

        streams = None
        device = None
        name = None
        frame = None
        dtype = None
        iteration = 0

        first = True
        while stop_q.empty():
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

                if device is not None:
                    output_q.put(VideoStreamDatagram(device, name, frame, dtype, False))

                elapsed = time.time() - start
                fps = round((1 / elapsed) if elapsed != 0 else np.inf, 3)
                fps_q.put(fps)
                # print('\rProcessing at {} fps, avg depth {}'.format(fps, round(avg, 3)), end='')


class WindowUpdater(QThread):

    stop_q = Queue()

    def __init__(self, cam_q: Queue, img_control: pg.ImageView, fps_q: Queue, fps_lbl: QLabel,
                 lbl: QLabel = None, **kwargs):
        super().__init__(**kwargs)

        self.fq = fps_q
        self.f_lbl = fps_lbl

        self.q = cam_q
        self.lbl = lbl

        self.c = img_control

        self.depth_levels = (0, 65536)

    def run(self) -> None:
        while self.stop_q.empty():
            try:
                timg = self.q.get_nowait()
                fps = self.fq.get_nowait()

                if timg.dtype == VideoStreamType.Z16:
                    self.c.setImage(timg.frame, levels=self.depth_levels)
                    if self.lbl is not None:
                        avg, _, _ = cu.average_depth(timg.frame)
                        avg *= scale * 39.3701
                        self.lbl.setText('Average Depth: {}'.format(avg))
                else:
                    self.c.setImage(timg.frame)

                self.f_lbl.setText('FPS: {} fps'.format(fps))
            except Empty:
                time.sleep(0.1)


if __name__ == '__main__':
    import sys

    # TODO Ask the user which streams they want to enable to allow control over rgb and depth streams

    stop_q = WindowUpdater.stop_q  # Allows control over processes, I can stop them without hanging

    hosts = []
    depth_qs = {}
    rgb_qs = {}
    processes = []

    num_servers = int(input('How many servers are you connecting to? '))

    for server in range(num_servers):

        d_q = Queue()
        fd_q = Queue()
        rgb_q = Queue()
        frgb_q = Queue()

        host = input('Hostname for server {}? '.format(server))
        hosts.append(host)

        md = input("Would you like to stream both RGB and Depth, if no, I'll just stream Depth? (y/n) ").capitalize()
        while md != 'Y' and md != 'N':
            print('Lets try that again, shall we...')
            md = input(
                "Would you like to stream both RGB and Depth, if no, I'll just stream Depth? (y/n) ").capitalize()

        depth_qs[host] = {'img': d_q, 'fps': fd_q}

        if md == 'Y':
            rgb_qs[host] = {'img': rgb_q, 'fps': frgb_q}
            processes.append(Process(target=frame_socket, args=(int(input('RGB Port Number: ')),
                                                                rgb_q, stop_q, frgb_q, host)))

        processes.append(Process(target=frame_socket, args=(int(input('Depth Port Number: ')),
                                                            d_q, stop_q, fd_q, host)))

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

    threads = []

    for i, server in enumerate(hosts):
        row = i * 4

        d_img = pg.ImageView(window)
        dfps_lbl = QLabel('FPS: 0 fps', window)
        rgb_img = pg.ImageView(window)
        rgbfps_lbl = QLabel('FPS: 0 fps', window)

        avg_lbl = QLabel('Average Depth: 0', window)

        grid.addWidget(QLabel('{}'.format(server), window), row, 0)

        if server in rgb_qs:
            grid.addWidget(d_img, row + 1, 0)
            grid.addWidget(rgb_img, row + 1, 1)
            grid.addWidget(dfps_lbl, row + 2, 0)
            grid.addWidget(rgbfps_lbl, row + 2, 1)
        else:
            grid.addWidget(d_img, row + 1, 0, 1, 2)
            grid.addWidget(dfps_lbl, row + 2, 0)

        grid.addWidget(avg_lbl, row + 3, 0)

        d_img_item = pg.ImageItem()
        rgb_img_item = pg.ImageItem()
        d_img.addItem(d_img_item)
        rgb_img.addItem(rgb_img_item)

        # Will allow me to show selected streams later
        if server in depth_qs:
            qs = depth_qs[server]
            threads.append(WindowUpdater(qs['img'], d_img, qs['fps'], dfps_lbl, lbl=avg_lbl))

        if server in rgb_qs:
            qs = rgb_qs[server]
            threads.append(WindowUpdater(qs['img'], rgb_img, qs['fps'], rgbfps_lbl))

    for t in threads:
        t.start()

    app.exec_()

    stop_q.put(True)  # Signals to end all zombie processes

    # endregion


