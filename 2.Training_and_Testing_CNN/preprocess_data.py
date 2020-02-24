#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import pandas as pd
import tensorflow as tf

def load_csv(path):
    images, labels = [], []
    with open(path) as f:
        reader = pd.read_csv(f)
        for i in range(reader.shape[0]):
            img = reader['Id'][0]
            images.append(img)
        labels = reader.drop(['Id'], axis=1)
        labels = labels.to_numpy()
        return images, labels


def load_images(root, label_path, mode='train'):
    # build a numerical code
    # read the label information
    images, labels = load_csv(label_path)
    if mode == 'train':
        images = images[:int(0.75 * len(images))]
        labels = labels[:int(0.75 * len(labels))]
    elif mode == 'val':
        images = images[int(0.75 * len(images)):int(0.85 * len(images))]
        labels = labels[int(0.75 * len(labels)):int(0.85 * len(labels))]
    else:
        images = images[int(0.85 * len(images)):]
        labels = labels[int(0.85 * len(labels)):]
    return images, labels


img_mean = tf.constant([0.485, 0.456, 0.406])
img_std = tf.constant([0.229, 0.224, 0.225])


def normalise(x, mean= img_mean, std= img_std):
    x = (x - mean) / std
    return x


def denormalise(x, mean= img_mean, std= img_std):
    x = x * std + mean
    return x


def preprocess(x, y):
    x = tf.io.read_file(x)
    x = tf.image.decode_jpeg(x, channels=3)
    x = tf.image.resize(x, [244, 244])

    # data augment
    x = tf.image.random_flip_left_right(x)
    x = tf.image.random_crop(x, [244, 244, 3])
    x = tf.cast(x, dtype=tf.float32) / 255.0
    x = normalise(x)
    y = tf.convert_to_tensor(y)
    return x, y


def main():
    import time
    # load the dataset
    images, labels, table = load_images('test', 'train')
    print('images:', len(images), images)
    print('labels:', len(labels), labels)
    print('table:', table)

    db = tf.data.Dataset.from_tensor_slices((images, labels))
    db = db.shuffle(1000).map(preprocess).batch(2)

    writter = tf.summary.create_file_writer('logs')
    for step, (x, y) in enumerate(db):
        with writter.as_default():
            x = denormalise(x)
            tf.summary.image('img', x, step=step, max_outputs=9)
            time.sleep(5)


if __name__ == '__main__':
    main()
