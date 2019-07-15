import socket
import numpy as np
import time
from multiprocessing import Process, Queue
from threading import Lock
from queue import Empty

import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QLabel
from PyQt5.QtCore import QThread, pyqtSignal

from dependencies.queue_ops import lossy_enqueue
from server_util.datapacket_util import VideoStreamDatagram, VideoInitDatagram
from server_util.client import SocketInfo, InterwovenSocketReader
from video_util.data import VideoStreamType
import video_util.cy_collection_util as cu


scale = 0.001
framerate = 30
graph_lock = Lock()


# def frame_socket(port: int, output_q: Queue, stop_q: Queue, fps_q: Queue, hostname: str = 'localhost'):
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
#         sock.connect((hostname, port))
#
#         print('Successfully connected to {}:{}'.format(hostname, port))
#
#         streams = None
#         device = None
#         name = None
#         frame = None
#         dtype = None
#         spf = 1 / framerate
#
#         first = True
#         while stop_q.empty():
#             start = time.time()
#             data = readline(sock)
#
#             # elapsed = time.time() - start
#             # print('\rProcessing at {} fps'.format(round((1 / elapsed) if elapsed != 0 else np.inf, 3)), end='')
#
#             if data != '':
#                 # start = time.time()
#                 if first:
#                     first = False
#                     streams = VideoInitDatagram.from_json(data)
#                 else:
#                     device, name, frame, dtype = VideoStreamDatagram.from_json(data, streams.streams[0].resolution)
#
#                 if device is not None:
#                     lossy_enqueue(output_q, VideoStreamDatagram(device, name, frame, dtype, False))
#
#                 elapsed = time.time() - start
#                 if elapsed < spf:
#                     diff = spf - elapsed
#                     time.sleep(diff)
#
#                 elapsed = time.time() - start
#
#                 fps = round((1 / elapsed) if elapsed != 0 else np.inf, 3)
#                 lossy_enqueue(fps_q, fps)
#                 # print('\rProcessing at {} fps, avg depth {}'.format(fps, round(avg, 3)), end='')


class WindowUpdater:

    imageChanged = pyqtSignal(np.ndarray)
    stop_q = Queue()

    def __init__(self, cam_q: Queue, fps_q: Queue, cam_img: pg.ImageView, fps_lbl: QLabel,
                 lbl: QLabel = None, **kwargs):
        super().__init__(**kwargs)

        self.fq = fps_q
        self.f_lbl = fps_lbl

        self.c = cam_img
        self.q = cam_q
        self.lbl = lbl
        self.depth_levels = (0, 65536)
        self.scale = 0.0001


class MasterWindowUpdater(QThread):
    stop_q = Queue(1)

    def __init__(self, cams: list, **kwargs):
        super().__init__(**kwargs)
        self.cams = cams

    def join(self):
        self.stop_q.put(True)
        super().join()

    def run(self) -> None:
        while self.stop_q.empty():
            for c in self.cams:
                try:
                    timg = c.q.get_nowait()
                    fps = c.fq.get_nowait()

                    if timg.dtype == VideoStreamType.Z16:
                        # graph_lock.acquire(True)
                        c.c.setImage(timg.frame, levels=c.depth_levels)
                        c.c.updateImage()
                        # graph_lock.release()
                        # c.imageChanged.emit(timg.frame)
                        if c.lbl is not None:
                            avg, _, _ = cu.average_depth(timg.frame)
                            avg *= c.scale * 39.3701
                            c.lbl.setText('Average Depth: {} inches'.format(avg))
                    else:
                        # c.imageChanged.emit(timg.frame)
                        c.c.setImage(timg.frame)
                        c.c.updateImage()

                    c.f_lbl.setText('FPS: {} fps'.format(fps))
                except Empty:
                    continue


if __name__ == '__main__':
    import sys

    # TODO Ask the user which streams they want to enable to allow control over rgb and depth streams

    stop_q = WindowUpdater.stop_q  # Allows control over processes, I can stop them without hanging

    sockets = []
    qs = []
    rgb_qs = {}
    depth_qs = {}

    num_servers = int(input('How many servers are you connecting to? '))

    for server in range(num_servers):

        d_q = Queue(1)
        fd_q = Queue(1)
        rgb_q = Queue(1)
        frgb_q = Queue(1)

        host = input('Hostname for server {}? '.format(server))

        md = input("Would you like to stream both RGB and Depth, if no, I'll just stream Depth? (y/n) ").capitalize()
        while md != 'Y' and md != 'N':
            print('Lets try that again, shall we...')
            md = input(
                "Would you like to stream both RGB and Depth, if no, I'll just stream Depth? (y/n) ").capitalize()

        depth_qs[host] = {'img': d_q, 'fps': fd_q}

        if md == 'Y':
            rgb_qs[host] = {'img': rgb_q, 'fps': frgb_q}
            sockets.append(SocketInfo(6667, host))
            qs.append((rgb_q, frgb_q))
            # processes.append(Process(target=frame_socket, args=(6667, rgb_q, stop_q, frgb_q, host)))

        sockets.append(SocketInfo(6668, host))
        qs.append((d_q, fd_q))
        # processes.append(Process(target=frame_socket, args=(6668, d_q, stop_q, fd_q, host)))

    interwover = InterwovenSocketReader(sockets, qs)
    interwover.start()

    # for p in processes:
    #     p.start()

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

    for i, server in enumerate(sockets):
        row = i * 4

        d_img = pg.ImageView(window)
        dfps_lbl = QLabel('FPS: 0 fps', window)
        rgb_img = pg.ImageView(window)
        rgbfps_lbl = QLabel('FPS: 0 fps', window)

        avg_lbl = QLabel('Average Depth: 0 inches', window)

        grid.addWidget(QLabel('{}'.format(server.host), window), row, 0)

        if _ in rgb_qs:
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
        if server.host in depth_qs:
            qs = depth_qs[server.host]
            thread = WindowUpdater(qs['img'], qs['fps'], d_img, dfps_lbl, lbl=avg_lbl)
            # thread.imageChanged.connect(lambda x: d_img.setImage(x, levels=(0, 65536)))
            threads.append(thread)

        if server.host in rgb_qs:
            qs = rgb_qs[server.host]
            thread = WindowUpdater(qs['img'], qs['fps'], rgb_img, rgbfps_lbl)
            # thread.imageChanged.connect(rgb_img.setImage)
            threads.append(thread)

    master = MasterWindowUpdater(threads)
    master.start()

    sys.exit(app.exec_())

    interwover.join()
    master.join()

    # stop_q.put(True)  # Signals to end all zombie processes

    # endregion


