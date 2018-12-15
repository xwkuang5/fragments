import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt


class DecisionNode:
    def __init__(self, attr_idx, attr_thresh, flipped=False, error_rate=None):
        """Initialize a decision node

        Parameters
        ------------------
        attr_idx : int,
            index of the attribute used for making decisions
        
        attr_thresh : float,
            threshold used for making decisions

        flipped : boolean,
            whether to flip the decision of the decision node
        
        error_rate : float,
            error rate of the weak hypothesis (with non-uniform distribution)
        """

        self._attr_idx = attr_idx
        self._attr_thresh = attr_thresh
        self._flipped = flipped
        self._error_rate = error_rate

    def __str__(self):
        """String representation of the decision node

        Returns
        ------------------
        repr_string : string,
            the representation string for the decision node
        """

        sep_str = "-" * 50

        if self._flipped:
            decision_str = "\tf(x) = -1 if x[{}] <= {}, else +1".format(
                self._attr_idx, self._attr_thresh)
        else:
            decision_str = "\tf(x) = +1 if x[{}] <= {}, else -1".format(
                self._attr_idx, self._attr_thresh)

        if self._error_rate is not None:
            error_str = "\tError rate on training set: {:.4f}".format(
                self._error_rate)
            return "\n".join([
                sep_str, "Classification Node", decision_str, error_str,
                sep_str
            ])

        return "\n".join(
            [sep_str, "Classification Node", decision_str, sep_str])

    def classification(self, instance):
        """Make classification on the instance

        Parameters
        ------------------
        instance : (n, ) numpy array of float
            numpy instance to be classified
        """

        assert self._attr_idx < len(
            instance
        ), "Attribute index can not be greater than length of instances"

        if self._flipped:
            return -1 if instance[self._attr_idx] <= self._attr_thresh else 1
        else:
            return 1 if instance[self._attr_idx] <= self._attr_thresh else -1


