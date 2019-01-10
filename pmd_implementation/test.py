print('Importing libraries')
import sys
import time
import numpy as np
import tensorflow as tf
import cv2
from random import *
import argparse

from utils import label_map_util
from utils import visualization_utils_color as vis_util
from utils import vis_depth_util
from utils.model_util import TensorflowDetectorThread

from roypy_util import roypy
from collections import deque
from roypy_util.sample_camera_info import print_camera_info
from roypy_util.roypy_sample_utils import CameraOpener, add_camera_opener_options
from roypy_util.roypy_platform_utils import PlatformHelper
from roypy_util.roypy_classes import *

# Parser info
parser = argparse.ArgumentParser(description="Used to take live video using the roypy camera.", usage=__doc__)
add_camera_opener_options (parser)
options = parser.parse_args()

# pmd software utillity stuff
#platformhelper = PlatformHelper()
opener = CameraOpener (options)
cap = opener.open_camera ()

# we will use this queue to synchronize the callback with the main
# thread, as drawing should happen in the main thread
q = deque()
q_depth = deque()
l_depth = DepthListener(q, q_depth)
cap.registerDataListener(l_depth)
cap.setUseCase("MODE_5_45FPS_500")
cap.setExposureTime(300)
print(cap.getCurrentUseCase())
cap.startCapture()

print_camera_info (cap)
print("isConnected", cap.isConnected())
print("getFrameRate", cap.getFrameRate())

print('Setting up paths')
# Path to frozen detection graph. This is the actual model that is used for the object detection.
PATH_TO_CKPT = './models/current/frozen_graph/frozen_inference_graph.pb'

# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = './protos/seed_label_map.pbtxt'

NUM_CLASSES = 2

print('Loading labelmaps')
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

thread_in = deque()
thread_out = deque()
tensorflow_thread = TensorflowDetectorThread(PATH_TO_CKPT, thread_in, thread_out)
tensorflow_thread.start()
tens_ready = True
tens_result = None
tens_start_time = time.time()

while True:
	start_time = time.time()
	if len(q) > 0 and len(q_depth) > 0:
		frame = q.pop()
		depth_image = q_depth.pop()
		#time.sleep(0.05)
		if len(q) > 20 or len(q_depth) > 20:
			print('Falling behind, skipping {} frames'.format(len(q)))
			q.clear()
			q_depth.clear()
		    
		if frame is not None and depth_image is not None:
			image = np.stack((frame,)*3, axis=-1)
			# Apparently the grayscale is returning values of more than 2000
			image = ((image - image.min()) / image.max() * 255).astype(np.uint8)
			#print(image.size)
			if depth_image.max() is not 0:
				# Converts to a floating point scale from 0-1
				depth_image = ((depth_image - depth_image.min()) / depth_image.max() * 255).astype(np.uint8)

			if tens_ready:
				thread_in.append((depth_image, image))
				tens_start_time = time.time()
				tens_ready = False

			if len(thread_out) > 0:
				print('Updating bounding boxes, this iteration took {}'.format(time.time() - tens_start_time))
				#print(image.shape)
				tens_result = thread_out.pop()
				tens_ready = True

			if tens_result:
				# Allows for drawing of old data to make it not blink up and disappear
				(boxes, scores, classes, num_detections) = tens_result
				vis_util.visualize_boxes_and_labels_on_image_array(
					image, depth_image,
					np.squeeze(boxes),
					np.squeeze(classes).astype(np.int32),
					np.squeeze(scores),
					category_index,
					use_normalized_coordinates=True,
					line_thickness=4)

			l_depth.paint(depth_image, image)
			#print(image.max())
			k = cv2.waitKey(1) & 0xff
			if k == ord('q') or k == 27:
				break
	#print('This frame took {} seconds to compute'.format(time.time() - start_time))

tensorflow_thread.stop()
cap.stopCapture()
