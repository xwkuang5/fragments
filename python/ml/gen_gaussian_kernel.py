#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 16 10:06:30 2017

@author: louis
"""

import numpy as np
import matplotlib.pyplot as plt
import cv2
from scipy.stats import multivariate_normal


def genGaussianKernel(height, width, ptsList, humanHeight=10):
    densityMap = np.zeros((height, width))
    xlim = (0, width)
    ylim = (0, height)
    x = np.linspace(xlim[0], xlim[1], width)
    y = np.linspace(ylim[0], ylim[1], height)
    xx, yy = np.meshgrid(x, y)
    xxyy = np.c_[xx.ravel(), yy.ravel()]
    ptsList = [(5, 5), (10, 10)]
    for x, y in ptsList:
        sigmaHead = 0.2 * humanHeight
        sigmaBody = 0.5 * humanHeight
        m1 = (x, y)
        s1 = np.eye(2) * sigmaHead
        k1 = multivariate_normal(mean=m1, cov=s1)

        m2 = (x, int(y + 0.2 * humanHeight))
        s2 = np.array([[sigmaHead, 0], [0, sigmaBody]])
        k2 = multivariate_normal(mean=m2, cov=s2)

        densityMap += (k1.pdf(xxyy) + k2.pdf(xxyy)).reshape((height, width))
    densityMap = densityMap / densityMap.sum(axis=(0, 1)) * len(ptsList)
    densityMap = (densityMap - np.min(densityMap)) / (
        np.max(densityMap) - np.min(densityMap))
    densityMap = np.array(densityMap * 255, dtype=np.uint8)
    densityMap = cv2.applyColorMap(densityMap, cv2.COLORMAP_JET)
    plt.imshow(densityMap)


ptsList = [(5, 5), (10, 10)]
genGaussianKernel(100, 100, ptsList)
