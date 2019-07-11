from multiprocessing import Queue
import time

from video_util.cam import RealsenseCam
from video_util.data import VideoStreamType
from video_util.multiprocessing import SplitCamServer

from server_util.datapacket_util import VideoStreamDatagram


if __name__ == "__main__":
    cam = RealsenseCam

    c_q = Queue(10)
    d_q = Queue(10)

    cam_server = SplitCamServer(cam_type=cam, rgb_q=c_q, depth_q=d_q, ignore_if_full=False)
    cam_server.start()
    # cam_server.run()

    datagram = None
    first = True

    while True:
        data = c_q.get()

        if first:
            first = False
            datagram = VideoStreamDatagram('test', 'depth', data, VideoStreamType.RGB)
        else:
            datagram.frame = data

        start = time.time()
        j = datagram.to_json()
        print('\rProcessing at {} fps'.format(1 / (time.time() - start)), end='')

        device, name, frame, dtype = VideoStreamDatagram.from_json(j, (1280, 720))
