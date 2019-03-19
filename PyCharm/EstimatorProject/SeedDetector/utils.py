import tensorflow as tf

from .models import *


def train(train_dict, test_dict, iterations, model_dir, batch_size, logged_tensors=None):
    """Trains the nn for given number of iterations
    from the given model directory with a given batch_size"""

    with tf.Session() as session:

        estimator = generate_model(model_dir)

        train_input_fn = get_input_fn(train_dict["data"], train_dict["labels"], batch_size)
        eval_input_fn = get_input_fn(test_dict["data"], test_dict["labels"], batch_size)

        estimator.train(input_fn=train_input_fn, steps=iterations, hooks=[logged_tensors])

        return estimator.evaluate(input_fn=eval_input_fn)


def indefinite_train(train_dict, test_dict, batch_iterations, model_dir, batch_size, logged_tensors=None):

    try:
        while True:
            print(train(train_dict, test_dict, batch_iterations, model_dir, batch_size, logged_tensors))
    except Exception as e:
        # Catches the Ctrl+C break
        print("Finished training!")
        print(e)

