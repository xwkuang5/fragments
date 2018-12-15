import numpy as np
from functools import reduce
from functools import partial

import matplotlib.pyplot as plt


class CoinTossEMEstimator:
    def __init__(self, num_coins, coin_priors):
        """Initialize the estimator

        Parameters
        -------------
        num_coins : int
            number of coins, i.e., number of clusters

        coin_priors : list of float
            prior beliefs about the coin selection process. The priors 
            are used when calculating the probabilities p_zk_xi. In 
            general the priors can be estimated along with other latent 
            parameters using the EM algorithm.

        Note
        -------------
        For the coin tossing estimator, the E-step and the M-step are as follows:
            E-step:
                Q_i(z_k) = p(x_i | z_k; theta) * prior(z_k) / 
                    (\sum_k=1^K p(x_i | z_k; theta) * prior(z_k))
            M-step:
                theta_k = (\sum_i=1^m \sum_j=1^n Q_ik * X_ij) / 
                    (\sum_i=1^m \sum_j=1^n Q_ik)
        """

        assert num_coins == len(coin_priors), "Number of coins does not match \
            the length of coin_priors"

        self._num_coins = num_coins
        self._coin_priors = coin_priors

        # estimate for the parameters of interest, thetas
        self._thetas_hat = None
        """
        Q_i(z), i.e., any distribution over the latent variable Z
        If we set Q_i(z) to be P(z|x_i; theta), we get the lower
        bound of the p_xi_zk assuming theta does not change
        """
        self._Qi_zk = None

    def estimate(self, samples, thetas, tolerance_ratio, max_iter=20):
        """Perform EM iteration for parameter estimation

        Parameters
        -------------
        samples : (m, n) numpy array of int (specifically, 0s and 1s)
            samples obtained from the coin tossing experiment

        thetas : list of float
            initial guess of the parameters

        tolerance : float
            tolerance ratio for the change in liklihood

        max_iter : int
            maximum number of EM iterations

        Returns
        -------------
        theta_hat : list of float
            final estimate of the parameters
        
        theta_hat_history : list of list of float
            history of the theta_hat

        liklihood_history : list of float
            history of the log liklihood
        """

        self._thetas_hat = thetas

        liklihood_history = []
        thetas_history = [self._thetas_hat]

        for _ in range(max_iter):
            self.expectation_step(samples)
            self.maximization_step(samples)

            liklihood_history.append(self.liklihood(samples))
            thetas_history.append(self._thetas_hat)

            if len(liklihood_history) >= 2:
                if liklihood_history[-2] / liklihood_history[-1] <= tolerance_ratio:
                    break

        return self._thetas_hat, thetas_history, liklihood_history

    def expectation_step(self, samples):
        """Perform one expectation step of the EM algorithm

        E-step:
            Q_i(z_k) = p(x_i | z_k; theta) * prior(z_k) / 
                (\sum_k=1^K p(x_i | z_k; theta) * prior(z_k))

        Parameters
        -------------
        samples : (m, n) numpy array of int (specifically, 0s and 1s)
            samples obtained from the coin tossing experiment
        """

        # compute the conditional probability of the latent variables
        # given the samples and the current theta
        self._Qi_zk = np.stack([
            self.p_zk_cond_xi(samples[idx], self._thetas_hat,
                              self._coin_priors)
            for idx in range(samples.shape[0])
        ])

    def maximization_step(self, samples):
        """Perform one maximization step of the EM algorithm

        M-step:
            theta_k = (\sum_i=1^m \sum_j=1^n Q_ik * X_ij) / 
                (\sum_i=1^m \sum_j=1^n Q_ik)

        Parameters
        -------------
        samples : (m, n) numpy array of int (specifically, 0s and 1s)
            samples obtained from the coin tossing experiment
        """

        num_heads_in_samples = np.sum(samples, axis=1, keepdims=False)

        # find new thetas that maximize the log p_xi_zk given p_zk_cond_xi
        self._thetas_hat = np.array([
            np.dot(self._Qi_zk[:, i], num_heads_in_samples) /
            (samples.shape[1] * self._Qi_zk[:, i].sum())
            for i in range(self._num_coins)
        ])

    def liklihood(self, samples):
        """Calculate the liklihood of the observed samples given the 
        current estimated parameters

        Parameters
        -------------
        samples : (m, n) numpy array of int (specifically, 0s and 1s)
            samples obtained from the coin tossing experiment

        Returns
        -------------
        liklihood : float
            liklihood of the observed samples given the current estimated
            parameters
        """

        p_xi_z_handle = partial(self.p_xi_z, thetas=self._thetas_hat)

        return sum([
            np.dot(self._Qi_zk[i],
                   np.log(
                       np.divide(p_xi_z_handle(samples[i]), self._Qi_zk[i])))
            for i in range(samples.shape[0])
        ])

    def p_xi_z(self, sample, thetas):
        """Calculate the liklihood of the given sample under different
        coins (clusters)

        Parameters
        -------------
        sample : (n, ) numpy array of int (specifically, 0s and 1s)
            one sample (experiment) from the samples
        
        thetas : list of float
            parameters for different coins (clusters)

        Returns
        -------------
        liklihood : float
            liklihood of the given sample under different coins 
            (clusters)
        """

        return np.array([self.p_xi_zk(sample, theta) for theta in thetas])

    def p_xi_zk(self, sample, theta):
        """Calculate the liklihood of the given sample under for one
        coin (cluster)

        Parameters
        -------------
        sample : (n, ) 
            numpy array of int (specifically, 0s and 1s) one sample 
            (experiment) from the samples
        
        theta : float
            the parameter for the coin (cluster)

        Returns
        ------------- 
        liklihood : float
            liklihood of the given sample under for one coin
            (cluster)
        """

        num_heads = sample.sum()
        num_tails = sample.shape[0] - num_heads

        return reduce(lambda x, y: x * y,
                      np.power([theta, 1 - theta], [num_heads, num_tails]))

    def p_zk_cond_xi(self, xi, thetas, priors):
        """Calculate the conditiona distribution p(z_k | x_i; theta)

        Parameters
        -------------
        xi : (n, ) 
            numpy array of int (specifically, 0s and 1s) one sample 
        (experiment) from the samples

        thetas : list of float
            parameters for different coins (clusters)

        priors : list of float
            prior beliefs about the coin selection process. 
        """

        raw_prob = np.array([
            self.p_xi_zk(xi, thetas[idx]) * priors[idx]
            for idx in range(len(thetas))
        ])

        return raw_prob / raw_prob.sum()


