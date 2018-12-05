from matplotlib import pyplot as plt

import numpy as np
import os
import tensorflow as tf
import cv2
import inception_preprocessing
from inception_resnet_v2 import inception_resnet_v2, inception_resnet_v2_arg_scope



def classification(directory_name):
    log_dir = '/home/visbic/shoh/train_data/train_inception_resnet_v2_cracky_slim_FineTune_logs/4-001-60/after20'
    DEFAULT_DIRECTORY = "/home/visbic/shoh/cracky_test"

    completed_list = []
    slim = tf.contrib.slim

    image_size = inception_resnet_v2.default_image_size
    if(directory_name==""):
        directory_name = DEFAULT_DIRECTORY

    with tf.Graph().as_default():
        user_images = []  # 복수의 원본 이미지
        user_processed_images = []  # 복수의 전처리된 이미지

        image_files = os.listdir(directory_name)  # 분류하고 싶은 이미지가 저장된 폴더

        # 각 이미지마다 clahe를 적용하여 저장한다.
        for i in image_files:
            cvimage = cv2.imread(directory_name+ '/' + i)
            lab = cv2.cvtColor(cvimage, cv2.COLOR_BGR2LAB)
            lab_planes = cv2.split(lab)
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            lab_planes[0] = clahe.apply(lab_planes[0])
            lab = cv2.merge(lab_planes)
            clahe_img = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
            # image_input = tf.read_file(directory_name+ '/' + i)
            temp_image = cv2.imencode('.jpg', cvimage)[1].tostring()
            image = tf.image.decode_jpeg(temp_image, channels=3)

            user_images.append(image)
            processed_image = inception_preprocessing.preprocess_image(image, image_size, image_size, is_training=False)
            user_processed_images.append(processed_image)

        processed_images = tf.expand_dims(processed_image, 0)

        with slim.arg_scope(inception_resnet_v2_arg_scope()):
            logits, _ = inception_resnet_v2(user_processed_images, num_classes=3, is_training=False)
        probabilities = tf.nn.softmax(logits)

        init_fn = slim.assign_from_checkpoint_fn(
            tf.train.latest_checkpoint(log_dir),
            slim.get_model_variables('InceptionResnetV2'))

        with tf.Session() as sess:
            init_fn(sess)
            np_images, probabilities = sess.run([user_images, probabilities])

            names = ['crack', 'draw', 'no_crack']

        classify_list = []

        for files in range(len(image_files)):
            probabilitie = probabilities[files, 0:]
            sorted_inds = [i[0] for i in sorted(enumerate(-probabilitie), key=lambda x: x[1])]
            completed_image = np_images[files].astype(np.uint8)
            # draw_lined_image = draw_line(completed_image)
            completed_list.append(completed_image)
            classify_list.append(sorted_inds[0])
            for p in range(3):
                index = sorted_inds[p]
                print('Probability %0.2f%% => [%s]' % (probabilitie[index], names[index]))

        return completed_list, classify_list


def draw_line(image):
    IMAGE_SIZE = 256
    graph = tf.Graph()

    with tf.Session() as sess:
        predictions = graph.get_operation_by_name("predictions").outputs[0]
        x = graph.get_operation_by_name("x").outputs[0]
        broken_image, h, w, h_no, w_no = break_image(image, IMAGE_SIZE)

        output_image = np.zeros((h_no * IMAGE_SIZE, w_no * IMAGE_SIZE, 3), dtype=np.uint8)

        feed_dict = {x: broken_image}
        batch_predictions = sess.run(predictions, feed_dict=feed_dict)

        matrix_pred = batch_predictions.reshape((h_no, w_no))
        # Concentrate after this for post processing
        for i in range(0, h_no):
            for j in range(0, w_no):
                a = matrix_pred[i, j]
                output_image[IMAGE_SIZE * i:IMAGE_SIZE * (i + 1), IMAGE_SIZE * j:IMAGE_SIZE * (j + 1), :] = 1 - a

        cropped_image = image[0:h_no * IMAGE_SIZE, 0:w_no * IMAGE_SIZE, :]
        pred_image = np.multiply(output_image, cropped_image)

        return pred_image


def break_image(test_image, size):

    h, w = np.shape(test_image)[0], np.shape(test_image)[1]
    broken_image = []
    h_no = h // size
    w_no = w // size
    h = h_no * size
    w = w_no * size
    for i in range(0, h_no):
        for j in range(0, w_no):
            split = test_image[size * i:size * (i + 1), size * j:size * (j + 1), :]
            broken_image.append(split);

    return broken_image, h, w, h_no, w_no
