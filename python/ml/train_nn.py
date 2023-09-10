#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 22 11:17:51 2017

@author: louis
"""

import numpy as np
import matplotlib.pyplot as plt
from gen_data import load_2Dblobs
from multilayer_nn import SimpleNeuralNetwork
from sklearn.preprocessing import OneHotEncoder
import nn_utilities as utils

np.random.seed(1)

plt.rcParams['figure.figsize'] = (5.0, 4.0)  # set default size of plots
plt.rcParams['image.interpolation'] = 'nearest'
plt.rcParams['image.cmap'] = 'gray'

X_train, Y_train, X_test, Y_test = load_2Dblobs(
    5000, n_center=5, ratio=0.5, one_hot=True)

enc = OneHotEncoder(sparse=False)
# training sample should be large enough to cover all encoding cases
Y_train_one_hot, idx_to_one_hot, one_hot_to_idx = utils.convert_to_one_hot(
    Y_train, enc)
Y_test_one_hot, _, _ = utils.convert_to_one_hot(Y_test, enc)

layers = []
layers.append((X_train.shape[1], "linear"))
layers.append((10, "relu"))
layers.append((10, "relu"))
layers.append((10, "relu"))
layers.append((Y_train_one_hot.shape[1], "softmax"))

model = SimpleNeuralNetwork(layers, "xavier")
"""
# gradient check
grad_check_x = X_train[0, :].reshape(-1, 1)
grad_check_y = Y_train_one_hot[0, :].reshape(-1, 1)
model.gradient_check(grad_check_x, grad_check_y, epsilon=1e-8, weight_decay=.0)
"""

# model training
model.train(
    X_train.T,
    Y_train_one_hot.T,
    X_test.T,
    Y_test_one_hot.T,
    mini_batch_size=64,
    learning_rate=0.005,
    weight_decay=0.,
    keep_prob=0.5,
    num_epochs=100)

plt.scatter(
    X_train[:, 0], X_train[:, 1], s=40, c=Y_train, cmap=plt.cm.Spectral)

utils.plot_decision_boundary(lambda x, y: model.predict_class_output(x.T, y),
                             X_train, Y_train, one_hot_to_idx)
