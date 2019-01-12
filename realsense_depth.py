# -*- coding: utf-8 -*-
# pylint: disable=C0103
# pylint: disable=E1101

print('Importing libraries')
import sys
import time
import numpy as np
import tensorflow as tf
import cv2
import pyrealsense2 as rs
from random import *
from collections import deque

from utils import label_map_util
from utils import visualization_utils_color_depth as vis_util
from utils.model_util import TensorflowDetectorThread

print('Setting up paths')
# Path to frozen detection graph. This is the actual model that is used for the object detection.
PATH_TO_CKPT = './model/frozen_inference_graph_face.pb'

# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = './protos/face_label_map.pbtxt'

NUM_CLASSES = 2

print('Loading labelmaps')
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

# Used to find advanced_mode devices
DS5_product_ids = ["0AD1", "0AD2", "0AD3", "0AD4", "0AD5", "0AF6", "0AFE", "0AFF", "0B00", "0B01", "0B03", "0B07"]

def find_device_that_supports_advanced_mode() :
    ctx = rs.context()
    ds5_dev = rs.device()
    devices = ctx.query_devices();
    for dev in devices:
        if dev.supports(rs.camera_info.product_id) and str(dev.get_info(rs.camera_info.product_id)) in DS5_product_ids:
            if dev.supports(rs.camera_info.name):
                print("Found device that supports advanced mode:", dev.get_info(rs.camera_info.name))
        return dev
    return None


if __name__ == "__main__":

    thread_in = deque()
    thread_out = deque()
    tensorflow_thread = TensorflowDetectorThread(PATH_TO_CKPT, thread_in, thread_out)
    tensorflow_thread.start()
    tens_ready = True
    tens_result = None
    tens_start_time = time.time()

    import sys
    #tDetector = TensoflowFaceDector(PATH_TO_CKPT)

    print('Creating realsense pipeline')
    # Realsense pipeline
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
    config.enable_stream(rs.stream.infrared, 1280, 720, rs.format.y8, 30)
    config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)
    profile = pipeline.start(config)
    depth_scale = profile.get_device().first_depth_sensor().get_depth_scale()
    print('Depth Scale: ' + str(depth_scale) + ' meters/unit')

    print('Searching for json file')
    from pathlib import Path
    if Path('./realsense_cam_settings.json').exists():
        with open('./realsense_cam_settings.json') as f:
            json_string = f.read().replace("'", '\"')
            dev = find_device_that_supports_advanced_mode()
            if dev is not None:
                advnc_mode = rs.rs400_advanced_mode(dev)
            else:
                print('Found no usable devices for advanced mode')
                pass
            while dev is not None and not advnc_mode.is_enabled():
                advnc_mode.toggle_advanced_mode(True)
                time.sleep(5)
                dev = find_device_that_supports_advanced_mode()
                if dev is not None:
                    advnc_mode = rs.rs400_advanced_mode(dev)
                else:
                    print('Found no usable devices for advanced mode')
                    pass
                print('Trying to turn on advanced mode')
            print('Loading config file')
            if advnc_mode is not None:
                advnc_mode.load_json(json_string)
                # Get each control's current value
                print("Depth Control: \n", advnc_mode.get_depth_control())
                print("RSM: \n", advnc_mode.get_rsm())
                print("RAU Support Vector Control: \n", advnc_mode.get_rau_support_vector_control())
                print("Color Control: \n", advnc_mode.get_color_control())
                print("RAU Thresholds Control: \n", advnc_mode.get_rau_thresholds_control())
                print("SLO Color Thresholds Control: \n", advnc_mode.get_slo_color_thresholds_control())
                print("SLO Penalty Control: \n", advnc_mode.get_slo_penalty_control())
                print("HDAD: \n", advnc_mode.get_hdad())
                print("Color Correction: \n", advnc_mode.get_color_correction())
                print("Depth Table: \n", advnc_mode.get_depth_table())
                print("Auto Exposure Control: \n", advnc_mode.get_ae_control())
                print("Census: \n", advnc_mode.get_census())
                #advnc_mode.set_rsm(rs.STRsm.)
                #advnc_mode.load_json(json_string)
    else:
        print('json does not exist, using default camera settings')

    print('Starting computation')
    depth_scale = profile.get_device().first_depth_sensor().get_depth_scale()
    print('Depth Scale: {}'.format(depth_scale))
    windowNotSet = True
    try:
        while True:
            # Realsense pipeline image collection and conversion
            frame = pipeline.wait_for_frames()
            depth_frame = frame.get_depth_frame()
            ir_frame = frame.get_infrared_frame()
            color_frame = frame.get_color_frame()

            # Reformats the data into a usable form
            image = np.asanyarray(color_frame.get_data())
            depth_image_orig = np.asanyarray(depth_frame.get_data())
            ir_image = np.asanyarray(ir_frame.get_data())
            # Converts the depth information into meters
            depth_image = (depth_image_orig * depth_scale).astype(float) #cv2.convertScaleAbs(depth_image_orig, alpha=depth_scale)
            # Converts single channel grayscale to 3 channel rgb, remove for color
            ir_image = np.stack((ir_image,)*3, axis=-1)
            #image = image.reshape((720, 1280, 3))

            [h, w] = image.shape[:2]
            #print (h, w)
            ir_image = cv2.flip(ir_image, 1)
            image = cv2.flip(image, 1)

            if tens_ready:
                # It doesn't actually use both images right now, but it might in the future
                # Use original so that the depth values are correct
                image_np = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                thread_in.append((None, ir_image))
                tens_start_time = time.time()
                tens_ready = False

            if len(thread_out) > 0:
                print('Updating bounding boxes, this iteration took {}'.format(time.time() - tens_start_time))
                #print(image.shape)
                tens_result = thread_out.pop()
                tens_ready = True

            if tens_result:
                # Allows for drawing of old data to make it not blink up and disappear
                # Use original depth image for accurate depth information depth_image_orig,
                # Not depth_image
                (boxes, scores, classes, num_detections) = tens_result

                # Draws bounding boxes
                vis_util.visualize_boxes_and_labels_on_image_array(
                    ir_image, depth_image, profile,
                    np.squeeze(boxes),
                    np.squeeze(classes).astype(np.int32),
                    np.squeeze(scores),
                    category_index,
                    use_normalized_coordinates=True,
                    line_thickness=4)

            if windowNotSet is True:
                cv2.namedWindow("tensorflow based (%d, %d)" % (w, h), cv2.WINDOW_NORMAL)
                windowNotSet = False

            colorizer = rs.colorizer()
            depth_image_scaled = colorizer.colorize(depth_frame) #((depth_image / depth_image.max()) * 255).astype(np.uint8)
            depth_colormap = np.asanyarray(depth_image_scaled.get_data()) #cv2.applyColorMap(depth_image_scaled, cv2.COLORMAP_JET)
            image = np.hstack((image, ir_image, depth_colormap))

            cv2.imshow("tensorflow based (%d, %d)" % (w, h), image)
            k = cv2.waitKey(1) & 0xff
            if k == ord('q') or k == 27:
                break
    except Exception as e:
	    print("Runtime exception: {}".format(e))

    tensorflow_thread.stop()
    pipeline.stop()
    cv2.destroyAllWindows()
