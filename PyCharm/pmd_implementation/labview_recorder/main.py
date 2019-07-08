import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import pyrealsense2 as rs
import json
import cv2
import os
import sys
from queue import Queue
from collections import deque
from copy import deepcopy
import threading

from dependencies.display_util.string_display_util import *

from tqdm import tqdm
from PIL import Image

import labview_recorder.distribution as db


matplotlib.use('Qt5agg')
np.set_printoptions(threshold=np.inf)


class ConcurrentVideoWriter(threading.Thread):
    def __init__(self, dest: str, q: Queue, fps: int = 30, resolution: tuple = (640, 480), auto_start: bool = True):
        super().__init__()
        try:
            self.dest = dest
            self.writer = cv2.VideoWriter(dest, cv2.VideoWriter_fourcc(*'XVID'), fps, resolution)
            self.q = q

            if auto_start:
                self.start()
        except Exception as e:
            print(e)

    def run(self):
        while True:
            try:
                frame = self.q.get(True, None)
                if frame is not None and not isinstance(frame, int):
                    try:
                        self.writer.write(frame)
                    except Exception as e:
                        print(e)
                else:
                    break
            except Exception as e:
                print(e)
        self.writer.release()


is_stopping = False
cnf_file = "C:\\Users\\aaron.jencks\\Documents\\GitHub\\emerson_seed_object_detection\\realsense_cam_settings.json"
depth_dq = deque()
color_dq = deque()


if __name__ == "__main__":
    in_dir = input("Input file path: ")
    out_dir = input("Ourput file path: ")

    for file in os.listdir(in_dir):
        file = os.path.join(in_dir, file)

        print_notification("Converting {}".format(file))

        ctx = rs.context()
        pipeline = rs.pipeline(ctx)
        config = rs.config()
        rs.config.enable_device_from_file(config, file, False)
        config.enable_all_streams()
        cap = pipeline.start(config)

        scale = cap.get_device().first_depth_sensor().get_depth_scale()

        # cap = cv2.VideoCapture(0)

        print("Depth Scale is {}".format(scale))

        fig, ax = plt.subplots()
        ax.axis('off')

        plot = fig.add_axes([0.1, 0.5, 0.7, 0.4])
        dist = fig.add_axes([0.1, 0.1, 0.7, 0.4])

        print("Saving to {}".format(os.path.join(out_dir,
                                                 '{}_depth.mp4'.format(os.path.splitext(file)[0].split('\\')[-1]))))

        try:
            first = True

            while not is_stopping:

                frames = pipeline.wait_for_frames()
                depth_frame = np.asanyarray(frames.get_depth_frame().get_data(), dtype=np.uint16)
                color_frame = np.asanyarray(frames.get_color_frame().get_data(), dtype=np.uint8)
                # depth_array = np.multiply(np.asanyarray(depth_frame.get_data()), 1)  # scale)

                # depth_frame = np.dstack((depth_frame, depth_frame, depth_frame))

                # m = depth_frame.max()

                # depth_frame = np.float32(np.multiply(depth_frame, 1 / m))

                # depth_frame = np.dstack((depth_frame, depth_frame, depth_frame))

                # print(depth_frame)

                # ret, frame = cap.read()

                depth_frame = db.compute_depth_bytes(depth_frame)

                # print("cv")
                # print(frame.shape)
                # print("rs")
                # print(color_frame.shape)

                plot.clear()
                plot.imshow(depth_frame)
                plot.axis('off')

                # norm = db.normal_distribution(frames)

                dist.clear()
                dist.imshow(color_frame)
                dist.axis('off')
                # dist.hist(np.multiply(norm, scale), range=(-1, 1), histtype='step')
                # dist.hist(norm[:, 1])  # , range=(-5, 5))  # [:, 1])

                plt.draw()
                plt.pause(0.001)

                depth_dq.append(deepcopy(depth_frame))
                color_dq.append(deepcopy(color_frame))

        except RuntimeError as e:
            print_info(str(e))
            print_notification("Finished conversion")
            plt.close(fig)

            print_notification("Saving file")
            color_writer = cv2.VideoWriter(os.path.join(out_dir, '{}_color.avi'.format(
                os.path.splitext(file)[0].split('\\')[-1])), cv2.VideoWriter_fourcc(*'XVID'), 30, (1280, 720))
            for f in tqdm(range(len(color_dq))):
                color_writer.write(color_dq.popleft())
            color_writer.release()

            depth_writer = cv2.VideoWriter(os.path.join(out_dir, '{}_depth.avi'.format(
                os.path.splitext(file)[0].split('\\')[-1])), cv2.VideoWriter_fourcc(*'XVID'), 30, (848, 480))
            for f in tqdm(range(len(depth_dq))):
                depth_writer.write(depth_dq.popleft())
            depth_writer.release()

        finally:
            plt.close(fig)
            pipeline.stop()
