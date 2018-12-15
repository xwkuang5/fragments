"""
According to "An Introduction to Conditional Random Fields", the independence assumption made by
Naive Bayes model makes the model provide unreliable probability estimates, meaning that if some
features are repeated, the predicted probability will be inflated.
"""

import numpy as np
from copy import deepcopy
from sklearn import datasets
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split

random_state = 1

iris = datasets.load_iris()

x = iris.data
y = iris.target

x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.5, random_state=random_state)


def nb_experiment(x_train, y_train, x_test, y_test, model, repeat):

    x_train_repeated = np.tile(x_train, repeat)
    x_test_repeated = np.tile(x_test, repeat)

    model_cloned = deepcopy(model)

    model_cloned.fit(x_train_repeated, y_train)

    predictions = model_cloned.predict(x_test_repeated)
    predictions_proba = model_cloned.predict_proba(x_test_repeated)
    """
    In general we might need to check whether the predictions are the same for all repeated models. But I'm not doing
    them here because I don't expect performances of the repeated models to be worse in this case.
    """
    return np.choose(predictions, predictions_proba.T)


n_repeat = 4

result = [
    nb_experiment(x_train, y_train, x_test, y_test, MultinomialNB(), repeat=r)
    for r in range(1, n_repeat + 1)
]

from cycler import cycler
import matplotlib.pyplot as plt

plt.rc(
    'axes',
    prop_cycle=(cycler('color', ['r', 'g', 'b', 'y']) +
                cycler('linestyle', ['-', '--', ':', '-.'])))

ys = np.array(result)

x = np.arange(ys.shape[1])

for r in range(1, n_repeat + 1):
    plt.plot(x, ys[r - 1], label='repeat={}'.format(r))

plt.legend()
plt.title("Experiment on Naive Bayes Model with Repeated Features")
plt.savefig("figures/nb_model_repeated_features.png")
