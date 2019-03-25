import tensorflow as tf
import tensorflow.estimator as te


def cnn_model_fn(features, labels, mode, params):
    """Model function for CNN."""
    # Input Layer
    input_layer = tf.reshape(features, [-1, params["height"], params["width"], 1])

    # Convolutional Layer #1
    conv1 = tf.keras.layers.Conv2D(
        filters=32,
        kernel_size=[5, 5],
        padding='same',
        activation=tf.nn.relu)(input_layer)

    # Pooling Layer #1
    pool1 = tf.keras.layers.MaxPooling2D(pool_size=[2, 2], strides=2)(conv1)

    # Convolutional Layer #2 and Pooling Layer #2
    conv2 = tf.keras.layers.Conv2D(
        filters=64,
        kernel_size=[5, 5],
        padding='same',
        activation=tf.nn.relu)(pool1)
    pool2 = tf.keras.layers.MaxPooling2D(pool_size=[2, 2], strides=2)(conv2)

    # Dense Layer
    # pool2_flat = tf.reshape(pool2, [-1, int(params["height"] / 4) * int(params["width"] / 4) * 64])
    pool2_flat = tf.keras.layers.Flatten()(pool2)
    dense = tf.keras.layers.Dense(units=1024, activation=tf.nn.relu)(pool2_flat)
    dropout = tf.keras.layers.Dropout(rate=0.4)(
        dense, training=mode == te.ModeKeys.TRAIN)

    # Logits Layer
    logits = tf.keras.layers.Dense(units=10)(dropout)

    pred_index = tf.argmax(input=logits, axis=1)

    predictions = {
        # Generate predictions (for PREDICT and EVAL mode)
        "classes": pred_index,
        # Add `softmax_tensor` to the graph. It is used for PREDICT and by the
        # `logging_hook`.
        "probabilities": tf.nn.softmax(logits, name="softmax_tensor")
    }

    if mode == te.ModeKeys.PREDICT:
        return te.EstimatorSpec(mode=mode, predictions=predictions)

    # Calculate Loss (for both TRAIN and EVAL modes)
    loss = tf.losses.sparse_softmax_cross_entropy(labels=labels, logits=logits)

    # Configure the Training Op (for TRAIN mode)
    if mode == te.ModeKeys.TRAIN:
        optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.001)
        train_op = optimizer.minimize(
            loss=loss,
            global_step=tf.train.get_global_step())
        return te.EstimatorSpec(mode=mode, loss=loss, train_op=train_op)

    # Add evaluation metrics (for EVAL mode)
    eval_metric_ops = {
        "accuracy": tf.metrics.accuracy(
            labels=labels, predictions=predictions["classes"])
    }
    return te.EstimatorSpec(
        mode=mode, loss=loss, eval_metric_ops=eval_metric_ops)


def generate_model(model_dir, image_size):
    """Generates a new tensorflow model using estimators"""

    return te.Estimator(
        model_fn=cnn_model_fn,
        model_dir=model_dir,
        params={"height": image_size[0], "width": image_size[1]}
    )
