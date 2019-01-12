import time
import numpy as np
import cv2

import roypy
from collections import deque
import queue
from sample_camera_info import print_camera_info
from roypy_sample_utils import CameraOpener, add_camera_opener_options
from roypy_platform_utils import PlatformHelper

"""
# Fixes Segmentation fault upon import of matplotlib using anaconda
# https://github.com/matplotlib/matplotlib/issues/9294/
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
"""

class ImageListener(roypy.IDepthDataListener):
    def __init__(self, q):
        super(ImageListener, self).__init__()
        self.queue = q

    def onNewData(self, data):
        zvalues = []
        for i in range(data.getNumPoints()):
            try:
                zvalues.append(data.getGrayValue(i))
            except Exception as e:
                print(e)
        try:
            zarray = np.asarray(zvalues)
            p = zarray.reshape (-1, data.width)
            p = cv2.convertScaleAbs(p)
        except Exception as e:
            print(e)
        #p = np.reshape(zarray, (640, 480)).astype(np.uint8)
        self.queue.append(p)

class DepthListener(roypy.IDepthDataListener):
    def __init__(self, q, q_depth):
        super(DepthListener, self).__init__()
        self.queue = q_depth
        self.gqueue = q

    def onNewData(self, data):
        zvalues = []
        gvalues = []
        for i in range(data.getNumPoints()):
            zvalues.append(data.getZ(i))
            gvalues.append(data.getGrayValue(i))
        zarray = np.asarray(zvalues)
        garray = np.asarray(gvalues)
        p = zarray.reshape (-1, data.width)
        self.queue.append(p)
        p = garray.reshape (-1, data.width)
        self.gqueue.append(p)

    def paint (self, data, data2, window_name='frame'):
        """Called in the main thread, with data containing one of the items that was added to the
        queue in onNewData.
        """

        new_data = cv2.applyColorMap(data, cv2.COLORMAP_JET)
        images = np.hstack((new_data, data2))
        cv2.imshow(window_name, images)

def process_event_queue (q, painter, seconds):
    # create a loop that will run for the given amount of time
    t_end = time.time() + seconds
    while time.time() < t_end or seconds < 0:
        try:
            # try to retrieve an item from the queue.
            # this will block until an item can be retrieved
            # or the timeout of 1 second is hit
            item = q.get(True, 1)
        except queue.Empty:
            # this will be thrown when the timeout is hit
            break
        else:
            painter.paint (item)
