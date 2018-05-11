import math
import numpy as np
import matplotlib.pyplot as plt

def parzen_window(query, sample, window_size):
    """
    Parameters
    ----------
    query: (n, )
        numpy array of float
    sample: (n, )
        numpy array of float
    window_size: float,
        size of the parzen window

    Returns
    ----------
    indicator: int
        1 if the sample falls within a unit hypercube around the query
        0 otherwise
    """

    return int(np.all(np.abs(np.divide(query - sample, window_size)) <= .5))

def gaussian_kernel(query, sample, window_size):
    """
    Parameters
    ----------
    query: (n, )
        numpy array of float
    sample: (n, )
        numpy array of float
    window_size: float,
        size of the parzen window

    Returns
    ----------
    prob: float
    """

    dimension = query.shape[0]

    unit_distance = np.divide(query - sample, window_size)

    return math.pow(2*math.pi, -0.5*dimension) * np.exp(-0.5*np.dot(unit_distance, unit_distance))

print(gaussian_kernel(np.array([0]), np.array([0]), 1))