from mdptoolbox import mdp
import mdptoolbox.examples.tictactoe

def wrap_to_PI_MDP():
    transitions, rewards = mdptoolbox.examples.tictactoe.getTransitionAndRewardArrays()
    wrapped = mdp.PolicyIteration(transitions, rewards, discount=0.1, max_iter=10000)
    wrapped.verbose = True
    return wrapped

def wrap_to_VI_MDP():
    transitions, rewards = mdptoolbox.examples.tictactoe.getTransitionAndRewardArrays()
    wrapped = mdp.ValueIteration(transitions, rewards, discount=0.1, max_iter=10000)
    wrapped.verbose = True
    return wrapped