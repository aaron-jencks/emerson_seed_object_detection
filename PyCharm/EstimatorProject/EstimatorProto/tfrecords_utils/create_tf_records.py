import pandas as pd
import xml.etree.ElementTree as ET
import os
import fnmatch
import io
import contextlib2
import tensorflow as tf

from PIL import Image
from object_detection.dataset_tools import tf_record_creation_util
from collections import namedtuple

from tqdm import tqdm


def convert_jpg_to_xml(root_path: str, path: str):
    """Converts a list of file names in the given path from .jpg to .xml"""

    # Finds all jpg files
    files = fnmatch.filter(os.listdir(path), "*.jpg")

    # Converts the .jpg to .xml and adds the ./annotations/xmls prefix
    xmls = map(lambda x: os.path.join(root_path, "annotations/xmls/" + x[:-4] + ".xml"), files)

    return list(xmls)


def remove_non_existant_files(file_list):
    """Iterates through the list and removes and files that don't exist"""

    # Checks to make sure that the xml files exist, and if they don't then skips them
    print("Checking for missing files in dataset")
    for i in tqdm(range(len(file_list) - 1, -1, -1)):
        if not os.path.isfile(file_list[i]):
            # print("File " + file_list[i] + " does not exist, removing...")
            del(file_list[i])


def find_xml_files(root_path: str):
    """Locates all of the image files in the two ./images/train/ and ./images/test/
    directories and finds the corresponding xml files in the ./annotations/xmls/ directory"""

    # Finds the xml files
    train_files = convert_jpg_to_xml(root_path, os.path.join(root_path, "images/train/"))
    test_files = convert_jpg_to_xml(root_path, os.path.join(root_path, "images/test/"))

    # Checks to make sure that the xml files exist, and if they don't then skips them
    # Train files
    remove_non_existant_files(train_files)
    # Test files
    remove_non_existant_files(test_files)

    print("Training files: {}".format(len(train_files)))
    print("Testing files: {}".format(len(test_files)))

    # Returns the located xml files
    return train_files, test_files


def xml_to_csv(xml_file_list):
    """Converts given xml files into a csv panda dataframe"""

    # Parses the xml files
    print("Converting xml to dataframe")
    xml_list = []
    for xml_file in tqdm(xml_file_list):
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


# YOU HAVE TO CHANGE THIS EVERY TIME AARON!!!!
#
# TO MATCH THE LABEL MAP
#
# TO MATCH THE LABEL MAP
#
def class_text_to_int(row_label):

    if row_label == 'dog':
        return 1
    elif row_label == 'cat':
        return 2
    else:
        return None


def split(df, group):

    data = namedtuple('data', ['filename', 'object'])
    gb = df.groupby(group)

    return [data(filename, gb.get_group(x)) for filename, x in zip(gb.groups.keys(), gb.groups)]


def create_tf_example(group, path):
    # print("opening " + group.filename)

    with tf.gfile.GFile(os.path.join(path, '{}'.format(group.filename)), 'rb') as fid:
        encoded_jpg = fid.read()

    classes = []

    for index, row in group.object.iterrows():
        classes.append(class_text_to_int(row['class']))

    tf_example = tf.train.Example(features=tf.train.Features(feature={
        'image/encoded': tf.train.Feature(bytes_list=tf.train.BytesList(value=[encoded_jpg])),
        'image/object/class/label': tf.train.Feature(int64_list=tf.train.Int64List(value=[classes[0]])),
    }))

    return tf_example


def gen_tfrecord(panda_df, output_path, data_path, num_shards = 10):
    """Creates a TFRecord of the current dataframe into the output file"""

    with contextlib2.ExitStack() as tf_record_close_stack:
        writer = tf_record_creation_util.open_sharded_output_tfrecords(
            tf_record_close_stack, output_path, num_shards)
        grouped = split(panda_df, 'filename')
        for idx, group in tqdm(enumerate(grouped)):
            # if idx % 100 == 0:
                # print("On image " + str(idx) + " of " + str(len(grouped)))
            tf_example = create_tf_example(group, os.path.join(data_path, "images/raw"))
            shard_idx = idx % num_shards
            writer[shard_idx].write(tf_example.SerializeToString())

        print("Successfully creates the TFRecords: {}".format(output_path))

