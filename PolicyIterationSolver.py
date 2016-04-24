import TestTakingMDP
import TicTacToeMDP

test_taking = TestTakingMDP.wrap_to_PI_MDP()
tictactoe = TicTacToeMDP.wrap_to_PI_MDP()

def solve_test_taking():
    test_taking.run()
    for index in range(len(TestTakingMDP.STATES)):
        print("%s: %s" % (TestTakingMDP.STATES[index], TestTakingMDP.ACTIONS[test_taking.policy[index]]))

def solve_tictactoe():
    tictactoe.run()

solve_tictactoe()