import TestTakingMDP
import TicTacToeMDP

import time as _time
import sys

test_taking = TestTakingMDP.wrap_to_PI_MDP()
tictactoe = TicTacToeMDP.wrap_to_PI_MDP()

def solve_test_taking():
    time = _time.time()
    print(time)
    test_taking.run()
    print(_time.time())
    time = _time.time() - time
    for index in range(len(TestTakingMDP.STATES)):
        print("%s: %s" % (TestTakingMDP.STATES[index], TestTakingMDP.ACTIONS[test_taking.policy[index]]))

    print("Time: %d" % time)

    val = 0
    for i, state in enumerate(TestTakingMDP.STATES):
        print("State %s: %d" % (state, test_taking.V[i]))
        val += test_taking.V[i]

    print("Value: %d" % val)

def solve_tictactoe():
    filename = "PI_TTT_out.txt"
    sys.stdout = open(filename, 'w')
    tictactoe.run()

    print("Time: %d" % tictactoe.time)

    val = 0
    for i in range(TicTacToeMDP.STATES):
        print("State %s: %s" % (str(TicTacToeMDP.convertIndexToTuple(i)), str(tictactoe.policy[i])))
        val += tictactoe.V[i]

    print("Value: %d" % val)