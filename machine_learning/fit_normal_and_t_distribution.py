# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a demo of fitting gaussian and student t distribution to data with outliers
"""

import scipy
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats


def genData(numPts, numOutliers, mu=0, sigma=1):
    data = np.random.normal(mu, sigma, numPts)
    data = np.append(data, np.random.uniform(mu, mu + 3 * sigma, numOutliers))
    return data


distributions = ['norm', 't']
numPts = 1000
numOutliers = 300
size = numPts + numOutliers

y = genData(numPts, numOutliers)
x = np.linspace(int(np.amin(y)), int(np.amax(y)), 1000)
h = plt.hist(y, bins=int(np.amax(y)) - int(np.amin(y)))
for distName in distributions:
    dist = getattr(scipy.stats, distName)
    param = dist.fit(y)
    if distName == 'norm':
        rv = scipy.stats.norm(*param)
    elif distName == 't':
        rv = scipy.stats.t(param[0])
    plt.plot(x, rv.pdf(x) * size, label=distName)
plt.legend()
plt.grid()
plt.show()
