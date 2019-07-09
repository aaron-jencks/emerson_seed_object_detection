import socket
import numpy as np
import matplotlib.pyplot as plt
import time

from server_util.datapacket_util import VideoStreamDatagram, VideoInitDatagram


host = 'localhost'
buffsize = 1024
residual_data = b''


def readline(sock: socket.socket) -> str:
    """Continuously calls read on the given socket until a '\n' is found,
    then saves the residual and returns the string"""

    global residual_data

    result = residual_data

    data = sock.recv(buffsize)
    while data != b'' and b'\n' not in data:
        result += data
        data = sock.recv(buffsize)

    if data != b'':
        index = data.find(b'\n')
        result += data[:index]
        if index < len(data) - 1:
            residual_data = data[index + 1:]
        else:
            residual_data = b''

    return result


if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect_ex((host, int(input('Port number to connect to? '))))

        streams = None
        framedata = None
        iteration = 0

        first = True
        while True:
            print('\rProcessing frame {}'.format(iteration), end='')
            iteration += 1

            data = readline(sock)
            if data != '':
                if first:
                    first = False
                    print(data)
                    streams = VideoInitDatagram.from_json(data)
                else:
                    framedata = VideoStreamDatagram.from_json(data)

                if framedata is not None:
                    if framedata.name == 'rgb':
                        res = streams.streams[0].resolution
                        rgb_frame = np.rot90(np.reshape(framedata.frame, newshape=(res[0], res[1])))

                        plt.clf()
                        plt.imshow(rgb_frame)
                        plt.draw()
                        plt.pause(0.001)
