import time
import numpy as np
import cv2

import roypy
from collections import deque
import queue
from sample_camera_info import print_camera_info
from roypy_sample_utils import CameraOpener, add_camera_opener_options
from roypy_platform_utils import PlatformHelper

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
        #print(points)
        zarray = np.asarray(zvalues)
        garray = np.asanyarray(gvalues)
        #print(zarray)
        p = zarray.reshape (-1, data.width)
        print(p)
        #p = cv2.normalize(p, None, 255, 0, cv2.NORM_MINMAX, cv2.CV_8UC1)
        p = p.astype(np.uint8)
        #print(p)
        #p = cv2.convertScaleAbs(p)
        #print(p)
        #p = np.reshape(zarray, (640, 480)).astype(np.uint8)
        
        self.queue.append(p)
        pg = garray.reshape (-1, data.width)
        pg = cv2.convertScaleAbs(pg)
        #p = np.reshape(zarray, (640, 480)).astype(np.uint8)
        self.gqueue.append(pg)

def process_event_queue (q, painter, seconds):
    # create a loop that will run for the given amount of time
    t_end = time.time() + seconds
    while time.time() < t_end:
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
