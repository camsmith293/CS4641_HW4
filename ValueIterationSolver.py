import TestTakingMDP
import TicTacToeMDP

test_taking = TestTakingMDP.wrap_to_VI_MDP()
tictactoe = TicTacToeMDP.wrap_to_VI_MDP()

def solve_test_taking():
    test_taking.run()
    for index in range(len(TestTakingMDP.STATES)):
        print("%s: %s" % (TestTakingMDP.STATES[index], TestTakingMDP.ACTIONS[test_taking.policy[index]]))

    print("Time: %d" % test_taking.time)

    val = 0
    for i, state in enumerate(TestTakingMDP.STATES):
        val += test_taking.V[i]

    print("Value: %d" % val)

def solve_tictactoe():
    tictactoe.run()

    print("Time: %d" % tictactoe.time)

    val = 0
    for i in range(TicTacToeMDP.STATES):
        val += tictactoe.V[i]

    print("Value: %d" % val)