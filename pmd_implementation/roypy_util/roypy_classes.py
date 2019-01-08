import time

from roypy_util import roypy
from collections import deque
import queue
from roypy_util.sample_camera_info import print_camera_info
from roypy_util.roypy_sample_utils import CameraOpener, add_camera_opener_options
from roypy_util.roypy_platform_utils import PlatformHelper

class DepthListener(roypy.IDepthDataListener):
    def __init__(self, q):
        super(DepthListener, self).__init__()
        self.queue = q

    def onNewData(self, data):
        zvalues = []
        for i in range(data.getNumPoints()):
            zvalues.append(data.getGrayValue(i))
        zarray = np.asarray(zvalues)
        p = zarray.reshape (-1, data.width)
        p = cv2.convertScaleAbs(p)
        #p = np.reshape(zarray, (640, 480)).astype(np.uint8)
        self.queue.append(p)



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
