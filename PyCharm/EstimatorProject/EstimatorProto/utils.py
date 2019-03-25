from __future__ import absolute_import, division, print_function
import tensorflow as tf

from .models import generate_model
from .data_utils import get_input_fn
import os

from tqdm import tqdm


def train_path(root_path: str, iterations: int, model_dir: str, batch_size: int, resolution=(28, 28), tensors_to_log={}):
    """Trains the nn for given number of iterations
    from the given model directory with a given batch_size"""

    print("I don't know how many training and testing samples you gave me")

    image_height = resolution[0]
    image_width = resolution[1]
    print("Images will be resized to ({}x{})".format(image_height, image_width))

    estimator = generate_model(model_dir, (image_height, image_width))

    data_path = os.path.join(root_path, "data")
    train_rec = os.path.join(data_path, "train.record")
    test_rec = os.path.join(data_path, "test.record")

    # Executes either with or without logging depending on size of dictionary
    if len(tensors_to_log) > 0:
        logging_hook = tf.train.LoggingTensorHook(
            tensors=tensors_to_log, every_n_iter=50)

        estimator.train(input_fn=lambda: get_input_fn(train_rec, batch_size, resolution), steps=iterations, hooks=[logging_hook])
    else:
        estimator.train(input_fn=lambda: get_input_fn(train_rec, batch_size, resolution), steps=iterations)

    return estimator.evaluate(input_fn=lambda: get_input_fn(test_rec, batch_size, resolution), steps=1)


def train_dictionary(train_dict: dict, test_dict: dict, iterations: int, model_dir: str, batch_size: int, tensors_to_log={}):
    """Trains the nn for given number of iterations
    from the given model directory with a given batch_size"""

    print("Given {} training examples and {} testing examples".format(
        len(train_dict["data"]), len(test_dict["data"])))

    image_height = len(train_dict["data"][0])
    image_width = len(train_dict["data"][0][0])
    print("Images will be resized to ({}x{})".format(image_height, image_width))

    estimator = generate_model(model_dir, (image_height, image_width))

    # Executes either with or without logging depending on size of dictionary
    if len(tensors_to_log) > 0:
        logging_hook = tf.train.LoggingTensorHook(
            tensors=tensors_to_log, every_n_iter=50)

        estimator.train(input_fn=lambda: get_input_fn(train_dict, batch_size), steps=iterations, hooks=[logging_hook])
    else:
        estimator.train(input_fn=lambda: get_input_fn(train_dict, batch_size), steps=iterations)

    return estimator.evaluate(input_fn=lambda: get_input_fn(test_dict, batch_size), steps=1)


def indefinite_train_dictionary(train_dict, test_dict, batch_iterations, model_dir, batch_size, logged_tensors={}):

    try:
        while True:
            print(train_dictionary(train_dict, test_dict, batch_iterations, model_dir, batch_size, logged_tensors))
    except Exception as e:
        # Catches the Ctrl+C break
        print("Finished training!")
        print(e)


def indefinite_train_path(root_path: str, batch_iterations: int, model_dir: str, batch_size: int,
                          resolution=(28, 28), logged_tensors={}):

    try:
        while True:
            print(train_path(root_path, batch_iterations, model_dir, batch_size, resolution, logged_tensors))
    except Exception as e:
        # Catches the Ctrl+C break
        print("Finished training!")
        print(e)


def test(model_dir, tensors_to_log={}):

    import numpy as np

    tf.logging.set_verbosity(tf.logging.INFO)

    # Load training and eval data
    ((train_data, train_labels),
     (eval_data, eval_labels)) = tf.keras.datasets.mnist.load_data()

    train_data = train_data / np.float32(255)
    train_labels = train_labels.astype(np.int32)  # not required

    eval_data = eval_data / np.float32(255)
    eval_labels = eval_labels.astype(np.int32)  # not required

    train_dict = {"data": train_data, "labels": train_labels}
    test_dict = {"data": eval_data, "labels": eval_labels}

    batch_size = 1
    iterations = 1000

    train_dictionary(train_dict, test_dict, iterations, model_dir, batch_size, tensors_to_log)


def test_directory(tensors_to_log={},
                   skip_conversion: bool = False, skip_split: bool = False, skip_tfr: bool = False):
    import urllib
    import tarfile
    import fnmatch
    import shutil

    from EstimatorProto.data_utils import setup_temp_model_dir

    tf.logging.set_verbosity(tf.logging.INFO)

    temp_ctx, temp_dir, data_dir, image_dir, annotation_dir, model_dir = setup_temp_model_dir("Path_Test")

    if not skip_conversion:
        IMAGE_URL = "http://www.robots.ox.ac.uk/~vgg/data/pets/data/images.tar.gz"
        ANNOTATION_URL = "http://www.robots.ox.ac.uk/~vgg/data/pets/data/annotations.tar.gz"

        # Downloads the image dataset
        image_path = os.path.join(data_dir, "images.tar.gz")
        annotation_path = os.path.join(data_dir, "annotations.tar.gz")

        if not (os.path.isfile(image_path) and os.path.isfile(annotation_path)):

            from Display.progress_bar import DownloadProgressBar

            def download_url(url, output_path):
                with DownloadProgressBar(unit='B', unit_scale=True,
                                         miniters=1, desc=url.split('/')[-1]) as t:
                    urllib.request.urlretrieve(url, filename=output_path, reporthook=t.update_to)

            if not os.path.isfile(image_path):
                print("Downloading images")
                download_url(IMAGE_URL, image_path)
            else:
                print("Using cached image data")
            if not os.path.isfile(annotation_path):
                print("Downloading annotations")
                download_url(ANNOTATION_URL, annotation_path)
            else:
                print("Using cached annotation data")
        else:
            print("Using cached data for images and annotations")

        print("Extracting")
        tarfile.open(image_path).extractall(data_dir)
        for f in tqdm(fnmatch.filter(os.listdir(image_dir), "*.jpg")):
            shutil.move(os.path.join(image_dir, f), os.path.join(os.path.join(image_dir, "raw"), os.path.basename(f)))
        tarfile.open(annotation_path).extractall(data_dir)
    else:
        print("Skipping the download and extraction")

    from SeedDetector.main import split_dataset, convert_tfr
    from EstimatorProto.data_utils import find_min_dim

    if not skip_split:
        min_dim = split_dataset(data_dir)
    else:
        print("Skipping the dataset split")
        # Gotta ensure that we have the minimum dimensions, even if we don't split the dataset.
        min_dim = find_min_dim(list(map(lambda x: os.path.join(image_dir, "raw/") + x,
                                        fnmatch.filter(os.listdir(os.path.join(image_dir, "raw/")), "*.jpg"))))

    if not skip_tfr:
        convert_tfr(data_dir)
    else:
        print("Skipping the tfrecord creation")

    batch_size = 1
    iterations = 1000

    train_path(data_dir, iterations, model_dir, batch_size, min_dim, tensors_to_log)

    print("Cleaning up directory")
    temp_ctx.cleanup()

