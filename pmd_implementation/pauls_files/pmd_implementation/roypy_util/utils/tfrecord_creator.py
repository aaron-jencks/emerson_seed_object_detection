import tensorflow as tf
import numpy as np
import argparse
from random import shuffle
import os, fnmatch, pathlib, shutil

import pandas as pd
import xml.etree.ElementTree as ET
import io, contextlib2

from PIL import Image
from object_detection.utils import dataset_util
from object_detection.dataset_tools import tf_record_creation_util
from object_detection.utils import label_map_util
from collections import namedtuple, OrderedDict
from labelmap_creation_util import LabelmapManager

# Documentations
parser = argparse.ArgumentParser("Creates tfrecords from the given parameters")
parser.add_argument("--annotation_xmls", "-a", help="Directory to the xml annotations for the images, default is ./annotations", type=str, default="./annotations")
parser.add_argument("--labelmap_path", "-l", help="Specifies the labelmap to use when creating the examples, if none is specified, it will create one, likewise, it will also update the current one if a label occurs that does not exist in the current map", type=str, default=None)
parser.add_argument("--image_dir", "-i", help="Directory that the images are stored in, default is ./images", type=str, default="./images")
parser.add_argument("--split", "-s", help="Automatically splits the tfrecord into a train.record, and test.record", action="store_true", default=False)
parser.add_argument("--percent_test", "-p", help="The percent of samples that should be used as testing samples, default is 10%", type=int, default=10)
parser.add_argument("--shards", help="The number of shards to split the record files into, default is 10", type=int, default=10)
parser.add_argument("output_dir", help="The directory to put the output file(s) default is .", type=str, default=".")
args = parser.parse_args()

map_manager = LabelmapManager(args.labelmap_path if args.labelmap_path else os.path.join(args.output_dir, "labelmap.pbtxt"))

def convert_xml_to_jpg(path: str):
	"""Converts a list of file names in the given path from .xml to .jpg"""
	# Converts the .jpg to .xml and adds the ./annotations/xmls prefix
	return os.path.join(args.image_dir, path[:-4] + ".jpg")
	
def remove_non_existant_files(file_list):
	"""Iterates through the list and removes and files that don't exist"""
	# Checks to make sure that the jpg files exist, and if they don't then skips them
	
	# Converts the xml files to jpg equivalent
	jpg_list = list(map(lambda x: convert_xml_to_jpg(x), file_list))
	
	# Checks the existance
	for i in range(len(jpg_list) - 1, -1, -1):
		if not os.path.isfile(jpg_list[i]):
			print("File " + jpg_list[i] + " does not exist, removing...")
			del(file_list[i])
	
def xml_to_csv(xml_file_list):
	"""Converts given xml files into a csv panda dataframe"""
	
	# Parses the xml files
	xml_list = []
	for xml_file in xml_file_list:
		tree = ET.parse(xml_file)
		root = tree.getroot()
		for member in root.findall('object'):
			value = (root.find('filename').text,
				int(root.find('size')[0].text),
				int(root.find('size')[1].text),
				member[0].text,
				int(member[4][0].text),
				int(member[4][1].text),
				int(member[4][2].text),
				int(member[4][3].text)
				)
			xml_list.append(value)
			
	# Sets up the pandas dataframe
	column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
	xml_df = pd.DataFrame(xml_list, columns=column_name)
	return xml_df

def class_text_to_int(row_label):
    if map_manager.labelmap_dict:
        if row_label in map_manager.labelmap_dict:
            return map_manager.labelmap_dict[row_label]
        else:
            print('Updating label map to contain ' + row_label)
            return map_manager.add_label(row_label)
    else:
        None

def split(df, group):
    data = namedtuple('data', ['filename', 'object'])
    gb = df.groupby(group)
    return [data(filename, gb.get_group(x)) for filename, x in zip(gb.groups.keys(), gb.groups)]

	
