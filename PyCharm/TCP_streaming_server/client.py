import socket
import numpy as np
import time
from multiprocessing import Process, Queue
from threading import Lock
from queue import Empty

import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QLabel
from PyQt5.QtCore import QThread, pyqtSignal, QObject

from dependencies.queue_ops import lossy_enqueue
from server_util.datapacket_util import VideoStreamDatagram, VideoInitDatagram
from server_util.client import SocketInfo, InterwovenSocketReader
from video_util.data import VideoStreamType
import video_util.cy_collection_util as cu


rgb_port = 6667
depth_port = 6668
scale = 0.001
framerate = 30
graph_lock = Lock()


class GUI(QMainWindow):
    def __init__(self, socks: list):
        super().__init__()
        self.grid = QGridLayout()
        self.grid.setSpacing(10)
        self.widg = QWidget()
        self.widg.setLayout(self.grid)

        self.setCentralWidget(self.widg)
        self.show()

        self.setGeometry(300, 300, 500, 400)
        self.setWindowTitle('Remote Viewing Utility')
        self.statusBar().showMessage('Ready')
        self.show()

        self.scales = {}
        self.imgs = {}
        for i, server in enumerate(socks):
            row = i * 4

            d_img = pg.ImageView(self)
            dfps_lbl = QLabel('FPS: 0 fps', self)
            rgb_img = pg.ImageView(self)
            rgbfps_lbl = QLabel('FPS: 0 fps', self)

            avg_lbl = QLabel('Average Depth: 0 inches', self)

            self.grid.addWidget(QLabel('{}'.format(server.host), self), row, 0)

            self.scales[server.host] = 1
            if VideoStreamType.RGB in server.stream_types:
                # server.imageChanged.connect(rgb_img.setImage)
                self.imgs[server.host] = {'depth': d_img, 'rgb': rgb_img,
                                          'depth fps': dfps_lbl, 'rgb fps': rgbfps_lbl,
                                          'avg depth': avg_lbl}
                self.grid.addWidget(d_img, row + 1, 0)
                self.grid.addWidget(rgb_img, row + 1, 1)
                self.grid.addWidget(dfps_lbl, row + 2, 0)
                self.grid.addWidget(rgbfps_lbl, row + 2, 1)
            else:
                # server.imageChanged.connect(d_img.setImage)
                self.imgs[server.host] = {'img': d_img, 'fps': dfps_lbl, 'avg': avg_lbl}
                self.grid.addWidget(d_img, row + 1, 0, 1, 2)
                self.grid.addWidget(dfps_lbl, row + 2, 0)

            self.grid.addWidget(avg_lbl, row + 3, 0)

            d_img_item = pg.ImageItem()
            rgb_img_item = pg.ImageItem()
            d_img.addItem(d_img_item)
            rgb_img.addItem(rgb_img_item)

            # # Will allow me to show selected streams later
            # if VideoStreamType.Z16 in server.stream_types:
            #     qs = depth_qs[server.host]
            #     thread = WindowUpdater(qs['img'], qs['fps'], d_img, dfps_lbl, lbl=avg_lbl)
            #     # thread.imageChanged.connect(lambda x: d_img.setImage(x, levels=(0, 65536)))
            #     self.threads.append(thread)
            #
            # if VideoStreamType.RGB in server.stream_types:
            #     qs = rgb_qs[server.host]
            #     thread = WindowUpdater(qs['img'], qs['fps'], rgb_img, rgbfps_lbl)
            #     # thread.imageChanged.connect(rgb_img.setImage)
            #     self.threads.append(thread)

    def recv_init(self, h: str, data: VideoInitDatagram):
        if h in self.imgs:
            self.scales[h] = data.streams[0].scale

    def recv_fps(self, h: str, p: int, fps: float):
        if h in self.imgs:
            img = self.imgs[h]
            if 'rgb' in img:
                if p == rgb_port and img['rgb fps'] is not None:
                    img['rgb fps'].setText('FPS: {} fps'.format(fps))
                if p == depth_port and img['depth fps'] is not None:
                    img['depth fps'].setText('FPS: {} fps'.format(fps))
            else:
                if p == depth_port and img['fps'] is not None:
                    img['fps'].setText('FPS: {} fps'.format(fps))

    def recv_img(self, h: str, data: VideoStreamDatagram):
        if h in self.imgs:
            img = self.imgs[h]
            if 'rgb' in img:
                if data.dtype == VideoStreamType.RGB and 'rgb' in img:
                    img['rgb'].setImage(data.frame)
                elif data.dtype == VideoStreamType.Z16 and 'depth' in img:
                    img['depth'].setImage(data.frame)

                    if img['avg depth'] is not None:
                        avg, _, _ = cu.average_depth(data.frame)
                        avg *= self.scales[h] * 39.3701
                        img['avg depth'].setText('Average Depth: {} inches'.format(avg))
            else:
                if data.dtype == VideoStreamType.Z16 and 'img' in img:
                    img['img'].setImage(data.frame)

                    if img['avg'] is not None:
                        avg, _, _ = cu.average_depth(data.frame)
                        avg *= self.scales[h] * 39.3701
                        img['avg'].setText('Average Depth: {} inches'.format(avg))


