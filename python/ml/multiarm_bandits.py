import numpy as np

# TODO: pull the streamlit app out to someplace else
# TODO: structure the app into packages and subpackages for better separation of concerns

class MultiArmedBandits:
    """Implement a multi-armed bandits environment

    Arms are coins and each coin has a bias (characterized) by thetas.
    The reward returned from playing an arm is either 0 or 1 following
    a bernoulli distribution parametrized by the bias. As a result, the 
    expected reward of an arm is E[bias(coin)].
    """

    def __init__(self, num_arms, thetas):
        """Initialize the environment

        Parameters
        ------------
        num_arms : int,
            number of arms (coins)

        thetas : list of float,
            bias of the arms (coins)
        """

        self._num_arms = num_arms
        self._thetas = thetas

    def __str__(self):
        return "Multi-armed Bandits Environment"

    def play_arm(self, arm):
        """Play an arm and observe rewards

        Parameters
        ------------
        arm : int,
            the arm to be played

        reward : int,
            the reward obtained by playing the arm
        """

        assert 0 <= arm < self._num_arms, "Invalid action"

        return np.random.random_sample() <= self._thetas[arm]


class ThompsonSampler:
    """Implement the thompson sampling algorithm for the multi-armed
    bandits problem where each arm is a coin. Assume a beta prior
    on the bias of the arms (coins).
    """

    def __init__(self, num_arms, num_samples, priors=None):
        """Initialize the thompson sampler

        Parameters
        ------------
        num_arms : int,
            number of arms (coins)

        num_samples : int,
            number of samples to simulated at each simulation step

        priors : list of tuple of floats,
            beta priors of the coins in the form [[a, b]] where a is
            the alpha parameter and b is the beta parameter. If not
            provided, the default value is a = b = 1
        """

        self._num_arms = num_arms
        self._k = num_samples

        # store priors for resetting
        self._priors = priors

        if priors is None:
            self._parameters = np.ones(
                self._num_arms * 2, dtype=np.int64).reshape(self._num_arms, 2)
        else:
            self._parameters = np.array(priors)

        # list of list of int, [[a, reward]]
        self._action_reward_pairs = []

        self._iteration = 0

    def __str__(self):
        return "Thompson sampling player"

    def play_arm(self):
        """Play arm by simulating k samples from each action and select
        the one that gives the highest expected reward.
        """

        if self._iteration == 0:

            self._iteration += 1

            return np.random.randint(self._num_arms)

        else:

            samples = np.stack([
                np.random.beta(a, b, size=self._k) for a, b in self._parameters
            ])
            self._iteration += 1

            return np.argmax(samples.mean(axis=1))

    def get_play_estimate(self):
        """Return the player's current estimate of the avg reward of
        plyaing an action.
        """

        return np.stack([
            np.random.beta(a, b, size=self._k) for a, b in self._parameters
        ]).mean(axis=1)

    def observe_action_reward_pair(self, action, reward):
        """Learn from experience

        Parameters
        ------------
        action : int,
            the action taken
        reward : int,
            the reward 0 or 1
        """

        self._parameters[action] += [reward, 1 - reward]

        self._action_reward_pairs.append([action, reward])

    def reset(self):
        """Re-initialize the player
        """

        self.__init__(self._num_arms, self._k, self._priors)


class OptimalPlayer:
    """The optimal player has access to the parameters of the environment.
    Knowing the biases of the coins, the optimal player always plays the arm 
    (coin) that has the highest probability of yielding a reward of 1.
    """

    def __init__(self, num_arms, thetas):
        """Initialize the optimal player with the spec of the environment

        Parameters
        ------------
        num_arms : int,
            number of arms (coins)

        thetas : list of float,
            bias of the arms (coins)
        """

        self._num_arms = num_arms
        self._thetas = thetas

        # list of list of int, [[a, reward]]
        self._action_reward_pairs = []

    def __str__(self):
        return "Optimal player"

    def play_arm(self):
        """Play the arm with highest probability of getting a reward
        of one regardless of the environment.
        """

        return np.argmax(self._thetas)

    def observe_action_reward_pair(self, action, reward):
        """Record action reward pairs

        Parameters
        ------------
        action : int,
            the action taken
        reward : int,
            the reward 0 or 1
        """

        self._action_reward_pairs.append([action, reward])

    def reset(self):
        """Re-initialize the player
        """

        self.__init__(self._num_arms, self._thetas)


