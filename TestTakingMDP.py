import numpy as np
from mdptoolbox import mdp

ACTIONS = ["MOVEON", "ATTEMPT", "DONE", "CHEAT"]
STATES = ["Q1U", "Q1I", "Q1C",
               "Q2U", "Q2I", "Q2C",
               "Q3U", "Q3I", "Q3C",
               "Q4U", "Q4I", "Q4C",
               "Q5U", "Q5I", "Q5C",
               "CHEATING", "Q6U"]


def transition_model(state, action):
    state_prime = state

    question_num = int(state[1])
    next_question_num = question_num + 1

    if action == "DONE":
        state_prime = "Q6U"

    elif state.endswith("U"):
        if action == "MOVEON":
            state_prime = "Q%dU" % next_question_num
        if action == "CHEAT":
            outcomes = ["CHEATING", "Q%dC" % question_num, "Q%dI" % question_num]
            state_prime = np.random.choice(outcomes, p=[0.2, 0.4, 0.4])
        if action == "ATTEMPT":
            outcomes = ["Q%dC" % question_num, "Q%dI" % question_num]
            state_prime = np.random.choice(outcomes, p=[0.8**question_num, 1-0.8**question_num])

    elif state.endswith("I"):
        if action == "MOVEON":
            state_prime = "Q%dU" % next_question_num
        if action == "CHEAT":
            outcomes = ["CHEATING", "Q%dC" % question_num, "Q%dI" % question_num]
            state_prime = np.random.choice(outcomes, p=[0.2, 0.3, 0.5])
        if action == "ATTEMPT":
            outcomes = ["Q%dC" % question_num, "Q%dI" % question_num]
            state_prime = np.random.choice(outcomes, p=[0.8**question_num, 1-0.8**question_num])

    elif state.endswith("C"):
        if action == "MOVEON":
            state_prime = "Q%dU" % next_question_num
        if action == "CHEAT":
            outcomes = ["CHEATING", "Q%dC" % question_num, "Q%dI" % question_num]
            state_prime = np.random.choice(outcomes, p=[0.2, 0.5, 0.3])
        if action == "ATTEMPT":
            outcomes = ["Q%dC" % question_num, "Q%dI" % question_num]
            state_prime = np.random.choice(outcomes, p=[0.8**question_num, 1-0.8**question_num])

    elif state == "CHEATING":
        state_prime = "CHEATING"

    else:
        state_prime = "Q6U"

    return state_prime

def reward_model(state):
    reward = 0.0

    if state.endswith("U"):
        reward = -0.02
        if state == "Q6U":
            reward = 0.04

    elif state.endswith("I"):
        reward = -0.5

    elif state.endswith("C"):
        question_num = int(state[1])
        reward = 1.0 * question_num

    elif state == "CHEATING":
        reward = -10.0

    else:
        reward = 1.0

    return reward

def P(state_prime, state, action):
    if state == "CHEATING":
        if state_prime == "CHEATING": return 1.0
        return 0.0

    elif state == "Q6U":
        if state_prime == "Q6U": return 1.0
        return 0.0

    if action == "DONE":
        if state_prime == "Q6U": return 1.0
        return 0.0

    question_num = int(state[1])
    next_question_num = question_num + 1

    if state.endswith("U"):
        if action == "MOVEON":
            if state_prime == "Q%dU" % next_question_num: return 1.0
            return 0.0

        if action == "CHEAT":
            if state_prime == "CHEATING": return 0.1
            if state_prime == "Q%dC" % question_num: return 0.45
            if state_prime == "Q%dI" % question_num: return 0.45
            return  0.0

        if action == "ATTEMPT":
            if state_prime == "Q%dC" % question_num: return 0.8**question_num
            if state_prime == "Q%dI" % question_num: return 1 - 0.8**question_num
            return  0.0

    elif state.endswith("I"):
        if action == "MOVEON":
            if state_prime == "Q%dU" % next_question_num: return 1.0
            return 0.0

        if action == "CHEAT":
            if state_prime == "CHEATING": return 0.2
            if state_prime == "Q%dC" % question_num: return 0.3
            if state_prime == "Q%dI" % question_num: return 0.5
            return  0.0

        if action == "ATTEMPT":
            if state_prime == "Q%dC" % question_num: return 0.8**question_num
            if state_prime == "Q%dI" % question_num: return 1 - 0.8**question_num
            return  0.0

    elif state.endswith("C"):
        if action == "MOVEON":
            if state_prime == "Q%dU" % next_question_num: return 1.0
            return 0.0

        if action == "CHEAT":
            if state_prime == "CHEATING": return 0.2
            if state_prime == "Q%dC" % question_num: return 0.5
            if state_prime == "Q%dI" % question_num: return 0.3
            return  0.0

        if action == "ATTEMPT":
            if state_prime == "Q%dC" % question_num: return 0.8**question_num
            if state_prime == "Q%dI" % question_num: return 1 - 0.8**question_num
            return  0.0


def build_transition_matrix():
    transitions = np.zeros((len(ACTIONS), len(STATES), len(STATES)), dtype=np.float64)

    for index in np.ndindex((transitions.shape)):
        a = ACTIONS[index[0]]
        s = STATES[index[1]]
        s_prime = STATES[index[2]]
        transitions[(index[0],index[1],index[2])] = float(P(s_prime, s, a))

    return transitions

def build_reward_matrix():
    rewards = np.zeros((len(STATES), len(ACTIONS)), dtype=np.float64)

    for index in np.ndindex((rewards.shape)):
        s = STATES[index[0]]
        a = ACTIONS[index[1]]
        reward = float(reward_model(s))

        if ((s[2] == "C")) and ((a == "ATTEMPT") or (a == "CHEAT")):
            reward -= 0.6/float(s[1])

        rewards[(index[0],index[1])] = reward

    return rewards

def wrap_to_PI_MDP():
    transitions = build_transition_matrix()
    rewards = build_reward_matrix()
    wrapped = mdp.PolicyIteration(transitions, rewards, discount=0.1, max_iter=10000,
                                  policy0=np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]))
    wrapped.verbose = True
    return wrapped

def wrap_to_VI_MDP():
    transitions = build_transition_matrix()
    rewards = build_reward_matrix()
    wrapped = mdp.ValueIteration(transitions, rewards, discount=0.1, epsilon=0.05, max_iter=10000)
    wrapped.verbose = True
    return wrapped

def wrap_to_QL_MDP():
    transitions = build_transition_matrix()
    rewards = build_reward_matrix()
    wrapped = mdp.QLearning(transitions, rewards, discount=0.1)
    wrapped.verbose = True
    return wrapped