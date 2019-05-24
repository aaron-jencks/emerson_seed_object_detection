import pyximport; pyximport.install()
import video_util.cy_collection_util as cu
import roypy
import time
import numpy as np
import cv2
import queue
from roypy_sample_utils import CameraOpener
from .roypy_sample_utils_custom import CameraOpenerExternTrig
from data_structures.lists import LinkedList


def get_camera(options, filename=None):
    """Finds the requested pmd camera and opens it for viewing"""

    manager = roypy.CameraManager()

    cap = manager.createCamera() if filename is None else manager.createCamera(filename)

    cap.initialize()

    # if options.external_trig:
    #     opener = CameraOpenerExternTrig(options)
    # else:
    #     opener = CameraOpener(options)

    return cap


class ImageListener(roypy.IDepthDataListener):
    def __init__(self, q):
        super(ImageListener, self).__init__()
        self.queue = q

    def onNewData(self, data):
        p = cu.convert_gray(data)
        self.queue.append(p)


class DepthListener(roypy.IDepthDataListener):
    def __init__(self, q, q_depth):
        super(DepthListener, self).__init__()
        self.queue = q_depth
        self.gqueue = q

    def onNewData(self, data):
        zarray, garray = cu.convert_raw(data)
        self.queue.append(zarray)
        self.gqueue.append(garray)

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
