import socket
import numpy as np
import matplotlib.pyplot as plt
import time

from server_util.datapacket_util import VideoStreamDatagram, VideoInitDatagram


host = 'localhost'
buffsize = 3072000
residual_data = ''


def readline(sock: socket.socket) -> str:
    """Continuously calls read on the given socket until a '\n' is found,
    then saves the residual and returns the string"""

    global residual_data

    if '\n' in residual_data:
        index = residual_data.find('\n')

        temp = residual_data[:index]

        if index < len(residual_data) - 1:
            residual_data = residual_data[index + 1:]
        else:
            residual_data = ''

        return temp

    result = residual_data

    data_read = sock.recv(buffsize).decode('utf-8')
    while data_read != '' and '\n' not in data_read:
        result += data_read
        data_read = sock.recv(buffsize).decode('utf-8')

    if data_read != '':
        index = data_read.find('\n')
        result += data_read[:index]
        if index < len(data_read) - 1:
            residual_data = data_read[index + 1:]
        else:
            residual_data = ''

    return result


if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, int(input('Port number to connect to? '))))

        streams = None
        framedata = None
        iteration = 0

        first = True
        while True:
            # print('\rProcessing frame {}'.format(iteration), end='')
            iteration += 1

            start = time.time()
            data = readline(sock)
            print('\rIteration {} took {} seconds to read this frame from the internet'.format(iteration,
                                                                                               time.time() - start),
                  end='')
            if data != '':
                if first:
                    first = False
                    streams = VideoInitDatagram.from_json(data)
                else:
                    framedata = VideoStreamDatagram.from_json(data)

                if framedata is not None:
                    if framedata.name == 'rgb':
                        res = streams.streams[0].resolution
                        rgb_frame = np.reshape(framedata.frame, newshape=(res[1], res[0]))

                        plt.clf()
                        plt.imshow(rgb_frame)
                        plt.draw()
                        plt.pause(0.001)
                    if framedata.name == 'depth':
                        res = streams.streams[1].resolution
                        depth_frame = np.reshape(framedata.frame, newshape=(res[1], res[0]))
                        depth_frame = np.multiply(depth_frame, 1 / depth_frame.max())

                        plt.clf()
                        plt.imshow(depth_frame)
                        plt.draw()
                        plt.pause(0.001)
