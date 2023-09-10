import math
import numpy as np
import itertools
from functools import partial
import matplotlib.pyplot as plt


def parzen_window(query, sample, window_size):
    """
    Parameters
    ----------
    query: float
    sample: float
    window_size: float,
        size of the parzen window

    Returns
    ----------
    indicator: int
        1 if the sample falls within a unit hypercube around the query
        0 otherwise
    """

    return 1 if abs((query - sample) / window_size) < .5 else 0


def gaussian_kernel(query, sample, window_size):
    """
    Parameters
    ----------
    query: float
    sample: float
    window_size: float,
        size of the parzen window

    Returns
    ----------
    prob: float
    """

    unit_distance = (query - sample) / window_size

    return math.pow(2*math.pi, -0.5) * \
        np.exp(-0.5*np.dot(unit_distance, unit_distance))


def kernel_function_wrapper(window_size, kernel):
    """Wrapper for kernel function

    Parameters
    ----------
    window_size: float
        size of the kernel band width
    kernel: string
        kernel to use for estimation

    Returns
    ---------
    handle: partial method
    """

    if kernel == "parzen":
        return partial(parzen_window, window_size=window_size)
    elif kernel == "gaussian":
        return partial(gaussian_kernel, window_size=window_size)


def kernel_density_estimation(query, samples, window_size, kernel="gaussian"):
    """Evaluate value of the probability density function at position query

    Parameters
    ----------
    query: float
    samples: (m, )
        numpy array of float, m is the number of samples
    window_size: float
        size of the kernel band width
    kernel: string
        kernel to use for estimation

    Returns
    ---------
    prob: float
    """

    n_samples = samples.shape[0]

    kernel_function_handler = kernel_function_wrapper(window_size, kernel)

    return sum([
        kernel_function_handler(query, samples[idx])
        for idx in range(n_samples)
    ]) / (n_samples * window_size)


def kernel_density_estimation_wrapper(samples, window_size, kernel="gaussian"):
    """Wrapper for kernel density estimation function 

    Parameters
    ----------
    samples: (m, )
        numpy array of float, m is the number of samples
    window_size: float
        size of the kernel band width
    kernel: string
        kernel to use for estimation

    Returns
    ---------
    handle: partial method
    """

    return partial(
        kernel_density_estimation,
        samples=samples,
        window_size=window_size,
        kernel=kernel)


#########################################
# Standard normal distribution
#########################################

sample_size = 100
samples = np.random.normal(loc=0, scale=1, size=sample_size)

grid_1d = np.linspace(-10, 10, num=500, endpoint=True)

from scipy.stats import norm

window_size = [1, 2, 4, 8]

fig, axarr = plt.subplots(2, 2, sharex=True, sharey=True)

vectorized_norm_pdf = np.vectorize(norm.pdf)

# plot effect of window size
for i, j in itertools.product(range(2), range(2)):

    window_index = i + j

    parzen_window_estimation = np.vectorize(
        kernel_density_estimation_wrapper(
            samples=samples,
            window_size=window_size[window_index],
            kernel="parzen"),
        otypes=[np.float])
    gaussian_kernel_estimation = np.vectorize(
        kernel_density_estimation_wrapper(
            samples=samples,
            window_size=window_size[window_index],
            kernel="gaussian"),
        otypes=[np.float])

    pdf = vectorized_norm_pdf(grid_1d)
    pdf_parzen = parzen_window_estimation(grid_1d)
    pdf_gaussian = gaussian_kernel_estimation(grid_1d)

    line1, = axarr[i, j].plot(grid_1d, pdf, 'r', label="pdf")
    line2, = axarr[i, j].plot(grid_1d, pdf_parzen, 'g', label="parzen")
    line3, = axarr[i, j].plot(grid_1d, pdf_gaussian, 'b', label="gaussian")
    axarr[i, j].set_title("window size: {}".format(window_size[window_index]))

fig.legend(handles=[line1, line2, line3], loc="lower right")

plt.show()

#########################################
# Mixture of gaussian distributions
#########################################

means = [0, 3, 5]
stds = [1, 4, 2]

sample_size = 1000

n_distributions = 3
distribution_choice = np.random.choice(
    np.arange(3), p=[0.3, 0.4, 0.3], size=sample_size)


# Generate samples from a mixture of gaussians
def generate_samples(means, stds, distribution_choice):

    ret = []

    bin_counts = np.bincount(distribution_choice)

    for i in range(len(means)):
        ret += np.random.normal(
            loc=means[i], scale=stds[i], size=bin_counts[i]).tolist()

    return np.array(ret)


samples = generate_samples(means, stds, distribution_choice)

grid_1d = np.linspace(-10, 10, num=500, endpoint=True)

window_size = [1, 2, 4, 8]

fig, axarr = plt.subplots(2, 2, sharex=True, sharey=True)

# plot effect of window size
for i, j in itertools.product(range(2), range(2)):

    window_index = i + j

    parzen_window_estimation = np.vectorize(
        kernel_density_estimation_wrapper(
            samples=samples,
            window_size=window_size[window_index],
            kernel="parzen"),
        otypes=[np.float])
    gaussian_kernel_estimation = np.vectorize(
        kernel_density_estimation_wrapper(
            samples=samples,
            window_size=window_size[window_index],
            kernel="gaussian"),
        otypes=[np.float])

    pdf_parzen = parzen_window_estimation(grid_1d)
    pdf_gaussian = gaussian_kernel_estimation(grid_1d)

    line1 = axarr[i, j].hist(
        samples, bins=100, label="empirical", normed=True, color='r')
    line2, = axarr[i, j].plot(grid_1d, pdf_parzen, 'g', label="parzen")
    line3, = axarr[i, j].plot(grid_1d, pdf_gaussian, 'b', label="gaussian")
    axarr[i, j].set_title("window size: {}".format(window_size[window_index]))

fig.legend(handles=[line2, line3], loc="lower right")

plt.show()
