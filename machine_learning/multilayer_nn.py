#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 19 09:32:25 2017

@author: louis
"""

import math
import numpy as np
import matplotlib.pyplot as plt
import nn_utilities as utils

class SimpleNeuralNetwork:
    def __init__(self, layers, initialization="he"):
        """
        Arguments:
        layers          -- list of (n_uints, activations) pairs that define network structure, including input layer X
        initialization  -- initialization scheme for model parameters, available options are [random, he, xavier]

        Returns:
        model -- A model for the network architecture
        """

        np.random.seed(3)
        self.layers = layers[:]
        self.parameters = {}

        for i in range(1, len(self.layers)):
            if initialization == "random":
                self.parameters["W" + str(i)] = np.random.randn(layers[i][0], layers[i-1][0]) * 0.01
                self.parameters["b" + str(i)] = np.zeros((layers[i][0], 1))

            elif initialization == "he":
                self.parameters["W" + str(i)] = np.random.randn(layers[i][0], layers[i-1][0]) * np.sqrt(2. / layers[i-1][0])
                self.parameters["b" + str(i)] = np.zeros((layers[i][0], 1))

            elif initialization == "xavier":
                self.parameters["W" + str(i)] = np.random.randn(layers[i][0], layers[i-1][0]) * np.sqrt(2. / (layers[i-1][0] + layers[i][0]))
                self.parameters["b" + str(i)] = np.zeros((layers[i][0], 1))

            elif initialization == "zero":
                self.parameters["W" + str(i)] = np.zeros((layers[i][0], layers[i-1][0]))
                self.parameters["b" + str(i)] = np.zeros((layers[i][0], 1))

        self.initialize_adam()

    def initialize_adam(self):
        """
        Initializes the velocity and squares of gradients as a python dictionary with:
                    - keys: "dW1", "db1", ..., "dWL", "dbL"
                    - values: numpy arrays of zeros of the same shape as the corresponding gradients/parameters.

        Updates:
        velocity -- python dictionary containing the current velocity.
                        v['dW' + str(l)] = velocity of dWl
                        v['db' + str(l)] = velocity of dbl
        squares  -- python dictionary that will contain the exponentially weighted average of the squared gradient.
                    s["dW" + str(l)] = ...
                    s["db" + str(l)] = ...
        """

        L = len(self.parameters) // 2 # number of layers in the neural networks
        self.velocity = {}
        self.squares = {}

        # Initialize velocity
        for l in range(L):
            self.velocity["dW" + str(l+1)] = np.zeros(self.parameters["W" + str(l+1)].shape)
            self.velocity["db" + str(l+1)] = np.zeros(self.parameters["b" + str(l+1)].shape)
            self.squares["dW" + str(l+1)] = np.zeros(self.parameters["W" + str(l+1)].shape)
            self.squares["db" + str(l+1)] = np.zeros(self.parameters["b" + str(l+1)].shape)


    def forward_prop(self, X):
        """
        Implement forward propagation for the [LINEAR->ACTIVATION]*(L)

        Arguments:
        X -- data, numpy array of shape (input size, number of examples)

        Returns:
        AL -- last post-activation value
        caches -- list of caches
        """
        caches = []
        A = X
        L = len(self.parameters) // 2 + 1 # len(parameters) = 1 (input) + 2 * n_layers

        for i in range(1, L):
            A_prev = A
            A, cache = linear_activation_forward(A_prev, self.parameters["W" + str(i)], self.parameters["b" + str(i)], activation=self.layers[i][1])
            caches += [cache]

        return A, caches

    def back_prop(self, AL, Y, caches, weight_decay):
        """
        Implement the backward propagation for the [LINEAR->ACTIVATION] * (L-2) -> LINEAR -> SOFTMAX

        Arguments:
        AL              -- probability vector, output of the forward propagation
        Y               -- true "label" one hot vector
        caches          -- list of caches
        weight_decay    -- weight decay multiplier, default to 0.0

        Returns:
        grads -- A dictionary with the gradients
                 grads["dA" + str(l-1)] = ...
                 grads["dW" + str(l)] = ...
                 grads["db" + str(l)] = ...
        """
        grads = {}
        L = len(caches) # the number of layers excluding input layer

        current_cache = caches[L-1]
        grads["dA" + str(L)], grads["dW" + str(L)], grads["db" + str(L)] = short_cut_softmax(AL, Y, current_cache, weight_decay)

        for l in reversed(range(L-1)):
            current_cache = caches[l]
            dA_prev_temp, dW_temp, db_temp = linear_activation_backward(grads["dA" + str(l+2)], current_cache, self.layers[l+1][1], weight_decay)
            grads["dA" + str(l+1)] = dA_prev_temp
            grads["dW" + str(l+1)] = dW_temp
            grads["db" + str(l+1)] = db_temp

        return grads

    def update_parameters(self, grads, beta1, beta2, learning_rate, time, epsilon=1e-8):
        """
        Update parameters using gradient descent

        Arguments:
        grads           -- python dictionary containing your gradients, output of L_model_backward
        beta            -- the momentum hyperparameter, scalar
        learning_rate   -- the learning rate, scalar
        time            -- time parameter in the exponentially average equation

        Updates:
        parameters -- python dictionary containing your updated parameters
                      parameters["W" + str(l)] = ...
                      parameters["b" + str(l)] = ...
        """

        v_corrected = {}                         # Initializing first moment estimate, python dictionary
        s_corrected = {}                         # Initializing second moment estimate, python dictionary

        for l in range(1, len(self.layers)):
            self.velocity["dW" + str(l)] = beta1 * self.velocity["dW" + str(l)] + (1-beta1) * grads["dW" + str(l)]
            self.velocity["db" + str(l)] = beta1 * self.velocity["db" + str(l)] + (1-beta1) * grads["db" + str(l)]
            v_corrected["dW" + str(l)] = self.velocity["dW" + str(l)] / (1 - math.pow(beta1, time))
            v_corrected["db" + str(l)] = self.velocity["db" + str(l)] / (1 - math.pow(beta1, time))

            self.squares["dW" + str(l)] = beta2 * self.squares["dW" + str(l)] + (1-beta2) * np.square(grads["dW" + str(l)])
            self.squares["db" + str(l)] = beta2 * self.squares["db" + str(l)] + (1-beta2) * np.square(grads["db" + str(l)])
            s_corrected["dW" + str(l)] = self.squares["dW" + str(l)] / (1 - math.pow(beta2, time))
            s_corrected["db" + str(l)] = self.squares["db" + str(l)] / (1 - math.pow(beta2, time))

            self.parameters["W" + str(l)] = self.parameters["W" + str(l)] - learning_rate * np.divide(v_corrected["dW" + str(l)], np.sqrt(s_corrected["dW" + str(l)]) + epsilon)
            self.parameters["b" + str(l)] = self.parameters["b" + str(l)] - learning_rate * np.divide(v_corrected["db" + str(l)], np.sqrt(s_corrected["db" + str(l)]) + epsilon)

    def train(self, X_train, Y_train, X_test, Y_test, mini_batch_size = 64, learning_rate=0.005, beta1=0.9, beta2=0.999, weight_decay=0.0, num_epochs=1000, epsilon=1e-8, verbose=True):
        """
        Trains the neural network as defined in model (self)

        Arguments:
        X_train         -- training data, numpy array of shape (n_features, n_examples)
        Y_train         -- training "label", one hot vector
        X_test          -- test data, numpy array of shape (n_features, n_examples)
        Y_test          -- test "label", one hot vector
        learning_rate   -- learning rate of the gradient descent update rule
        weight_decay    -- weight decay multiplier, default to 0.0
        num_epochs      -- number of epochs of
        epsilon         -- hyperparameter preventing division by zero in Adam updates
        verbose         -- if True, it prints the cost every 100 steps

        Updates:
        parameters -- parameters learnt by the model. They can then be used to predict.
        """

        costs = []                         # keep track of cost

        seed = 0
        time = 1

        # Loop (gradient descent)
        for i in range(0, num_epochs):

            seed = seed + 1

            minibatches = utils.random_mini_batches(X_train, Y_train, "one_hot", mini_batch_size, seed)

            for minibatch in minibatches:

                (minibatch_X, minibatch_Y) = minibatch

                AL, caches = self.forward_prop(minibatch_X)

                cost = utils.compute_cost(AL, minibatch_Y, self.parameters, weight_decay)

                grads = self.back_prop(AL, minibatch_Y, caches, weight_decay)

                self.update_parameters(grads, beta1, beta2, learning_rate, time, epsilon)

                if verbose and time % 100 == 0:
                    print ("Cost after time %i: %f" %(time, cost))
                    print ("Accuracy on training set after time %i : %f" %(time, self.evaluate_performance(X_train, Y_train)))
                    print ("Accuracy on test set after time %i : %f" %(time, self.evaluate_performance(X_test, Y_test)))
                if time % 100 == 0:
                    costs.append(cost)

                time = time + 1

        # plot the cost
        plt.plot(np.squeeze(costs))
        plt.ylabel('cost')
        plt.xlabel('iterations (per tens)')
        plt.title("Learning rate =" + str(learning_rate))
        plt.show()

    def evaluate_performance(self, X, Y):
        """
        Evaluate the classification accuracy of the model on the given data set

        Arguments:
        self -- model object
        X    -- input data, size [n_features, n_examples]
        Y    -- input label, size [n_out, n_examples]

        Returns:
        ret -- classification accuracy
        """

        y_hats_one_hot = self.predict_one_hot_output(X)
        correct = 0.
        for i in range(y_hats_one_hot.shape[1]):
            if all(y_hats_one_hot[:, i] == Y[:, i]):
                correct = correct + 1

        ret = correct / y_hats_one_hot.shape[1]

        assert(isinstance(ret, float))

        return ret


    def predict_class_output(self, x, mapping):
        """
        Arguments:
        self    -- model object
        x       -- input data, size [n_features, n_examples]
        mapping -- a dictionary mapping the labels from one_hot format to categorical format

        Returns:
        ret -- predicted class results, size [n_examples,]
        """

        AL, _ = self.forward_prop(x)
        one_hot = (AL >= np.max(AL, axis=0)).astype(np.float32)

        ret = []
        for i in range(one_hot.shape[1]):
            ret.append(mapping[str(one_hot[:, i])])
        ret = np.hstack(ret)
        return ret

    def predict_one_hot_output(self, x):
        """
        Arguments:
        self    -- model object
        x       -- input data, size [n_features, n_examples]

        Returns:
        ret -- predicted class results, size [n_outs, n_examples]
        """
        AL, _ = self.forward_prop(x)
        ret = (AL >= np.max(AL, axis=0)).astype(np.float32)

        return ret

    def gradient_check(self, X, Y, epsilon = 1e-7, weight_decay=0.0):
        """
        Checks if back_prop computes correctly the gradient of the cost output by forward_prop

        Arguments:
        x               -- input datapoint, of shape (input size, 1)
        y               -- true "label"
        epsilon         -- tiny shift to the input to compute approximated gradient with two sided difference
        weight_decay    -- weight decay multiplier

        Returns:
        difference -- difference between the approximated gradient and the backward propagation gradient
        """

        num_parameters = utils.calc_num_parameters(self.layers)
        parameters_values = utils.dictionary_to_vector(self.parameters, num_parameters)
        AL, caches = self.forward_prop(X)
        gradients = self.back_prop(AL, Y, caches, weight_decay)
        grad = utils.dictionary_to_vector(gradients, num_parameters)

        J_plus = np.zeros((num_parameters, 1))
        J_minus = np.zeros((num_parameters, 1))
        gradapprox = np.zeros((num_parameters, 1))

        # Compute gradapprox
        for i in range(num_parameters):

            thetaplus = np.copy(parameters_values)
            thetaplus[i][0] = thetaplus[i][0] + epsilon
            self.parameters = utils.vector_to_dictionary(thetaplus, self.layers)
            AL, _ = self.forward_prop(X)
            J_plus[i]  = utils.compute_cost(AL, Y, self.parameters, weight_decay)

            thetaminus = np.copy(parameters_values)
            thetaminus[i][0] = thetaminus[i][0] - epsilon
            self.parameters = utils.vector_to_dictionary(thetaminus, self.layers)
            AL, _ = self.forward_prop(X)
            J_minus[i]  = utils.compute_cost(AL, Y, self.parameters, weight_decay)

            gradapprox[i] = (J_plus[i] - J_minus[i]) / (2 * epsilon)

        numerator = np.linalg.norm(gradapprox - grad)
        denominator = np.linalg.norm(gradapprox) + np.linalg.norm(grad)                                         # Step 2'
        difference = numerator / denominator

        if difference > 1e-7:
            print ("\033[93m" + "There is a mistake in the backward propagation! difference = " + str(difference) + "\033[0m")
        else:
            print ("\033[92m" + "Your backward propagation works perfectly fine! difference = " + str(difference) + "\033[0m")

        return difference

def linear_forward(A, W, b):
    """
    Implement the linear part of a layer's forward propagation.

    Arguments:
    A -- activations from previous layer (or input data): (size of previous layer, number of examples)
    W -- weights matrix: numpy array of shape (size of current layer, size of previous layer)
    b -- bias vector, numpy array of shape (size of the current layer, 1)

    Returns:
    Z -- the input of the activation function, also called pre-activation parameter
    cache -- a python dictionary containing "A", "W" and "b" ; stored for computing the backward pass efficiently
    """

    Z = np.dot(W, A) + b

    assert(Z.shape == (W.shape[0], A.shape[1]))
    cache = (A, W, b)

    return Z, cache

def linear_activation_forward(A_prev, W, b, activation):
    """
    Implement the forward propagation for the LINEAR->ACTIVATION layer

    Arguments:
    A_prev -- activations from previous layer (or input data): (size of previous layer, number of examples)
    W -- weights matrix: numpy array of shape (size of current layer, size of previous layer)
    b -- bias vector, numpy array of shape (size of the current layer, 1)
    activation -- the activation to be used in this layer, stored as a text string: "sigmoid" or "relu"

    Returns:
    A -- the output of the activation function, also called the post-activation value
    cache -- a python dictionary containing "linear_cache" and "activation_cache";
             stored for computing the backward pass efficiently
    """

    if activation == "sigmoid":
        Z, linear_cache = linear_forward(A_prev, W, b)
        A, activation_cache = utils.sigmoid_cache(Z)

    elif activation == "relu":
        Z, linear_cache = linear_forward(A_prev, W, b)
        A, activation_cache = utils.relu_cache(Z)

    elif activation == "softmax":
        Z, linear_cache = linear_forward(A_prev, W, b)
        A, activation_cache = utils.softmax_cache(Z)

    cache = (linear_cache, activation_cache)

    return A, cache

def linear_backward(dZ, cache, weight_decay):
    """
    Implement the linear portion of backward propagation for a single layer (layer l)

    Arguments:
    dZ              -- Gradient of the cost with respect to the linear output (of current layer l)
    cache           -- tuple of values (A_prev, W, b) coming from the forward propagation in the current layer
    weight_decay    -- weight decay multiplier

    Returns:
    dA_prev -- Gradient of the cost with respect to the activation (of the previous layer l-1), same shape as A_prev
    dW -- Gradient of the cost with respect to W (current layer l), same shape as W
    db -- Gradient of the cost with respect to b (current layer l), same shape as b
    """
    A_prev, W, b = cache
    m = A_prev.shape[1]

    dW = 1./m * (np.dot(dZ, A_prev.T) + weight_decay * W)
    db = np.mean(dZ, axis=1, keepdims=True)
    dA_prev = np.dot(W.T, dZ)

    assert (dA_prev.shape == A_prev.shape)
    assert (dW.shape == W.shape)
    assert (db.shape == b.shape)

    return dA_prev, dW, db

def linear_activation_backward(dA, cache, activation, weight_decay):
    """
    Implement the backward propagation for the LINEAR->ACTIVATION layer.

    Arguments:
    dA              -- post-activation gradient for current layer l
    cache           -- tuple of values (linear_cache, activation_cache) we store for computing backward propagation efficiently
    activation      -- the activation to be used in this layer, stored as a text string: "sigmoid" or "relu"
    weight_decay    -- weight decay multiplier

    Returns:
    dA_prev -- Gradient of the cost with respect to the activation (of the previous layer l-1), same shape as A_prev
    dW      -- Gradient of the cost with respect to W (current layer l), same shape as W
    db      -- Gradient of the cost with respect to b (current layer l), same shape as b
    """
    linear_cache, activation_cache = cache
    if activation == "relu":
        dZ = utils.relu_backward(dA, activation_cache)
        dA_prev, dW, db = linear_backward(dZ, linear_cache, weight_decay)

    elif activation == "sigmoid":
        dZ = utils.sigmoid_backward(dA, activation_cache)
        dA_prev, dW, db = linear_backward(dZ, linear_cache, weight_decay)

    # correct implementation of sotfmax back prop needs tensor operations, the following softmax_backward is incorrect
    elif activation == "softmax":
        dZ = utils.softmax_backward(dA, activation_cache)
        dA_prev, dW, db = linear_backward(dZ, linear_cache, weight_decay)

    return dA_prev, dW, db

def short_cut_softmax(AL, targets, cache, weight_decay):
    """
    Implement the backward propagation for the softmax layer

    Arguments:
    AL              -- post-activation gradient for current layer l
    targets         -- one hot vector of targets in shape [n_outs, batch_size]
    cache           -- tuple of values (linear_cache, activation_cache) we store for computing backward propagation efficiently
    weight_decay    -- weight decay multiplier

    Returns:
    dA_prev -- Gradient of the cost with respect to the activation (of the previous layer l-1), same shape as A_prev
    dW      -- Gradient of the cost with respect to W (current layer l), same shape as W
    db      -- Gradient of the cost with respect to b (current layer l), same shape as b
    """
    linear_cache, activation_cache = cache
    dZ = AL - targets
    dA_prev, dW, db = linear_backward(dZ, linear_cache, weight_decay)

    return dA_prev, dW, db