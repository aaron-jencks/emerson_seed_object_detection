import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from math import floor, ceil
from pylab import rcParams
import cv2
import pyrealsense2 as rs

sns.set(style='ticks', palette='Spectral', font_scale=1.5)
material_palette = ["#4CAF50", "#2196F3", "#9E9E9E", "#FF9800", "#607D8B", "#9C27B0"]

sns.set_palette(material_palette)
rcParams['figure.figsize'] = 16, 8
plt.xkcd();

random_state = 42
np.random.seed(random_state)
tf.set_random_seed(random_state)

column_vector = ["xmin", "ymin", "xmax", "ymax", "proposed_depth", "actual_depth"]

collect_data = True
load_data = False

if collect_data:
	pipeline = rs.pipeline()
	print('Creating realsense pipeline')
	# Realsense pipeline
	pipeline = rs.pipeline()
	config = rs.config()
	config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
	config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
	profile = pipeline.start(config)
	depth_scale = profile.get_device().first_depth_sensor().get_depth_scale()

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
    else:
        print('json does not exist, using default camera settings')
