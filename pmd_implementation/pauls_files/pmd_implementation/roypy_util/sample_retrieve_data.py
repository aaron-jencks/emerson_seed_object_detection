#!/usr/bin/python3

# Copyright (C) 2017 Infineon Technologies & pmdtechnologies ag
#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY
# KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS FOR A
# PARTICULAR PURPOSE.

"""This sample shows how to shows how to capture image data.

It uses Python's numpy and matplotlib to process and display the data.
"""

import sys
import tensorflow as tf
import argparse
#import cv2
from random import *

import time
import queue
from sample_camera_info import print_camera_info
from roypy_sample_utils import CameraOpener, add_camera_opener_options
from roypy_platform_utils import PlatformHelper

from utils import label_map_util
from utils import visualization_utils_color as vis_util
from utils import vis_depth_util
from utils.model_util import TensorflowFaceDetector

import roypy
import numpy as np
import matplotlib.pyplot as plt


print('Setting up paths')
# Path to frozen detection graph. This is the actual model that is used for the object detection.
PATH_TO_CKPT = 'frozen_inference_graph.pb'

# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = 'seed_label_map.pbtxt'

NUM_CLASSES = 2

print('Loading labelmaps')
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)
tDetector = TensorflowFaceDetector(PATH_TO_CKPT)

class MyListener(roypy.IDepthDataListener):
    def __init__(self, q, q2):
        super(MyListener, self).__init__()
        self.queue = q
        self.queue2 = q2

    def onNewData(self, data):
        zvalues = []
        gvalues = []
        for i in range(data.getNumPoints()):
            zvalues.append(data.getZ(i))
            gvalues.append(data.getGrayValue(i))
        zarray = np.asarray(zvalues)
        garray = np.asarray(gvalues)
        p = zarray.reshape (-1, data.width)
        print(p)
        self.queue.put(p)
        p = garray.reshape (-1, data.width)
        self.queue2.put(p)

    def paint (self, data, data2):
        """Called in the main thread, with data containing one of the items that was added to the
        queue in onNewData.
        """
        # create a figure and show the raw data
        #cmap1 = Colormap
        plt.figure(1)
        plt.subplot(211)
        plt.imshow(data)
        plt.subplot(212)
        plt.imshow(data2, cmap="gray")

        plt.show(block = False)
        plt.draw()
        # this pause is needed to ensure the drawing for
        # some backends
        plt.pause(0.001)

def main ():

    

    platformhelper = PlatformHelper()
    parser = argparse.ArgumentParser (usage = __doc__)
    add_camera_opener_options (parser)
    parser.add_argument ("--seconds", type=int, default=15, help="duration to capture data")
    options = parser.parse_args()
    opener = CameraOpener (options)
    cam = opener.open_camera ()
    cam.setUseCase("MODE_5_45FPS_500")
    cam.setExposureTime(80)

    print_camera_info (cam)
    print("isConnected", cam.isConnected())
    print("getFrameRate", cam.getFrameRate())

    # we will use this queue to synchronize the callback with the main
    # thread, as drawing should happen in the main thread
    q = queue.Queue()
    q2 = queue.Queue()
    l = MyListener(q, q2)
    cam.registerDataListener(l)
    cam.startCapture()
    # create a loop that will run for a time (default 15 seconds)
    process_event_queue (q, q2, l, options.seconds)
    cam.stopCapture()

def process_event_queue (q, q2, painter, seconds):
    # create a loop that will run for the given amount of time
    t_end = time.time() + seconds
    while time.time() < t_end:
        try:
            # try to retrieve an item from the queue.
            # this will block until an item can be retrieved
            # or the timeout of 1 second is hit
            item = q.get(True, 1)
            item2 = q2.get(True, 1)
            (boxes, scores, classes, num_detections) = tDetector.run(item2)

            # Draws bounding boxes
            vis_util.visualize_boxes_and_labels_on_image_array(
                item2,
                np.squeeze(boxes),
                np.squeeze(classes).astype(np.int32),
                np.squeeze(scores),
                category_index,
                use_normalized_coordinates=True,
                line_thickness=4)

            # Draws the depth information
            vis_depth_util.apply_depth_to_boxes(item2, np.squeeze(boxes), np.squeeze(scores), depth_frame)
        except queue.Empty:
            # this will be thrown when the timeout is hit
            break
        else:
            painter.paint (item, item2)

if (__name__ == "__main__"):
    main()
