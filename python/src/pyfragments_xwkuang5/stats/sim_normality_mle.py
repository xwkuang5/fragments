# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a demo of fitting gaussian and student t distribution to data with outliers
"""

import numpy as np
import matplotlib.pyplot as plt

p = .5
n = 100000
m = 10000

x = np.random.binomial(n, p, m)

x_bar = x / n

plt.hist(x_bar)