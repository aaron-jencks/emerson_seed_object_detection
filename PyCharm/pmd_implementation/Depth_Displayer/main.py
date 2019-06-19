from dependencies.display_util.string_display_util import *
from dependencies.display_util.array_display_util import *
import pyrealsense2 as rs
import numpy as np
import json
import time
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import pyqtgraph as pg

from PIL import Image

import Depth_Displayer.cam_conversion as cc

# from tqdm import tqdm


file = ""  # "/home/aaron/Documents/20190607_103806.bag"
cnf_file = "C:\\Users\\aaron.jencks\\Documents\\GitHub\\emerson_seed_object_detection\\realsense_cam_settings.json"
clumping = 1
depth_clumping = 10
historical_average_depth = 64

current_roi = 0
update_roi = True
horizontal_trim = 0
vertical_trim = 0
rois = [
    {'l': 294, 'u': 262, 'r': 391, 'b': 360},  # Marker 1
    {'l': 312, 'u': 222, 'r': 378, 'b': 281},  # Marker 2
    {'l': 321, 'u': 198, 'r': 373, 'b': 243},  # Marker 3
    {'l': 325, 'u': 184, 'r': 369, 'b': 218},  # Marker 4
    {'l': 329, 'u': 175, 'r': 366, 'b': 201},  # Marker 5
    {'l': 321, 'u': 167, 'r': 366, 'b': 194},  # Marker 6
    {'l': 334, 'u': 162, 'r': 362, 'b': 190},  # Marker 7
    {'l': 335, 'u': 162, 'r': 359, 'b': 186},  # Marker 8
    {'l': 339, 'u': 159, 'r': 361, 'b': 179},  # Marker 9
    {'l': 341, 'u': 154, 'r': 360, 'b': 173},  # Marker 10
    {'l': 0, 'u': 0, 'r': 640, 'b': 480}       # Give me all of it
]

is_stopping = False


DS5_product_ids = ["0AD1", "0AD2", "0AD3", "0AD4", "0AD5", "0AF6",
                   "0AFE", "0AFF", "0B00", "0B01", "0B03", "0B07","0B3A"]


def find_device_that_supports_advanced_mode():
    ctx = rs.context()
    devices = ctx.query_devices()
    for dev in devices:
        if dev.supports(rs.camera_info.product_id) and str(dev.get_info(rs.camera_info.product_id)) in DS5_product_ids:
            if dev.supports(rs.camera_info.name):
                print("Found device that supports advanced mode:", dev.get_info(rs.camera_info.name))
                return dev
    raise Exception("No device that supports advanced mode was found")


def round_data(data):
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            data[i, j] = round(data[i, j], 4)  # '{:#05.4g}'.format(data[i, j])


def number_of_different_values(data) -> int:
    values = []
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            if int(data[i, j]) not in values:
                values.append(int(data[i, j]))

    return len(values)


def btn_callback(event):
    global current_roi, update_roi
    if current_roi == len(rois) - 1:
        current_roi = 0
    else:
        current_roi += 1

    update_roi = True

    print_notification("Switching to location {}".format(current_roi + 1))


def stop_callback(event):
    global is_stopping
    is_stopping = True
    print_notification("Stopping")


if __name__ == "__main__":
    file = ""  # input("Input file path: ") if file == "" else file

    ctx = rs.context()

    dev = find_device_that_supports_advanced_mode()
    advnc_mode = rs.rs400_advanced_mode(dev)

    advnc_mode.load_json(
        str(json.load(open(cnf_file))).replace("'", '\"'))

    pipeline = rs.pipeline(ctx)

    config = rs.config()
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 90)

    cap = pipeline.start(config)

    scale = cap.get_device().first_depth_sensor().get_depth_scale()

    print("Depth Scale is {}".format(scale))

    fig, ax = plt.subplots()
    ax.axis('off')

    plot = fig.add_axes([0.1, 0.5, 0.7, 0.4])
    dist = fig.add_axes([0.1, 0.1, 0.7, 0.4])

    btn_nxt = fig.add_axes([0.85, 0.15, 0.1, 0.05])
    btn_stp = fig.add_axes([0.85, 0.21, 0.1, 0.05])
    # btn.axis('off')
    btn_next = Button(btn_nxt, "Next")
    btn_next.on_clicked(btn_callback)
    btn_stop = Button(btn_stp, "Quit")
    btn_stop.on_clicked(stop_callback)

    # l, u, r, b = tuple([int(i) for i in
    #                     input("Enter roi in the order of left, up, right, bottom, separated by spaces: ").split()])

    try:
        first = True
        roi = []
        history = np.zeros(shape=(1, 1, 1), dtype=float)
        
        print_notification("Switching to location {}".format(current_roi + 1))
        
        while not is_stopping:
            roi_dict = rois[current_roi]
            l = roi_dict['l'] + horizontal_trim
            u = roi_dict['u'] + vertical_trim
            r = roi_dict['r'] + horizontal_trim
            b = roi_dict['b'] + vertical_trim

            frames = pipeline.wait_for_frames()
            depth_frame = frames.get_depth_frame()
            # depth_array = np.multiply(np.asanyarray(depth_frame.get_data()), 1)  # scale)

            if update_roi:
                roi = np.zeros(shape=(b - u, r - l), dtype=np.float32)
                update_roi = False

            history, roi, norm = cc.convert_realsense(frames, roi, u, b, l, r, clumping, depth_clumping,
                                                      1 if first else 0, history, historical_average_depth)

            if first:
                first = False

            plot.clear()
            plot.imshow(roi)
            plot.axis('off')

            dist.clear()
            dist.hist(np.multiply(norm, scale), range=(-1, 1), histtype='step')
            # dist.hist(norm[:, 1])  # , range=(-5, 5))  # [:, 1])

            plt.draw()
            plt.pause(0.001)

    finally:
        print_warning("Something went wrong")
