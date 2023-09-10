import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from ml.multiarm_bandits import *
import streamlit as st
import pandas as pd

thetas_input = st.text_input("Biases (average action reward) of the arms (coins)", value="1,0.5,0.25,0.1")

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

num_rounds = st.number_input('Number of rounds to simulate for', min_value=1, value=100)

reward_history = play_game(environment, list_of_players, num_rounds)

df = pd.DataFrame(reward_history.transpose(), columns=list_of_players)

st.line_chart(df)