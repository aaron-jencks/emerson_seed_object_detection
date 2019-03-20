from __future__ import absolute_import, division, print_function
import tensorflow as tf

from .models import generate_model
from .data_utils import get_input_fn


def train_path(root_path: str, iterations: int, model_dir: str, batch_size: int, resolution=(28, 28), tensors_to_log={}):
    """Trains the nn for given number of iterations
    from the given model directory with a given batch_size"""

    print("I don't know how many training and testing samples you gave me")

    image_height = resolution[0]
    image_width = resolution[1]
    print("Images will be resized to ({}x{})".format(image_height, image_width))

    estimator = generate_model(model_dir, (image_height, image_width))

    # Executes either with or without logging depending on size of dictionary
    if len(tensors_to_log) > 0:
        logging_hook = tf.train.LoggingTensorHook(
            tensors=tensors_to_log, every_n_iter=50)

        estimator.train(input_fn=lambda: get_input_fn(root_path, batch_size), steps=iterations, hooks=[logging_hook])
    else:
        estimator.train(input_fn=lambda: get_input_fn(train_dict, batch_size), steps=iterations)

    return estimator.evaluate(input_fn=lambda: get_input_fn(test_dict, batch_size), steps=1)


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

    batch_size = 100
    iterations = 1000

    train_dictionary(train_dict, test_dict, iterations, model_dir, batch_size, tensors_to_log)


def test_directory(model_dir: str, tmp_dir: str = "", tensors_to_log={}):

    import numpy as np

    tf.logging.set_verbosity(tf.logging.INFO)

    if len(tmp_dir) is 0:
        pass

    # Load training and eval data
    ((train_data, train_labels),
     (eval_data, eval_labels)) = tf.keras.datasets.mnist.load_data()

    train_data = train_data / np.float32(255)
    train_labels = train_labels.astype(np.int32)  # not required

    eval_data = eval_data / np.float32(255)
    eval_labels = eval_labels.astype(np.int32)  # not required

    train_dict = {"data": train_data, "labels": train_labels}
    test_dict = {"data": eval_data, "labels": eval_labels}

    batch_size = 100
    iterations = 1000

    train_dictionary(train_dict, test_dict, iterations, model_dir, batch_size, tensors_to_log)

