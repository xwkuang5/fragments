import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier

np.random.seed(0)
"""
This python script replicates the experiment in http://blog.kaggle.com/2016/12/27/a-kagglers-guide-to-model-stacking-in-practice/.
Specifically, the script trains a KNN classifier and a linear support vector machine classifier on the dart throwing dataset.
The dataset contains dart throwing performances of four people (Bob, Kate, Mark and Sue). Each throw of a dart generates two features
and one label. The two features are the x and y coordinates of the final location of the dart on a [-1, -1] x [-1, 1] board, and the
label encodes the person who threw the dart. The resulting KNN classifier and the SVC classifier have dissimilar decision boundaries.
Therefore, it might be a good idea to build a stacking learner to use these two classifiers to make better predictions. A figure will
be generated after running the script, the three subplot shows the decision boundary of the KNN classifier, the SVC classifier and the
stacking learner respectively. As can be seen from the figure, the third subplot looks like a combination of the two subplots, indicating
that the two classifiers can complement each other.
"""


class StackingLearner:
    def __init__(self, skf, list_of_estimators):
        """Initialize the learner with a Cross Validation fold generator
        and a list of first level classifiers to learn from
        """

        self._skf = skf
        self._list_of_estimators = list_of_estimators
        self._num_estimators = len(list_of_estimators)

        self._trained = False

    def prepare_stacking_data(self, X_train, X_test, Y_train, Y_test):
        """Prepare training data for the stacking learner

        For each (training fold, testing fold) pair, we train the first
        level classifiers with the training fold and record their
        predictions on the testing fold. Predictions on the testing fold
        will serve as training data for the stacking learner. Note this
        cross validation procedure means that we have data leakage in the
        stacking data. 
        """

        prediction_folds = []
        target_folds = []

        # generate training data for the stacking learner
        for train_idx, test_idx in self._skf.split(X_train, Y_train):
            X_train_fold, X_test_fold = X_train[train_idx], X_train[test_idx]
            Y_train_fold, Y_test_fold = Y_train[train_idx], Y_train[test_idx]

            for estimator in self._list_of_estimators:

                estimator.fit(X_train_fold, Y_train_fold)

            prediction_folds.append(
                np.stack([
                    estimator.predict(X_test_fold)
                    for estimator in self._list_of_estimators
                ]))
            target_folds.append(Y_test_fold)

        stack_train_X = np.transpose(np.concatenate(prediction_folds, axis=1))
        stack_train_Y = np.concatenate(target_folds)

        # generate testing data for the stacking learner
        stack_test_X = []

        for estimator in self._list_of_estimators:

            estimator.fit(X_train, Y_train)

            stack_test_X.append(estimator.predict(X_test))

        stack_test_X = np.transpose(np.stack(stack_test_X))
        stack_test_Y = Y_test

        # create a label encoder to encode string predictions in integer format
        self._feature_encoder = LabelEncoder().fit(np.unique(stack_train_X))
        stack_train_X = self._feature_encoder.transform(
            stack_train_X.flatten()).reshape((-1, self._num_estimators))
        stack_test_X = self._feature_encoder.transform(
            stack_test_X.flatten()).reshape((-1, self._num_estimators))

        return stack_train_X, stack_test_X, stack_train_Y, stack_test_Y

    def train(self, X_train, Y_train, meta_learner):
        """Train a stacking learner given a meta learner
        """

        stack_train_X, stack_test_X, stack_train_Y, stack_test_Y = self.prepare_stacking_data(
            X_train, X_test, Y_train, Y_test)
        meta_learner.fit(stack_train_X, stack_train_Y)

        self._meta_learner = meta_learner

        self._trained = True

        return self._meta_learner.score(stack_test_X, stack_test_Y)

    def predict(self, X_test):
        """Use the trained stacking learner to make predictions
        """

        assert self._trained, "The meta learner has not been trained yet!"

        stack_test_X = np.transpose(
            np.stack([
                estimator.predict(X_test)
                for estimator in self._list_of_estimators
            ]))

        stack_test_X = self._feature_encoder.transform(
            stack_test_X.flatten()).reshape((-1, self._num_estimators))

        return self._meta_learner.predict(stack_test_X)