class UCBPlayer:
    """Implement the upper confidence bound player for the multi-armed
    bandits problem. This player keeps track the number of times that
    an arm is played and take this into account in the decision process.
    """

    def __init__(self, num_arms):
        """Initialize the upper confidence bound player

        Parameters
        ------------
        num_arms : int,
            number of arms (coins)
        """

        self._num_arms = num_arms

        self._parameters = np.ones(
            self._num_arms * 2, dtype=np.int64).reshape(self._num_arms, 2)

        self._iteration = 0

        # list of list of int, [[a, reward]]
        self._action_reward_pairs = []

    def __str__(self):
        return "Upper confidence bound player"

    def play_arm(self):
        """Play an arm by taking into account exploitation and
        exploration bonuses
        """

        if self._iteration == 0:
            self._iteration += 1
            return np.random.randint(self._num_arms)

        else:
            exploitation_bonus = np.divide(
                self._parameters[:, 0], self._parameters.sum(axis=1))

            exploration_bonus = np.sqrt(2 * np.log(self._iteration) /
                                        (self._parameters.sum(axis=1) - 2))

            self._iteration += 1

            return np.argmax(exploitation_bonus + exploration_bonus)

    def get_play_estimate(self):
        """Return the player's current estimate of the avg reward of
        plyaing an action.
        """

        exploitation_bonus = np.divide(
            self._parameters[:, 0], self._parameters.sum(axis=1))

        exploration_bonus = np.sqrt(2 * np.log(self._iteration) /
                                    (self._parameters.sum(axis=1) - 2))

        return exploitation_bonus + exploration_bonus

    def observe_action_reward_pair(self, action, reward):
        """Learn from experience

        Parameters
        ------------
        action : int,
            the action taken
        reward : int,
            the reward 0 or 1
        """

        self._parameters[action] += [reward, 1 - reward]

        self._action_reward_pairs.append([action, reward])

    def reset(self):
        """Re-initialize the player
        """

        self.__init__(self._num_arms)


class EpsilonGreedyPlayer:
    """Implement the epsilon greedy player for the multi-armed bandits
    problem. This player plays a random arm with probability of epsilon
    and play the arm that gives the highest rewards so far otherwise.
    """

    def __init__(self, num_arms, epsilon=.1):
        """Initialize the epsilon greedy player

        Parameters
        ------------
        num_arms : int,
            number of arms (coins)
        
        epsilon : float,
            random play probability
        """

        self._num_arms = num_arms

        self._parameters = np.ones(
            self._num_arms * 2, dtype=np.int64).reshape(self._num_arms, 2)

        self._epsilon = epsilon

        # list of list of int, [[a, reward]]
        self._action_reward_pairs = []

        self._iteration = 0

    def __str__(self):
        return "Epsilon greedy player"

    def play_arm(self):
        """Play a random arm with probability epsilon and play the best
        seen arm so far
        """

        self._iteration += 1

        if self._iteration == 0 or np.random.random_sample() < self._epsilon:
            return np.random.randint(self._num_arms)

        else:

            return np.argmax(
                np.divide(
                    self._parameters[:, 0], self._parameters.sum(axis=1)))

    def observe_action_reward_pair(self, action, reward):
        """Learn from experience

        Parameters
        ------------
        action : int,
            the action taken
        reward : int,
            the reward 0 or 1
        """

        self._parameters[action] += [reward, 1 - reward]

        self._action_reward_pairs.append([action, reward])

    def reset(self):
        """Re-initialize the player
        """

        self.__init__(self._num_arms, self._epsilon)


def play_game(environment, list_of_players, n):
    """Play one game with the environment

    Parameters
    ------------
    environment : MultiArmedBandits object
        the environment that the agent will interact with
    
    list_of_players : list of Player objects
        the list of players that will interact with the environment
    
    n : int,
        number of rounds to play in each iteration
    """

    reward_history = [[]] * len(list_of_players)

    for _ in range(n):

        for idx, player in enumerate(list_of_players):
            action = player.play_arm()

            reward = environment.play_arm(action)

            player.observe_action_reward_pair(action, reward)

            # DONT USE APPEND !!!
            reward_history[idx] = reward_history[idx] + [reward]

    reward_history = np.cumsum(np.array(reward_history), axis=1)
    # Print out the avg reward estimates by the UCB and the Thompson
    # Sampling player. If the agents are really learning, the estimate
    # should rank the action similar to that of the thetas parameters
    # used by the environment
    # It would be cool to do a heat map visualization of the transition 
    # of beliefs
    print("Environment parameters: {}".format(environment._thetas))
    print("UCB estimate: {}".format(list_of_players[-2].get_play_estimate()))
    print("ThomsonSampling estimate: {}".format(
        list_of_players[-1].get_play_estimate()))

    return reward_history

