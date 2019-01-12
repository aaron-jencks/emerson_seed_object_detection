import numpy as np
import cv2
import argparse
from roypy_util import roypy
import time
import queue
from collections import deque
from roypy_util.sample_camera_info import print_camera_info
from roypy_util.roypy_sample_utils import CameraOpener, add_camera_opener_options
from roypy_util.roypy_platform_utils import PlatformHelper
#import matplotlib.pyplot as plt
from roypy_util.roypy_classes import *

platformhelper = PlatformHelper()
parser = argparse.ArgumentParser (description="Creates a video from into the given output directory using the given device ID, use space to toggle recording, and 'k' to take a snapshot, hit esc or 'q' to quit", usage = __doc__)
add_camera_opener_options (parser)
parser.add_argument('-o', '--output', help='The output path that the video will be created at, defaults to ./output.avi.', type=str, default='./output.avi')
parser.add_argument('-e', '--exposure', help='Exposure time to use', type=int, default=80)
parser.add_argument('-m', '--cam_mode', help='Camera mode to user', type=str, default="MODE_5_45FPS_500")
#parser.add_argument ("--seconds", type=int, default=15, help="duration to capture data")
options = parser.parse_args()

opener = CameraOpener (options)
cap = opener.open_camera ()
cap_temp = cv2.VideoCapture(0)

print_camera_info (cap)
print("isConnected", cap.isConnected())
print("getFrameRate", cap.getFrameRate())

# either *'XVID' or ('X', 'V', 'I', 'D') will work the same way
#fourcc = cv2.VideoWriter_fourcc(*'XVID')
fourcc = cv2.VideoWriter_fourcc(*'XVID')

# output path, video config, fps, screen resolution, isColor
out = cv2.VideoWriter(options.output, fourcc, int(cap.getFrameRate()), (224, 171), True) #int(cap.get(3)), int(cap.get(4))))

# Variables for video operation
isRecording = False
snapshot = False

# we will use this queue to synchronize the callback with the main
# thread, as drawing should happen in the main thread
q = deque()
l = ImageListener(q)
cap.registerDataListener(l)
cap.setUseCase(options.cam_mode)
#cap.setExposureMode(MANUAL)
cap.setExposureTime(options.exposure)
print(cap.getCurrentUseCase())
cap.startCapture()

while cap.isConnected():
    frame = q.pop() if len(q) > 0 else None
    if frame is not None:
            frame = np.stack((frame,)*3, axis=-1)
            if isRecording or snapshot:
                    #print(frame.shape)
                    print(frame.min())
                    print(frame.max())
                    #print(frame)
                    #toolong = list(cap_temp.read())[1]
                    #print(toolong.shape)
                    #print(toolong.min())
                    #print(toolong.max())
                    #print(toolong)
                    
                    out.write(frame)
                    if snapshot:
                            snapshot = False

            cv2.imshow('frame', frame)

            k = cv2.waitKey(1) & 0xFF
            if k == ord('q') or k == 27:
                    break
            elif k == 32:
                    isRecording = not isRecording
                    print('Recording Started' if isRecording else 'Recording Stopped')
            elif k == 107:
                    snapshot = True
                    print('Collecting snapshot' if not isRecording else "Can't take a snapshot while recording silly, I'm already taking in frames")
            elif k == 101:
                    new_exp = int(input('Enter a integer value for exposure in uSec:'))
                    cap.setExposureTime(new_exp)
            elif k == 109:
                    cap.setUseCase(input('Enter a new camera mode to use:'))
cap.stopCapture()
cap_temp.release()
out.release()
cv2.destroyAllWindows()




