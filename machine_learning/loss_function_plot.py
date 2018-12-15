import numpy as np
import matplotlib.pyplot as plt


def logistic_loss(x):

    return np.log(1 + np.exp(1 - x))


def hinge_loss(x):

    tmp = 1 - x

    tmp[np.where(tmp <= 0)] = 0

    return tmp


def squared_hinge_loss(x):

    tmp = 1 - x

    tmp[np.where(tmp <= 0)] = 0

    return np.square(tmp)


x = np.arange(-4, 4, 0.001)

plt.plot(x, logistic_loss(x), 'r')
plt.plot(x, hinge_loss(x), 'g')
plt.plot(x, squared_hinge_loss(x), 'b')
plt.legend(["logistic loss", "hinge loss", "squared hinge loss"])
plt.title("Loss function")
plt.show()
