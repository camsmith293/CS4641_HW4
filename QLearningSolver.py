import TestTakingMDP
import TicTacToeMDP

import time as _time

test_taking = TestTakingMDP.wrap_to_QL_MDP()
tictactoe = TicTacToeMDP.wrap_to_QL_MDP()

def solve_test_taking():
    time = _time.time()
    test_taking.run()
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
    tictactoe.run()

    print("Time: %d" % tictactoe.time)

    val = 0
    for i in range(TicTacToeMDP.STATES):
        # print("State %s: %d" % (str(TicTacToeMDP.convertIndexToTuple(i)), tictactoe.V[i]))
        val += tictactoe.V[i]

    print("Value: %d" % val)