class AdaBoost:
    """Binary AdaBoost classifier with decision stump base learner
    """

    def __init__(self, num_learners=300):
        """Initialize the adaboost classifier

        Parameters
        ------------------        
        num_learners : int,
            number of base learners to train
        """

        self._num_learners = num_learners

        self._base_learners = []
        self._base_learners_weights = []

    def construct_weak_hypothesis(self, train_X, train_Y, distribution):
        """Construct a weak hypothesis based on the training set

        Parameters
        ------------------
        train_X : (n, m) numpy array of float,
            training set

        train_Y : (n, ) numpy array of int,
            training labels, +1 / -1

        distribution : (n, ) numpy array of float,
            adjusted distribution of the training set

        Returns
        ------------------
        weak_hypothesis : DecisionNode,
            A newly constructed weak hypothesis 
        """

        # train_X[:, i][sorted_features_idx[i]][j] gives the j-th smallest value of feature i
        sorted_features_idx = [
            np.argsort(train_X[:, idx]) for idx in range(train_X.shape[1])
        ]

        positives = train_Y == 1

        num_examples = train_X.shape[0]

        errors = []

        # loop over all features
        for i in range(len(sorted_features_idx)):

            examples_idx_sorted_by_feature_i = sorted_features_idx[i]

            # dynamic programming to record error rates for different thresholds
            dp = [None] * (num_examples + 1)

            # classify all examples as -1
            dp[0] = distribution[positives].sum()

            errors.append((i, 0, dp[0], False))
            errors.append((i, 0, 1 - dp[0], True))

            # loop over all possible thresholds
            for j in range(1, num_examples + 1):

                orig_idx = examples_idx_sorted_by_feature_i[j - 1]

                if train_Y[orig_idx] == 1:
                    dp[j] = dp[j - 1] - distribution[orig_idx]
                else:
                    dp[j] = dp[j - 1] + distribution[orig_idx]

                # append normal error
                errors.append((i, j, dp[j], False))
                # append flipped error
                errors.append((i, j, 1 - dp[j], True))

        fea_idx, sorted_example_idx, error_rate, flipped = min(
            errors, key=lambda x: x[2])

        if sorted_example_idx == 0:
            fea_thresh = train_X[:,
                                 fea_idx][sorted_features_idx[fea_idx]][sorted_example_idx] - 0.5
        else:
            fea_thresh = train_X[:, fea_idx][sorted_features_idx[fea_idx]][
                sorted_example_idx - 1]

        return DecisionNode(fea_idx, fea_thresh, flipped, error_rate)

    def train(self, train_X, train_Y, test_X=None, test_Y=None):
        """Train the classifier

        Parameters
        ------------------
        train_X : (n, m) numpy array of float,
            training set

        train_Y : (n, ) numpy array of int,
            training labels, +1 / -1

        test_X : (n, m) numpy array of float,
            testing set

        test_Y : (n, ) numpy array of int,
            testing labels, +1 / -1

        Returns
        ------------------
        training_history : (int, float),
            history of (iteration, error rate) pairs
        
        testing_history : (int, float),
            history of (iteration, error rate) pairs
        """

        train_history = []
        test_history = []

        for iteration in range(1, self._num_learners + 1):

            if iteration == 1:
                weights = np.ones(train_Y.shape)
            else:
                weights = np.exp(
                    np.multiply(-1 * train_Y,
                                np.dot(
                                    self.prediction_vector(train_X),
                                    self._base_learners_weights)))

            # readjust training distributions
            distribution = weights / weights.sum()

            # construct new hypothesis
            weak_hypothesis = self.construct_weak_hypothesis(
                train_X, train_Y, distribution)

            correct_prediction_idx = [
                idx for idx in range(train_X.shape[0])
                if train_Y[idx] == weak_hypothesis.classification(
                    train_X[idx])
            ]

            wt_plus = weights[correct_prediction_idx].sum()
            wt_minus = weights.sum() - wt_plus

            # add weights and base learners
            self._base_learners.append(weak_hypothesis)
            self._base_learners_weights.append(.5 * np.log(wt_plus / wt_minus))

            train_history.append((iteration, self.error_rate(train_X,
                                                             train_Y)))

            if test_X is not None and test_Y is not None:
                test_history.append((iteration, self.error_rate(
                    test_X, test_Y)))

        return train_history, test_history

    def predict(self, instances):
        """Predict labels for instances

        Parameters
        ------------------
        instances : (n, m) numpy array of float,
            instances to be predicted

        Returns
        ------------------
        predictions : (n, ) numpy array of int,
            array of labels +1 / -1
        """

        def func(instance):
            if np.dot(
                    self.prediction_vector(instance),
                    self._base_learners_weights) >= 0:
                return 1
            else:
                return -1

        if len(instances.shape) == 1:
            return func(instances)

        return np.apply_along_axis(func, 1, instances)

    def prediction_vector(self, instances):
        """Predict vector labels for instances

        Parameters
        ------------------
        instances : (n, m) numpy array of float,
            instances to be predicted

        Returns
        ------------------
        predictions : (n, num_learners) numpy array of int,
            array of labels +1 / -1
        """

        if len(instances.shape) == 1:
            return np.array([
                node.classification(instances) for node in self._base_learners
            ])
        else:
            return np.apply_along_axis(lambda x: np.array([node.classification(x) for node in self._base_learners]), 1, instances)

    def error_rate(self, X, y):
        """Calculate the error rate of the classifier

        Parameters
        ------------------
        X : (n, m) numpy array of float,
            data instances
        y : (n, ) numpy array of int,
            array of labels +1 / -1

        Returns
        ------------------
        error_rate : float,
            error rate of the classifier
        """

        predictions = self.predict(X)

        return 1.0 - np.mean(predictions == y)


from sklearn import datasets

# load datasets
X, y = datasets.make_hastie_10_2(n_samples=12000, random_state=1)

# train test split
X_test, y_test = X[2000:], y[2000:]
X_train, y_train = X[:2000], y[:2000]

# initialize the classifier
adaboost = AdaBoost(300)

# train the classifier
train_history, test_history = adaboost.train(X_train, y_train, X_test, y_test)

iteration, train_errors = zip(*train_history)
_, test_errors = zip(*test_history)

# plot error curve
plt.plot(iteration, train_errors, 'r', label="training error rate")
plt.plot(iteration, test_errors, 'b', label="testing error rates")
plt.legend()
plt.title("Training and testing error of decision stump AdaBoost")
plt.xlabel("Number of estimators")
plt.ylabel("Error rate")
plt.show()
plt.savefig("figures/AdaBoost300WeakLearners.png")
