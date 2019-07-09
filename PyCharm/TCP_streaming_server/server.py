from multiprocessing import Queue
import time

from video_util.cam import RealsenseCam
from video_util.data import VideoStream, VideoStreamType
from video_util.multiprocessing import SplitCamServer
from server_util.multiprocessing.server import VideoStreamServerWrapper

cam_num = 0
server_name = 'CameraServer_{}'.format(cam_num)


def main():
    cam = RealsenseCam

    c_q = Queue(10)
    d_q = Queue(10)

    cam_server = SplitCamServer(cam_type=cam, rgb_q=c_q, depth_q=d_q, ignore_if_full=False)

    rgb_server = VideoStreamServerWrapper("{}_rgb".format(server_name), c_q, server_address=('localhost', 0),
                                          stream_type=VideoStream('rgb', (720, 1280), 30, VideoStreamType.RGB))

    depth_server = VideoStreamServerWrapper("{}_depth".format(server_name), d_q, server_address=('localhost', 0),
                                            stream_type=VideoStream('depth', (640, 480), 30, VideoStreamType.Z16))

    # cam_server.start()
    rgb_server.start()
    depth_server.start()

    cam_server.run()

    try:
        while cam_server.is_alive() and rgb_server.is_alive() and ir_server.is_alive() and depth_server.is_alive():
            time.sleep(1)
    finally:
        cam_server.join()
        rgb_server.join()
        depth_server.join()

        c_q.close()
        d_q.close()


if __name__ == "__main__":
    main()
