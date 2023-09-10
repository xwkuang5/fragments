#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 19 11:22:10 2017

@author: louis
"""

import numpy as np
import matplotlib.pyplot as plt

mu = 0
var = 1

n_samples = 100
nreps = 10000

sample_med = []

for i in range(nreps):

    x = np.random.normal(0, np.sqrt(var), n_samples)

    sample_med.append(np.median(x))

plt.hist(sample_med, histtype="bar")
print("sample mean: %f" % np.mean(np.array(sample_med)))
print("sample deviation: %f" % np.std(np.array(sample_med)))