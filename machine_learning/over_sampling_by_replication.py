"""
This script tests the intuition behind the Synthetic Minority Over-sampling 
Technique (SMOTE). Bascially, the intution behind the technique is that
simply over-sample the minority class by replicating will lead to overfitting.
The authors argue that replicating minority samples will cause the decision
boundary to become overly specific. Intuitively, if we do not have prior 
knowledge about the distribution of the input data, we should not mislead 
the learning algorithm to think that way, which arguably is what replication 
is doing. Therefore, the SMOTE algorithm can be thought of as a more
conservative way of doing data replication: we do not have 100% confidence
that the data will appear exactly the same as the sampled data. However, we
believe that unseen data should be close to the sampled data and its neighbors.

It is hard to replicate the results exactly without going into more details about
creating an artificial datasets. However, the figure shown by this script should
provide some evidence that the intution may be true to some extent. The second
plot in the figure shows that the algorithm learns more decision boundaries for the
second class due to over-sampling, which may (or may not) be a result of overfitting.

Installed packages:
    Package          Version
    ---------------- -------
    cycler           0.10.0 
    imbalanced-learn 0.3.3  
    imblearn         0.0    
    kiwisolver       1.0.1  
    matplotlib       2.2.2  
    numpy            1.14.3 
    pip              10.0.1 
    pyparsing        2.2.0  
    python-dateutil  2.7.2  
    pytz             2018.4 
    scikit-learn     0.19.1 
    scipy            1.1.0  
    setuptools       39.1.0 
    six              1.11.0 
    wheel            0.31.0 
"""

import numpy as np
import matplotlib.pyplot as plt

from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import make_classification

from imblearn.over_sampling import RandomOverSampler

X, y = make_classification(
    n_samples=5000,
    n_features=2,
    n_informative=2,
    n_redundant=0,
    n_repeated=0,
    n_classes=2,
    n_clusters_per_class=2,
    weights=[0.95, 0.05],
    flip_y=0,
    class_sep=0.1,
    random_state=0)

# over-sample the minority class
ros = RandomOverSampler({1: 3000}, random_state=0)

X_resampled, y_resampled = ros.fit_sample(X, y)

# create mesh grid
x_min = min(min(X[:, 0]), min(X_resampled[:, 0]))
x_max = max(max(X[:, 0]), max(X_resampled[:, 0]))

y_min = min(min(X[:, 1]), min(X_resampled[:, 1]))
y_max = max(max(X[:, 1]), max(X_resampled[:, 1]))

xx, yy = np.meshgrid(
    np.arange(x_min, x_max, 0.1), np.arange(y_min, y_max, 0.1))

f, axarr = plt.subplots(2, 1, sharex='col', figsize=(10, 8))
"""
Raw data
"""
clf = DecisionTreeClassifier(max_depth=4)
clf.fit(X[:, :2], y)

Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)

axarr[0].contourf(xx, yy, Z, alpha=0.4)
axarr[0].scatter(X[:, 0], X[:, 1], c=y, s=20, edgecolor='k')
axarr[0].set_title("Original data")
"""
Minority-class-over-sampled data
"""
clf_resampled = DecisionTreeClassifier(max_depth=4)
clf_resampled.fit(X_resampled[:, :2], y_resampled)

Z = clf_resampled.predict(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)

axarr[1].contourf(xx, yy, Z, alpha=0.4)
axarr[1].scatter(
    X_resampled[:, 0], X_resampled[:, 1], c=y_resampled, s=20, edgecolor='k')
axarr[1].set_title("Over-sampled data")

plt.show()