# path to data
train_csv_path = "../datasets/darts_train.csv"
test_csv_path = "../datasets/darts_test.csv"

# load data
train_csv = pd.read_csv(train_csv_path)
test_csv = pd.read_csv(test_csv_path)

# add distance to center to make svm learning easier
train_csv['Distance'] = train_csv.apply(
    lambda x: np.sqrt(x['XCoord']**2 + x['YCoord']**2), axis=1)
test_csv['Distance'] = test_csv.apply(
    lambda x: np.sqrt(x['XCoord']**2 + x['YCoord']**2), axis=1)

# convert dataframe to data
X_train = train_csv[['XCoord', 'YCoord', 'Distance']].values
Y_train = train_csv['Competitor'].values
X_test = test_csv[['XCoord', 'YCoord', 'Distance']].values
Y_test = test_csv['Competitor'].values

skf = StratifiedKFold(n_splits=5, random_state=0)

### Train a KNN classifier
knn_parameters = {'n_neighbors': list(range(1, 31))}

knn_clf = GridSearchCV(KNeighborsClassifier(), knn_parameters, cv=skf)
knn_clf.fit(X_train, Y_train)
best_knn_clf = knn_clf.best_estimator_

### Train a linear support vector machine classifier
svc_parameters = {
    'C': [.01, .1, 1, 10, 100, 1000, 2000],
    'multi_class': ['crammer_singer']
}

svc_clf = GridSearchCV(LinearSVC(), svc_parameters, cv=skf)
svc_clf.fit(X_train, Y_train)
best_svc_clf = svc_clf.best_estimator_

### Train a decision tree meta learner using the previous two classifiers
meta_learner = StackingLearner(skf, [best_knn_clf, best_svc_clf])
meta_learner_test_score = meta_learner.train(X_train, Y_train,
                                             DecisionTreeClassifier())

### Create meshgrid for visulization
xx, yy = np.meshgrid(np.arange(-1, 1, 0.01), np.arange(-1, 1, 0.01))
xxyy = np.c_[xx.ravel(), yy.ravel()]
xxyyzz = np.concatenate(
    [
        xxyy,
        np.apply_along_axis(
            lambda x: np.sqrt(x[0]**2 + x[1]**2), axis=1, arr=xxyy).reshape(
                -1, 1)
    ],
    axis=1)

knn_predictions = meta_learner._feature_encoder.transform(
    best_knn_clf.predict(xxyyzz)).reshape(xx.shape)
svc_predictions = meta_learner._feature_encoder.transform(
    best_svc_clf.predict(xxyyzz)).reshape(xx.shape)
meta_predictions = meta_learner._feature_encoder.transform(
    meta_learner.predict(xxyyzz)).reshape(xx.shape)
# plt.scatter does not take arbitrary string for color values
# so, convert string labels to integers
training_data_points = meta_learner._feature_encoder.transform(Y_train)

fig, axarr = plt.subplots(nrows=3, ncols=1, figsize=(5, 10))

# Plot decision boundaries for the three classifiers
axarr[0].contourf(xx, yy, knn_predictions, cmap=plt.cm.Spectral)
axarr[0].scatter(
    X_train[:, 0], X_train[:, 1], c=training_data_points, cmap=plt.cm.Spectral)
axarr[0].set_title("KNN Decision Boundary (score: {:.2f})".format(
    best_knn_clf.score(X_test, Y_test)))

axarr[1].contourf(xx, yy, svc_predictions, cmap=plt.cm.Spectral)
axarr[1].scatter(
    X_train[:, 0], X_train[:, 1], c=training_data_points, cmap=plt.cm.Spectral)
axarr[1].set_title("SVC Decision Boundary (score: {:.2f})".format(
    best_svc_clf.score(X_test, Y_test)))

axarr[2].contourf(xx, yy, meta_predictions, cmap=plt.cm.Spectral)
axarr[2].scatter(
    X_train[:, 0], X_train[:, 1], c=training_data_points, cmap=plt.cm.Spectral)
axarr[2].set_title("Meta Learner Decision Boundary (score: {:.2f})".format(
    meta_learner_test_score))

plt.tight_layout()
plt.show()