# region frame_socket()
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
# endregion


# region MasterWindowUpdater
# class MasterWindowUpdater(QThread):
#     stop_q = Queue(1)
#
#     def __init__(self, cams: list, **kwargs):
#         super().__init__(**kwargs)
#         self.cams = cams
#
#     def join(self):
#         self.stop_q.put(True)
#         super().join()
#
#     def run(self) -> None:
#         while self.stop_q.empty():
#             for c in self.cams:
#                 try:
#                     timg = c.q.get_nowait()
#                     fps = c.fq.get_nowait()
#
#                     if timg.dtype == VideoStreamType.Z16:
#                         # graph_lock.acquire(True)
#                         c.c.setImage(timg.frame, levels=c.depth_levels)
#                         # graph_lock.release()
#                         # c.imageChanged.emit(timg.frame)
#                         if c.lbl is not None:
#                             avg, _, _ = cu.average_depth(timg.frame)
#                             avg *= c.scale * 39.3701
#                             c.lbl.setText('Average Depth: {} inches'.format(avg))
#                     else:
#                         # c.imageChanged.emit(timg.frame)
#                         c.c.setImage(timg.frame)
#
#                     c.f_lbl.setText('FPS: {} fps'.format(fps))
#                 except Empty:
#                     continue
# endregion


if __name__ == '__main__':
    import sys

    # TODO Ask the user which streams they want to enable to allow control over rgb and depth streams

    # stop_q = WindowUpdater.stop_q  # Allows control over processes, I can stop them without hanging

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
            sockets.append(SocketInfo(rgb_port, host, [VideoStreamType.Z16, VideoStreamType.RGB]))
            qs.append((rgb_q, frgb_q))
            # processes.append(Process(target=frame_socket, args=(rgb_port, rgb_q, stop_q, frgb_q, host)))

        sockets.append(SocketInfo(depth_port, host, [VideoStreamType.Z16]))
        qs.append((d_q, fd_q))
        # processes.append(Process(target=frame_socket, args=(depth_port, d_q, stop_q, fd_q, host)))

    interwover = InterwovenSocketReader(sockets)  # , qs)

    # for p in processes:
    #     p.start()

    # region Qt Window

    app = QApplication(sys.argv)
    window = GUI(sockets)

    interwover.fpsCollected.connect(window.recv_fps)
    interwover.imgCollected.connect(window.recv_img)
    interwover.dataCollected.connect(window.recv_init)

    interwover.start()

    # master = MasterWindowUpdater(threads)
    # master.start()

    sys.exit(app.exec_())

    interwover.join()
    # master.join()

    # stop_q.put(True)  # Signals to end all zombie processes

    # endregion


