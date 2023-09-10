import pandas as pd
import streamlit as st
from ml.multiarm_bandits import *
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))


st.title("Multiarm Bandits")

st.markdown("""
This app shows a simulation of different multiarm bandits algorithm for the classic problem where each arm is parametrized by a bernoulli distribution where the bias `p` is unknown and ranges from `0` to `1`. The goal of the algorithm is to maximize the expected reward by exploring different arms.
            
A simpler explanation of the setup is that we have a set of biased coins (arms), and the game is played by choosing a coin, flipping it and collecting a reward of `1` if the coin turns up as heads and `0` if the coin turns up as tails. The goal of the algorithm is to maximum the expected reward, i.e., define a policy such that the expected number of times when a head is produced is maximized. 
            
The algorithms shown are:
            
1. `OptimalPlayer`: this is an oracle player that knows ahead of time which coin has the highest probability of turning up a head. This represents the upperbound performance of any algorithm.
2. `UCBPlayer`: this player adopts the uniform confidence bound algorithm and picks the coin that has the highest estimated upper bound probability
3. `ThomsonSamplingPlayer`: this player adopts the thomson sampling algorithm and picks the coin with the highest posterior probability of turning up a head is picked
4. `EpsilonGreedyPlayer`: this player plays a random arm with probability of epsilon
    and play the arm that gives the highest rewards so far otherwise. 
""")

with st.sidebar:
    thetas_input = st.text_input(
        "Biases (average action reward) of the arms (coins)", value="1,0.5,0.25,0.1")

    num_rounds = st.number_input(
        'Number of rounds to simulate for', min_value=1, value=1000)

thetas = [float(val) for val in thetas_input.split(",")]

assert len(thetas) >= 1, "The number of arms must not be zero"
assert all(0 <= val <= 1 for val in thetas), "All biases must be between 0 and 1"

num_arms = len(thetas)

# initialize the multi-armed bandits environment
environment = MultiArmedBandits(num_arms, thetas)

# initialize the thompson sampling player with one round of simulation
thompson_sampler = ThompsonSampler(num_arms, 1)

# initialize the upper confidence bound player
ucb_player = UCBPlayer(num_arms)

# initialize the optimal player with the biases of the arms (coins)
optimal_player = OptimalPlayer(num_arms, thetas)

# initialize the greedy player with random play probability 0.1
greedy_player = EpsilonGreedyPlayer(num_arms, epsilon=.1)

list_of_players = [optimal_player, greedy_player, ucb_player, thompson_sampler]

reward_history = play_game(environment, list_of_players, num_rounds)

df = pd.DataFrame(reward_history.transpose(), columns=list_of_players)

st.line_chart(df)

st.markdown("""
From the figure above, we can see that the thomson sampling algorithm converges to the optimal policy whereas the upper confidence bound algorithm and the epsilon greedy algorithm trails behind and may not converge.
""")