def create_tf_example(group, path):
    with tf.gfile.GFile(os.path.join(path, '{}'.format(group.filename)), 'rb') as fid:
        encoded_jpg = fid.read()
    encoded_jpg_io = io.BytesIO(encoded_jpg)
    image = Image.open(encoded_jpg_io)
    width, height = image.size

    filename = group.filename.encode('utf8')
    image_format = b'jpg'
    xmins = []
    xmaxs = []
    ymins = []
    ymaxs = []
    classes_text = []
    classes = []

    for index, row in group.object.iterrows():
        xmins.append(row['xmin'] / width)
        xmaxs.append(row['xmax'] / width)
        ymins.append(row['ymin'] / height)
        ymaxs.append(row['ymax'] / height)
        classes_text.append(row['class'].encode('utf8'))
        classes.append(class_text_to_int(row['class']))

    tf_example = tf.train.Example(features=tf.train.Features(feature={
        'image/height': dataset_util.int64_feature(height),
        'image/width': dataset_util.int64_feature(width),
        'image/filename': dataset_util.bytes_feature(filename),
        'image/source_id': dataset_util.bytes_feature(filename),
        'image/encoded': dataset_util.bytes_feature(encoded_jpg),
        'image/format': dataset_util.bytes_feature(image_format),
        'image/object/bbox/xmin': dataset_util.float_list_feature(xmins),
        'image/object/bbox/xmax': dataset_util.float_list_feature(xmaxs),
        'image/object/bbox/ymin': dataset_util.float_list_feature(ymins),
        'image/object/bbox/ymax': dataset_util.float_list_feature(ymaxs),
        'image/object/class/text': dataset_util.bytes_list_feature(classes_text),
        'image/object/class/label': dataset_util.int64_list_feature(classes),
    }))
    return tf_example
	
def gen_tfrecord(panda_df, output_path, num_shards = 10):
	"""Creates a TFRecord of the current dataframe into the output file"""
	with contextlib2.ExitStack() as tf_record_close_stack:
		writer = tf_record_creation_util.open_sharded_output_tfrecords(
			tf_record_close_stack, output_path, num_shards)
		grouped = split(panda_df, 'filename')
		for idx, group in enumerate(grouped):
			if idx % 100 == 0:
				print("On image " + str(idx) + " of " + str(len(grouped)))
			tf_example = create_tf_example(group, args.image_dir)
			shard_idx = idx % num_shards
			writer[shard_idx].write(tf_example.SerializeToString())
		
		print("Successfully creates the TFRecords: {}".format(output_path))


def read_train_val():
	"""Locates the given xml files, removes non-existant files,
	then shuffle the list, splits it into two categories (training, testing)
	but only if specified by args.split, and returns the two lists"""
	
	# Maps the directory for image files and reads in all of the lines and then shuffles them
	files = list(fnmatch.filter(os.listdir(args.annotation_xmls), "*.xml"))
	
	# Converts to the corresponding jpg files, and then removes the non-existant ones
	remove_non_existant_files(files)
	
	# Shuffles the list
	shuffle(files)
	files = list(map(lambda x: os.path.join(args.annotation_xmls, x), files))
	
	for name in files:
		print(name)
	
	# Splits the files into two arrays of train values, and test values if specified to
	# Otherwise all of the values will be put into the train_values
	split_loc = int(len(files) * (1 - (args.percent_test / 100))) if args.split else len(files)
	train_values = files[:split_loc]
	test_values = files[split_loc:]
	return (train_values, test_values)
    
if __name__ == '__main__':
	"""Separates the image files in the image_dir directory into two categories
	then creates tfrecords in the given output directory"""

	# Reads in the trainval.txt file and shuffles its contents
	# Then splits it into training and testing values
	(train, test) = read_train_val()
	
	print("Converting to pandas df")
	train_df = xml_to_csv(train)
	test_df = xml_to_csv(test)
	
	# Creates the tfrecord
	gen_tfrecord(train_df, os.path.join(args.output_dir, "train.record"), args.shards)
	
	# Creates the test.record if specified
	if args.split:
	    gen_tfrecord(test_df, os.path.join(args.output_dir, "test.record"), args.shards)
	
	print("Generated TFRecords")