"""
Draw <num_experiment> samples from a mixture of bernoulli distribution.
Each sample has <num_toss_per_experiment> tosses.
"""
thetas = [0.6, 0.4]

num_toss_per_experiment = 100
num_experiment = 100

# which coin to use in each experiment
coin_to_use = np.random.binomial(n=1, p=0.5, size=num_experiment)

# generate samples from a mixture of bernoulli
samples = np.stack([
    np.random.binomial(1, p=thetas[coin], size=num_toss_per_experiment)
    for coin in coin_to_use
])

# initialize estimator
estimator = CoinTossEMEstimator(2, [0.5, 0.5])

# perform EM learning
thetas_hat, thetas_hat_history, liklihood_history = estimator.estimate(
    samples, [0.0001, 0.9999], 1e-5, 10)

print("Estimated head probabilities for the two coins are {:.2f} and {:.2f}".
      format(thetas_hat[0], thetas_hat[1]))

# plot log liklihood curve
fig, axarr = plt.subplots(nrows=2, ncols=1)
axarr[0].plot(liklihood_history, label="log liklihood")
axarr[0].set_title("Log likilihood vs training iteration")
axarr[0].legend(loc="lower right")

# plot theta_hat curve
len_history = len(thetas_hat_history)
fst_coin_seq = [thetas[0]] * len_history
snd_coin_seq = [thetas[1]] * len_history

fst_theta_seq, snd_theta_seq = [list(tup) for tup in zip(*thetas_hat_history)]

axarr[1].plot(fst_coin_seq, "r", label="First coin")
axarr[1].plot(snd_coin_seq, "b", label="Second coin")
axarr[1].plot(fst_theta_seq, "g", label="First estimated coin")
axarr[1].plot(snd_theta_seq, "y", label="Second estimated coin")
axarr[1].set_title("Estimated thetas vs training iteration")
axarr[1].set_ylim(0, 1)
axarr[1].legend(loc="upper right")

plt.tight_layout()
plt.show()
