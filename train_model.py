
# coding: utf-8

# In[3]:

import numpy as np
import cv2
import os
#import fetch_data
import random
import tflearn
from tflearn.layers.conv import conv_2d, max_pool_2d, conv_2d_transpose, residual_block
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
from tflearn.layers.normalization import batch_normalization
import tensorflow as tf

from glob import glob

tf.reset_default_graph()



if not os.path.exists('model3'):
    os.mkdir('model3')


def model():
    # loading saved numpy files with training data
    INPATH = 'training_input_cropped.npy'
    OUTPATH = 'training_output_cropped.npy'

    if not os.path.exists(INPATH) or not os.path.exists(OUTPATH):
        training_input, training_output = fetch_data.create_train_data()

    else:
        training_input = np.load(INPATH)
        training_output = np.load(OUTPATH)

        
    #split into training and validation set    
    X = training_input[:8].reshape(-1,100,100,3)        
    Y = training_output[:8].reshape(-1,100,100,3)

    test_x = training_input[2:].reshape(-1,100,100,3)
    test_y = training_output[2:].reshape(-1,100,100,3)


    convnet = input_data(shape=[None, 100, 100, 3], name='input')

    convnet = conv_2d(convnet, 32, 5, activation='relu')
    convnet = conv_2d(convnet, 64, 5, activation='relu')
    convnet = conv_2d(convnet,128, 5, activation='relu')
    convnet = conv_2d(convnet, 256, 5, activation='relu')
    convnet = conv_2d(convnet, 512, 5, activation='relu')

    convnet = conv_2d_transpose(convnet, 256, 5,[100,100], activation='relu')
    convnet = conv_2d_transpose(convnet, 128, 5,[100,100], activation='relu')
    convnet = conv_2d(convnet,32, 3, activation='relu')


    convnet = dropout(convnet, 0.8)

    convnet = conv_2d(convnet,3, 5, activation='linear')
    # Adam optizer used to minimize mean square loss between pixel values
    convnet = regression(convnet, optimizer='adam', learning_rate=0.001, loss='mean_square', name='targets')

    model = tflearn.DNN(convnet, tensorboard_dir='log')

    if len(glob('model3/sketch1*')) == 3:
        model.load('model3/sketch1')
        print('model loaded')
    else:
        model.fit({'input': X}, {'targets': Y}, n_epoch=6, validation_set=({'input': test_x}, {'targets': test_y}), 
        snapshot_step=500, show_metric=True)

        model.save('model3/sketch1')

    return model

if __name__ == '__main__':
    model()
