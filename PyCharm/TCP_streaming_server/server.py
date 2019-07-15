from multiprocessing import Queue
import time

from video_util.cam import RealsenseCam
from video_util.data import VideoStream, VideoStreamType
from video_util.multiprocessing import SplitCamServer
from server_util.multiprocessing.server import VideoStreamServerWrapper
from server_util.server import find_ip

from dependencies.terminal_display_util import clear

cam_num = 0
server_name = 'CameraServer_{}'.format(cam_num)
cam_settings_filename = 'C:\\Users\\aaron.jencks\\Documents\\' \
                        'GitHub\\emerson_seed_object_detection\\realsense_cam_settings.json'
address = find_ip()  # '10.42.0.76'  # find_ip()


def main():
    cam = RealsenseCam
    cam_fps_q = Queue()

    c_q = Queue(10)
    c_fps_q = Queue()
    c_res = (640, 480)
    c_fr = 30

    d_q = Queue(10)
    d_fps_q = Queue()
    d_res = (640, 480)
    d_fr = 15

    cam_server = SplitCamServer(cam_type=cam, rgb_q=c_q, rgb_resolution=c_res, rgb_framerate=c_fr,
                                depth_q=d_q, depth_resolution=d_res, depth_framerate=d_fr,
                                tx_q=cam_fps_q, ignore_if_full=False,
                                configuration_file=cam_settings_filename)

    rgb_server = VideoStreamServerWrapper("{}_rgb".format(server_name), c_q,
                                          server_address=(address, 6667),
                                          stream_type=VideoStream('rgb', c_res, c_fr, VideoStreamType.RGB),
                                          tx_q=c_fps_q)

    depth_server = VideoStreamServerWrapper("{}_depth".format(server_name), d_q,
                                            server_address=(address, 6668),
                                            stream_type=VideoStream('depth', d_res, d_fr, VideoStreamType.Z16,
                                                                    depth_scale=0.001), tx_q=d_fps_q)

    # cam_server.start()
    rgb_server.start()
    print('rgb pid is {}'.format(rgb_server.pid))
    depth_server.start()
    print('depth server pid is {}'.format(depth_server.pid))

    cam_server.start()
    print('cam server pid is {}'.format(cam_server.pid))

    try:
        rgb_host = c_fps_q.get()
        depth_host = d_fps_q.get()

        while True:  # and rgb_server.is_alive() and depth_server.is_alive():
            c_fps = 0
            try:
                c_fps = c_fps_q.get_nowait()
            except Exception as e:
                pass

            d_fps = 0
            try:
                d_fps = d_fps_q.get_nowait()
            except Exception as e:
                pass

            cam_fps = 0
            try:
                cam_fps = cam_fps_q.get_nowait()
            except Exception as e:
                pass

            # clear()
            # print('RGB Server {}: {}, Depth Server {}: {}'.format(rgb_server.pid, rgb_host[1],
            #                                                       depth_server.pid, depth_host[1]))
            # print('Cam Server {}: {} fps, RGB Server: {} fps, Depth Server: {}'.format(cam_server.pid,
            #                                                                            round(cam_fps, 3),
            #                                                                            round(c_fps, 3),
            #                                                                            round(d_fps, 3)
            #                                                                            ))
            time.sleep(1)
    except Exception as e:
        print(e)
    finally:
        cam_server.join()
        rgb_server.join()
        depth_server.join()

        c_q.close()
        d_q.close()


if __name__ == "__main__":
    main()
