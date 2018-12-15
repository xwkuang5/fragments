#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 21:23:26 2017

@author: louis
"""

import math
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import OneHotEncoder


def approx_equal(x, y, epsilon=1e-8):
    return abs(x - y) < epsilon


def compute_cost(y_hats, targets, parameters, weight_decay):
    """
    Arguments:
    y_hats          -- vector of probabilities in shape [n_outs, batch_size]
    targets         -- one hot vector of targets in shape [n_outs, batch_size]
    weight_decay    -- weight decay multiplier

    Returns:
    cost -- cost values on a mini-batch
    """

    assert (y_hats.shape[1] == targets.shape[1])

    L = len(parameters) // 3 + 1

    cost = -1 * np.mean(np.sum(np.multiply(targets, np.log(y_hats)), axis=0))
    reg_cost = 0
    for l in range(1, L):
        reg_cost = reg_cost + .5 * weight_decay * np.sum(
            np.square(parameters["W" + str(l)]))
    reg_cost /= y_hats.shape[1]

    cost = cost + reg_cost

    assert (isinstance(cost, float))

    return cost


def convert_to_one_hot(y, enc=OneHotEncoder(sparse=False)):
    '''
    Arguments:
    y -- labels as a one-dimensional integer numpy array
    enc -- one hot encoder instance

    Returns:
    y_one_hot       -- labels as a two-dimensional integer numpy array where each row is a one hot vector
    idx_to_one_hot  -- a dictionary mapping the label from ordinal encoding to one hot encoding
    one_hot_to_idx  -- a dictionary mapping the label from one hot encoding to ordinal encoding
    '''

    idx_to_one_hot = {}
    one_hot_to_idx = {}
    y_one_hot = enc.fit_transform(y.reshape(-1, 1))

    for i in range(len(y)):
        idx_to_one_hot[str(y[i])] = y_one_hot[i]
        one_hot_to_idx[str(y_one_hot[i])] = y[i]

    return y_one_hot, idx_to_one_hot, one_hot_to_idx


def convert_to_column_major(data):
    '''
    Arguments:
    data -- two dimensional numpy array in shape [n_samples, n_features]

    Returns:
    ret -- two dimensional numpy array in shape [n_features, n_samples]
    '''

    ret = data.transpose()

    return ret


def random_mini_batches(X,
                        Y,
                        input_format="one_hot",
                        mini_batch_size=64,
                        seed=0):
    """
    Creates a list of random minibatches from (X, Y)

    Arguments:
    X -- input data, of shape (input size, number of examples)
    Y -- true "label" vector (1 for blue dot / 0 for red dot), of shape (1, number of examples)
    mini_batch_size -- size of the mini-batches, integer

    Returns:
    mini_batches -- list of synchronous (mini_batch_X, mini_batch_Y)
    """

    np.random.seed(seed)
    m = X.shape[1]
    mini_batches = []

    permutation = list(np.random.permutation(m))
    if input_format == "one_hot":
        shuffled_X = X[:, permutation]
        shuffled_Y = Y[:, permutation]

    else:
        shuffled_X = X[permutation, :]
        shuffled_Y = Y[permutation, :]

    num_complete_minibatches = math.floor(m / mini_batch_size)
    for k in range(0, num_complete_minibatches):
        if input_format == "one_hot":
            mini_batch_X = shuffled_X[:, k * mini_batch_size:(
                k + 1) * mini_batch_size]
            mini_batch_Y = shuffled_Y[:, k * mini_batch_size:(
                k + 1) * mini_batch_size]

        else:
            mini_batch_X = shuffled_X[k * mini_batch_size:(
                k + 1) * mini_batch_size, :]
            mini_batch_Y = shuffled_Y[k * mini_batch_size:(
                k + 1) * mini_batch_size, :]

        mini_batch = (mini_batch_X, mini_batch_Y)
        mini_batches.append(mini_batch)

    if m % mini_batch_size != 0:
        if input_format == "one_hot":
            mini_batch_X = shuffled_X[:, -(m % mini_batch_size):]
            mini_batch_Y = shuffled_Y[:, -(m % mini_batch_size):]

        else:
            mini_batch_X = shuffled_X[-(m % mini_batch_size):, :]
            mini_batch_Y = shuffled_Y[-(m % mini_batch_size):, :]
        mini_batch = (mini_batch_X, mini_batch_Y)
        mini_batches.append(mini_batch)

    return mini_batches


def plot_decision_boundary(pred_func, X, Y, one_hot_to_idx):
    '''
    Arguments:
    pred_func       -- prediction function that takes (X_train, Y_train) as argument
    X               -- data, numpy array of shape (input size, number of examples)
    Y               -- one hot vector of targets in shape [n_outs, batch_size]
    one_hot_to_idx  -- a dictionary mapping the label from one hot encoding to ordinal encoding

    Returns:
    ret -- two dimensional numpy array in shape [n_features, n_samples]
    '''

    # Set min and max values and give it some padding
    x_min, x_max = X[:, 0].min() - .5, X[:, 0].max() + .5
    y_min, y_max = X[:, 1].min() - .5, X[:, 1].max() + .5
    h = 0.1

    # Generate a grid of points with distance h between them
    xx, yy = np.meshgrid(
        np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

    # Predict the function value for the whole gid
    Z = pred_func(np.c_[xx.ravel(), yy.ravel()], one_hot_to_idx)
    Z = Z.reshape(xx.shape)

    # Plot the contour and training examples
    plt.contourf(xx, yy, Z, cmap=plt.cm.Spectral)
    plt.scatter(X[:, 0], X[:, 1], c=Y, cmap=plt.cm.Spectral)


def dictionary_to_vector(parameters, num_parameters):
    """
    Convert the parameter dictionary of a model into a one-dimensional vector

    Arguments:
    parameters      -- {"W1": ..., "WL": ..., "b1": ..., "bL": ..., "r1": ..., "rL": ...}
    num_parameters  -- total number of learnable parameters in the model

    Returns:
    ret -- a one-dimensiona vector in orders increasing key, note b > W
    """

    ret = np.zeros((num_parameters, 1))

    idx = 0
    for key in sorted(parameters.keys()):
        # skip activation key words
        if "A" in key:
            continue
        param = parameters[key]
        length = param.shape[0] * param.shape[1]
        ret[idx:idx + length, :] = param.reshape(-1, 1)[:]
        idx = idx + length

    return ret


def vector_to_dictionary(vector, layers):
    """
    Convert the parameter vector of a model into a dictionary used by the model

    Arguments:
    vector      -- one-dimensional vector in orders: "W1", "W2", "WL", "b1", "b2", "bL"
    layers      -- list of (n_uints, activations) pairs that define network structure, including input layer X

    Returns:
    ret -- parameter dictionary, {"W1": ..., "WL": ..., "b1": ..., "bL": ..., "r1": ..., "rL": ...}
    """

    ret = {}
    idx = 0

    # recover Ws first
    for l in range(1, len(layers)):
        length = layers[l][0] * layers[l - 1][0]
        ret["W" + str(l)] = vector[idx:idx + length].copy().reshape(
            (layers[l][0], layers[l - 1][0]))
        idx = idx + length

    # recover bs
    for l in range(1, len(layers)):
        length = layers[l][0]
        ret["b" + str(l)] = vector[idx:idx + length].copy().reshape(
            (layers[l][0], 1))
        idx = idx + length

    # recover rs
    for l in range(1, len(layers)):
        length = layers[l][0]
        ret["r" + str(l)] = vector[idx:idx + length].copy().reshape(
            (layers[l][0], 1))
        idx = idx + length

    return ret


def batch_norm_helper(Z, r, b, mean, var):
    """
    Implements the BN part at test time

    z_norm = (z - mu) / sqrt(var)
    z_norm_scale = r * z_norm + b

    Arguments:
        Z       -- linear net inputs, numpy array of shape (size of the current layer, number of examples)
        r       -- scale vector, numpy array of shape (size of the current layer, 1)
        b       -- bias vector, numpy array of shape (size of the current layer, 1)
        mean    -- mean of net input of training set
        var     -- variance of net input of test set

    Returns:
        ret     -- batch normalization output
    """

    Z_norm = np.divide(Z - mean, np.sqrt(var))

    ret = np.multiply(Z_norm, r) + b

    return ret


def calc_num_parameters(layers):
    """
    Compute the total number of learnable parameters in the model

    Arguments:
    layers      -- list of (n_uints, activations) pairs that define network structure, including input layer X

    Returns:
    ret -- total number of learnable parameters
    """

    ret = 0
    for l in range(1, len(layers)):
        ret = ret + layers[l][0] * (layers[l - 1][0] + 2)

    return ret


def sigmoid(z):
    """
    Arguments:
    z -- net input, column vector in shape [n_units, 1]

    Returns:
    ret -- sigmoid function outputs
    """

    ret = 1. / (1. + np.exp(-z))

    return ret


def sigmoid_cache(z):
    """
    Arguments:
    z -- net input, column vector in shape [n_units, 1]

    Returns:
    ret -- sigmoid function outputs
    cache -- copy of net net input, z
    """

    ret = 1. / (1. + np.exp(-z))
    cache = z.copy()

    return ret, cache


def sigmoid_backward(dA, Z):
    """
    Arguments:
    dA -- gradients of the cost with respect to the post-activations (current layer l)
    Z  -- cache of the pre-activations (current layer l)

    Returns:
    ret -- gradients of the cost with respect to the pre-activations (current layer l)
    """

    activation = sigmoid(Z)
    ret = np.multiply(dA, np.multiply(activation, 1 - activation))

    return ret


def tanh(z):
    """
    Arguments:
    z -- net input, column vector in shape [n_units, 1]

    Returns:
    ret -- hyperbolic tangent function outputs
    """

    ret = 2 * sigmoid(2 * z) - 1

    return ret


def tanh_cache(z):
    """
    Arguments:
    z -- net input, column vector in shape [n_units, 1]

    Returns:
    ret -- hyperbolic tangent function outputs
    cache -- copy of net input, z
    """

    ret = 2 * sigmoid(2 * z) - 1
    cache = z.copy()

    return ret, cache


def tanh_backward(dA, Z):
    """
    Arguments:
    dA -- gradients of the cost with respect to the post-activations (current layer l)
    Z  -- cache of the pre-activations (current layer l)

    Returns:
    ret -- gradients of the cost with respect to the pre-activations (current layer l)
    """

    activation = tanh(Z)
    ret = np.multiply(dA, 1 - np.square(activation))

    return ret


def relu(z):
    """
    Arguments:
    z -- net input, column vector in shape [n_units, 1]

    Returns:
    ret -- rectified linear unit function outputs
    """

    ret = np.multiply(z, (z >= 0))

    return ret


def relu_cache(z):
    """
    Arguments:
    z -- net input, column vector in shape [n_units, 1]

    Returns:
    ret -- rectified linear unit function outputs
    cache -- copy of net input, z
    """

    ret = np.multiply(z, (z >= 0))
    cache = z.copy()

    return ret, cache


def relu_backward(dA, Z):
    """
    Arguments:
    dA -- gradients of the cost with respect to the post-activations (current layer l)
    Z  -- cache of the pre-activations (current layer l)

    Returns:
    ret -- gradients of the cost with respect to the pre-activations (current layer l)
    """

    ret = np.multiply(dA, (Z > 0))

    return ret


def softmax(z):
    """
    Arguments:
    z -- net input, column vector in shape [n_units, 1]

    Returns:
    ret -- softmax function outputs computed in a numerically stable way
    """
    log_sum_exp_val = log_sum_exp(z)
    ret = np.exp(z - log_sum_exp_val)

    return ret


def softmax_cache(z):
    """
    Arguments:
    z -- net input, column vector in shape [n_units, 1]

    Returns:
    ret -- softmax function outputs computed in a numerically stable way
    cache -- copy of net input, z
    """

    log_sum_exp_val = log_sum_exp(z)
    ret = np.exp(z - log_sum_exp_val)
    cache = z.copy()

    return ret, cache


def softmax_backward(dA, Z):
    """
    Arguments:
    dA -- gradients of the cost with respect to the post-activations (current layer l)
    Z  -- cache of the post-activations (current layer l)

    Returns:
    ret -- gradients of the cost with respect to the pre-activations (current layer l)
    """

    A = softmax(Z)

    # mini_batch_size = 1
    # matrix = -np.outer(A, A) + np.multiply(np.eye(A.shape[0]), A)
    # ret = np.dot(matrix.T, dA)

    # mini_batch_size > 1
    # How do I vectorize this?
    stacked_prev = -np.stack(
        [np.outer(A[:, i], A[:, i]) for i in range(A.shape[1])]) + np.stack([
            np.multiply(np.eye(A.shape[0]), A[:, i])
            for i in range(A.shape[1])
        ])
    matrix = np.rollaxis(stacked_prev, 0, 3)

    stacked_post = np.stack(
        [np.dot(matrix[:, :, i].T, dA[:, i]) for i in range(dA.shape[1])])
    ret = np.rollaxis(stacked_post, 0, 2)

    return ret


def log_sum_exp(z):
    """
    Arguments:
    z -- column vector in shape [n_units, 1]

    Returns:
    ret -- scalar value equal to log of the sum of exponentials over the column
    """

    max_val_vec = np.max(z, axis=0, keepdims=True)
    ret = np.log(np.sum(np.exp(z - max_val_vec), axis=0,
                        keepdims=True)) + max_val_vec

    return ret
