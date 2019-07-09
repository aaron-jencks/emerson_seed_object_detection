from multiprocessing import Queue

from video_util.cam import RealsenseCam
from video_util.multiprocessing import SplitCamServer
from server_util.server import VideoStreamingServer, VideoStreamingHandler


server_name = 'CameraServer'


def main():
    cam = RealsenseCam()
    cam.start_streams()

    c_q = Queue()
    i_q = Queue()
    d_q = Queue()

    cam_server = SplitCamServer(cam, c_q, i_q, d_q)

    rgb_server = VideoStreamingServer("{}_rgb".format(server_name), c_q)
    ir_server = VideoStreamingServer("{}_ir".format(server_name), i_q)
    depth_server = VideoStreamingServer("{}_depth".format(server_name), d_q)

    rgb_server.serve_forever()


if __name__ == "__main__":
    cam = RealsenseCam()
    cam.start_streams()

    with VideoStreamingServer(cam=cam, device_identifier=server_name,
                              server_address=('localhost', 0)) as server:
        print('Starting server on port {}'.format(server.socket.getsockname()[1]))
        server.serve_forever()
