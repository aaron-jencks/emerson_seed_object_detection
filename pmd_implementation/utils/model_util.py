import tensorflow as tf
import numpy as np
import time
import cv2
import threading
from utils import visualization_utils_color as vis_util

class TensorflowDetectorThread(threading.Thread):
	"""This class can be used to parallelize the tensorflow processing part
	Images can be passed in via a queue, and then retrieved from a 
	different queue"""
	def __init__(self, path_to_model, queue_in, queue_out):
		threading.Thread.__init__(self)
		self.tDetector = TensorflowFaceDetector(path_to_model)
		self.queue_in = queue_in
		self.queue_out = queue_out
		self.isStopping = False

	def run(self):
		while not self.isStopping:
			if len(self.queue_in) > 0:
				(depth, gray) = self.queue_in.pop()
				if len(self.queue_in) > 0:
					self.queue_in.clear()
				(boxes, scores, classes, num_detections) = self.tDetector.run(gray)
				self.queue_out.append((boxes, scores, classes, num_detections))
			else:
				time.sleep(0.01)

	def stop(self):
		self.isStopping = True

class TensorflowFaceDetector(object):
    def __init__(self, path_to_model: str):
        """Tensorflow detector
        """

        self.detection_graph = tf.Graph()
        with self.detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(path_to_model, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')


        with self.detection_graph.as_default():
            config = tf.ConfigProto()
            config.gpu_options.allow_growth = True
            self.sess = tf.Session(graph=self.detection_graph, config=config)


    def run(self, image):
        """image: bgr image
        return (boxes, scores, classes, num_detections)
        """

        image_np = image #cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

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
