#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 16:40:07 2017

@author: louis
"""

from sklearn.datasets.samples_generator import make_blobs
from sklearn.model_selection import train_test_split


def load_2Dblobs(n_samples, n_center, ratio=0.5, one_hot=True):
    """
    Arguments:
    n_samples -- number of samples to generate
    n_center  -- number of classes to generate
    ratio     -- train test ratio

    Returns:
    X_train -- training data in shape [n_train_samples, 2]
    Y_train -- training labels of the data in shape [n_train_samples, n_center]
    X_test  -- testing data in shape [n_test_samples, 2]
    Y_test  -- testing labels of the data in shape [n_test_samples, n_center]
    """

    X, y = make_blobs(
        n_samples=n_samples, centers=n_center, n_features=2, random_state=0)
    X_train, X_test, Y_train, Y_test = train_test_split(
        X, y, test_size=ratio, random_state=0)

    return X_train, Y_train, X_test, Y_test
