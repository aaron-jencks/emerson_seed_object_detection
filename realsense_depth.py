#!/usr/bin/python
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

from utils import label_map_util
from utils import visualization_utils_color as vis_util
from utils import vis_depth_util

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

class TensoflowFaceDector(object):
    def __init__(self, PATH_TO_CKPT):
        """Tensorflow detector
        """

        self.detection_graph = tf.Graph()
        with self.detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')


        with self.detection_graph.as_default():
            config = tf.ConfigProto()
            config.gpu_options.allow_growth = True
            self.sess = tf.Session(graph=self.detection_graph, config=config)
            self.windowNotSet = True


    def run(self, image):
        """image: bgr image
        return (boxes, scores, classes, num_detections)
        """

        image_np = image # cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # the array based representation of the image will be used later in order to prepare the
        # result image with boxes and labels on it.
        # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
        image_np_expanded = np.expand_dims(image_np, axis=0)
        image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')
        # Each box represents a part of the image where a particular object was detected.
        boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')
        # Each score represent how level of confidence for each of the objects.
        # Score is shown on the result image, together with the class label.
        scores = self.detection_graph.get_tensor_by_name('detection_scores:0')
        classes = self.detection_graph.get_tensor_by_name('detection_classes:0')
        num_detections = self.detection_graph.get_tensor_by_name('num_detections:0')
        # Actual detection.
        #start_time = time.time()
        (boxes, scores, classes, num_detections) = self.sess.run(
            [boxes, scores, classes, num_detections],
            feed_dict={image_tensor: image_np_expanded})
        #elapsed_time = time.time() - start_time
        #print('inference time cost: {}'.format(elapsed_time))

        return (boxes, scores, classes, num_detections)

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
    import sys
    tDetector = TensoflowFaceDector(PATH_TO_CKPT)

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
    windowNotSet = True
    while True:
        # Realsense pipeline image collection and conversion
        frame = pipeline.wait_for_frames()
        depth_frame = frame.get_depth_frame()
        color_frame = frame.get_infrared_frame()

        # Reformats the data into a usable form
        image = np.asanyarray(color_frame.get_data())
        # Converts single channel grayscale to 3 channel rgb, remove for color
        image = np.stack((image,)*3, axis=-1)
        # image = image.reshape((480, 640, 3))

        [h, w] = image.shape[:2]
        #print (h, w)
        # image = cv2.flip(image, 1)

        (boxes, scores, classes, num_detections) = tDetector.run(image)

        # Draws bounding boxes
        vis_util.visualize_boxes_and_labels_on_image_array(
            image,
            np.squeeze(boxes),
            np.squeeze(classes).astype(np.int32),
            np.squeeze(scores),
            category_index,
            use_normalized_coordinates=True,
            line_thickness=4)

        # Draws the depth information
        vis_depth_util.apply_depth_to_boxes(image, np.squeeze(boxes), np.squeeze(scores), profile, depth_frame)

        if windowNotSet is True:
            cv2.namedWindow("tensorflow based (%d, %d)" % (w, h), cv2.WINDOW_NORMAL)
            windowNotSet = False

        # This is the depth scale stuff, it can also be found in
        # apply_depth_to_boxes
        depth_image = np.asanyarray(depth_frame.get_data())
        sel_y = randint(0, depth_image.shape[0] - 1)
        sel_x = randint(0, depth_image.shape[1] - 1)
        #a_bef = depth_image[sel_y, sel_x]
        depth_image_scaled = cv2.convertScaleAbs(depth_image, alpha=0.03) #depth_scale)
        #a_aft = depth_image_scaled[sel_y, sel_x]
        #m_aft = (a_bef * depth_scale).astype(np.uint8)
        #print('Before: ' + str(a_bef) + ' After: auto: ' + str(a_aft) + ' manual: ' + str(m_aft))
        #depth_image_scaled = ((depth_image_scaled / depth_image_scaled.max()) * 255).astype(np.uint8)
        depth_colormap = cv2.applyColorMap(depth_image_scaled, cv2.COLORMAP_JET)
        image = np.hstack((image, depth_colormap))

        cv2.imshow("tensorflow based (%d, %d)" % (w, h), image)
        k = cv2.waitKey(1) & 0xff
        if k == ord('q') or k == 27:
            break

    pipeline.stop()
