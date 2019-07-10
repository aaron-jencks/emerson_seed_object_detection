import socket
import numpy as np
import matplotlib.pyplot as plt
import time
import json
from multiprocessing import Process
import base64
import struct
import array

from server_util.datapacket_util import VideoStreamDatagram, VideoInitDatagram
from video_util.data import VideoStreamType
import video_util.cy_collection_util as cu


host = 'localhost'
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


def frame_socket(port: int):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))

        streams = None
        device = None
        name = None
        frame = None
        dtype = None
        iteration = 0

        first = True
        while True:
            iteration += 1

            # start = time.time()
            data = readline(sock)

            # elapsed = time.time() - start
            # print('\rProcessing at {} fps'.format(round((1 / elapsed) if elapsed != 0 else np.inf, 3)), end='')

            if data != '':
                start = time.time()
                if first:
                    first = False
                    streams = VideoInitDatagram.from_json(data)
                else:
                    device, name, frame, dtype = VideoStreamDatagram.from_json(data)

                if device is not None:
                    if name == 'rgb':
                        res = streams.streams[0].resolution
                        rgb_frame = np.reshape(frame, newshape=(res[1], res[0]))

                        plt.clf()
                        plt.imshow(rgb_frame)
                        plt.draw()
                        plt.pause(0.001)
                    if name == 'ir':
                        res = streams.streams[0].resolution
                        ir_frame = np.reshape(frame, newshape=(res[1], res[0]))

                        plt.clf()
                        plt.imshow(ir_frame)
                        plt.draw()
                        plt.pause(0.001)
                    if name == 'depth':
                        res = streams.streams[0].resolution
                        depth_frame = np.reshape(frame, newshape=(res[1], res[0]))
                        depth_frame = np.multiply(depth_frame, 1 / depth_frame.max())

                        plt.clf()
                        plt.imshow(depth_frame)
                        plt.draw()
                        plt.pause(0.001)

            elapsed = time.time() - start
            print('\rProcessing at {} fps'.format(round((1 / elapsed) if elapsed != 0 else np.inf, 3)), end='')


if __name__ == '__main__':
    processes = [
                    # Process(target=frame_socket, args=(int(input('RGB Port Number: ')),)),
                    Process(target=frame_socket, args=(int(input('Depth Port Number: ')),)),
                ]

    for p in processes:
        p.start()

    for p in processes:
        p.join()
