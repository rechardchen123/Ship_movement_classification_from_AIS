#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
matplotlib.rcParams['font.size'] = 18
matplotlib.rcParams['figure.titlesize'] = 18
matplotlib.rcParams['figure.figsize'] = [9, 7]
matplotlib.rcParams['font.family'] = ['Times New Roman']
matplotlib.rcParams['axes.unicode_minus'] = False

import os
import tensorflow as tf
import numpy as np
from tensorflow import keras
from tensorflow.keras import layers, optimizers, losses
from tensorflow.keras.callbacks import EarlyStopping
from datetime import datetime

EPOCHS = 50
batchsz = 32
log_dir = '/home/ucesxc0/Scratch/output/second_training_images_1/cnn_tf2_1/logs'
root = '/home/ucesxc0/Scratch/output/second_training_images_1/cnn_tf2_1/merged_image_for_training'
label_path = '/home/ucesxc0/Scratch/output/second_training_images_1/cnn_tf2_1/label.csv'

tf.random.set_seed(1234)
np.random.seed(1234)
os.environ['TF_CPP_MIN_LOG_lEVEL'] = '2'
assert tf.__version__.startswith('2.')
from preprocess_data import load_images


def preprocess(x, y):
    x = tf.io.read_file(root + '/' + x)
    x = tf.image.decode_jpeg(x, channels=3)
    x = tf.image.resize(x, [244, 244])
    x = tf.image.random_flip_left_right(x)
    x = tf.image.random_flip_up_down(x)
    x = tf.image.random_crop(x, [244, 244, 3])

    x = tf.cast(x, dtype=tf.float32) / 255.
    x = tf.image.per_image_standardization(x)
    y = tf.convert_to_tensor(y)
    # y = tf.one_hot(y, depth=3)
    return x, y


# build the training dataset
images, labels = load_images(root, label_path, mode='train')
db_train = tf.data.Dataset.from_tensor_slices((images, labels))
db_train = db_train.shuffle(1000).map(preprocess).batch(batchsz)
# build the validation dataset
images2, labels2 = load_images(root, label_path, mode='val')
db_val = tf.data.Dataset.from_tensor_slices((images2, labels2))
db_val = db_val.map(preprocess).batch(batchsz)
# build the test dataset
images3, labels3 = load_images(root, label_path, mode='test')
db_test = tf.data.Dataset.from_tensor_slices((images3, labels3))
db_test = db_test.map(preprocess).batch(batchsz)

# build the network
net = tf.keras.Sequential()
net.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(244, 244, 3)))
net.add(layers.BatchNormalization())
net.add(layers.Conv2D(32, (3, 3), activation='relu'))
net.add(layers.BatchNormalization())
net.add(layers.MaxPool2D(2, 2))
net.add(layers.Dropout(0.2))
net.add(layers.Conv2D(64, (3, 3), activation='relu'))
net.add(layers.BatchNormalization())
net.add(layers.Conv2D(64, (3, 3), activation='relu'))
net.add(layers.BatchNormalization())
net.add(layers.MaxPool2D(2, 2))
net.add(layers.Dropout(0.3))
net.add(layers.Conv2D(128, (3, 3), activation='relu'))
net.add(layers.BatchNormalization())
net.add(layers.Conv2D(128, (3, 3), activation='relu'))
net.add(layers.BatchNormalization())
net.add(layers.MaxPool2D(2, 2))
net.add(layers.Dropout(0.4))
net.add(layers.Conv2D(256, (3, 3), activation='relu'))
net.add(layers.BatchNormalization())
net.add(layers.Conv2D(256, (3, 3), activation='relu'))
net.add(layers.BatchNormalization())
net.add(layers.MaxPool2D(2, 2))
net.add(layers.Dropout(0.5))
net.add(layers.Flatten())
net.add(layers.Dense(3, activation='sigmoid'))
net.summary()

# build Early Stopping class, if the loss does not descent in the continuous three times,
# the training should be stopped.

#early_stopping = EarlyStopping(monitor='val_accuracy', min_delta=0.001, patience=3)

metrics = [keras.metrics.TruePositives(name='tp'),
           keras.metrics.FalsePositives(name='fp'),
           keras.metrics.TruePositives(name='tn'),
           keras.metrics.FalsePositives(name='fn'),
           keras.metrics.BinaryAccuracy(name='accuracy'),
           keras.metrics.Precision(name='precision'),
           keras.metrics.Recall(name='recall'),
           keras.metrics.AUC(name='auc')]
net.compile(optimizer=optimizers.Adam(), loss='binary_crossentropy', metrics=metrics)
# define the keras tensorboard callback and checkpoint
logdir = log_dir + datetime.now().strftime("%Y%m%d-%H%M%S")
tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=logdir)
checkpoint_path = 'checkpoint/cp-{epoch:04d}.ckpt'
checkpoint_dir = os.path.dirname(checkpoint_path)
cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_path, save_weights_only=True,
                                                 verbose=1, save_freq=1)
# history = net.fit(db_train, validation_data=db_val, validation_freq=1, epochs=EPOCHS,
#                   callbacks=[early_stopping, tensorboard_callback, cp_callback])
history = net.fit(db_train, validation_data=db_val, validation_freq=1, epochs=EPOCHS,
                  callbacks=[tensorboard_callback, cp_callback])
history = history.history
print(history.keys())
print(history['val_accuracy'])
print(history['accuracy'])
print(history['precision'])
print(history['recall'])
print(history['tp'])
print(history['fp'])
print(history['tn'])
print(history['fn'])
print(history['auc'])

test_acc = net.evaluate(db_test)

plt.figure()
returns = history['val_accuracy']
plt.plot(np.arange(len(returns)), returns, label='validation accuracy')
plt.plot(np.arange(len(returns)), returns, 's')
returns = history['accuracy']
plt.plot(np.arange(len(returns)), returns, label='training accuracy')
plt.plot(np.arange(len(returns)), returns, 's')

plt.plot([len(returns) - 1], [test_acc[-1]], 'D', label='test accuracy')
plt.xlabel('Epoch')
plt.ylabel('accuracy')
plt.savefig('scratch.svg')
