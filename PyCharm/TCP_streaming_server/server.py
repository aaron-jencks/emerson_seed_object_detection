from multiprocessing import Queue
import time

from video_util.cam import RealsenseCam
from video_util.data import VideoStream, VideoStreamType
from video_util.multiprocessing import SplitCamServer
from server_util.multiprocessing.server import VideoStreamServerWrapper

cam_num = 0
server_name = 'CameraServer_{}'.format(cam_num)
cam_settings_filename = 'C:\\Users\\aaron.jencks\\Documents\\' \
                        'GitHub\\emerson_seed_object_detection\\realsense_cam_settings.json'
address = 'localhost'  # '10.42.0.76'


def main():
    cam = RealsenseCam

    c_q = Queue(10)
    d_q = Queue(10)

    cam_server = SplitCamServer(cam_type=cam, rgb_q=c_q, depth_q=d_q, ignore_if_full=False,
                                configuration_file=cam_settings_filename)

    rgb_server = VideoStreamServerWrapper("{}_rgb".format(server_name), c_q, server_address=(address, 0),
                                          stream_type=VideoStream('rgb', (1280, 720), 30, VideoStreamType.RGB))

    depth_server = VideoStreamServerWrapper("{}_depth".format(server_name), d_q, server_address=(address, 0),
                                            stream_type=VideoStream('depth', (640, 480), 30, VideoStreamType.Z16,
                                                                    depth_scale=0.001))

    # cam_server.start()
    rgb_server.start()
    depth_server.start()

    cam_server.run()

    try:
        while cam_server.is_alive():  # and rgb_server.is_alive() and depth_server.is_alive():
            print('\rCam Server: {} fps, RGB Server: {} fps, Depth Server: {}'.format(round(cam_server.fps, 3),
                                                                                      round(rgb_server.server.fps, 3),
                                                                                      round(depth_server.server.fps, 3)
                                                                                      ))
    finally:
        cam_server.join()
        rgb_server.join()
        depth_server.join()

        c_q.close()
        d_q.close()


if __name__ == "__main__":
    main()
