import unittest

from valueiteration import *
from twostatemachine import TwoStateMachine
from gridmdp import GridMDP


class TestValueIterationsGMP(unittest.TestCase):
    """
    Tests using GridMDP.
    """

    def test_1_value_of_return(self):
        # Check value of returns something
        # Make grid with no walls and no rewards.
        gdp = GridMDP(["...",
                       "...",
                       "..."])
        # Just pick one state and action
        a = list(gdp._actions)[0]
        s = (0,0)
        # Let the values for all states be 0
        v = {s2 : 0 for s2 in gdp.states()}
        val = value_of(gdp, s, a, v, 0.5)
        # Check that it isn't None
        self.assertIsNotNone(val, msg = "Check that value_of returns a value (TASK 2.1)")
        # It needs to return a float. In this particular case it should be 0 as there are no values.
        self.assertEqual(val, 0, msg = "Check (TASK 2.1)")

    def test_2_valueiteration_return(self):
        # Check so value iteration returns a dictionary.
        gdp = GridMDP([".+.",
                       "-.#",
                       "#.."])
        gamma = 0.8
        epsilon = 0.01
        v = value_iteration(gdp, gamma, epsilon)
        # If value_iteration has not been implemented the return value is None.        
        self.assertIsNotNone(v, msg = "Check if value_iteration returns a value (TASK 2.2)")
        # It needs to return a dictionary.
        self.assertIsInstance(v, dict, msg = "value_iteration needs to return a dictionary (TASK 2.2)")
        
    def test_3_GridMDP_1(self):
        """ 
        Test based on GridMDP.
        """
        
        gdp = GridMDP([".+.",
                       "-.#",
                       "#.."])
        
        gamma = 0.8
        epsilon = 0.01
        v = value_iteration(gdp, gamma, epsilon)
        self.assertIsNotNone(v, msg = "Check if value_iteration returns a value.")
        # It needs to return a dictionary.
        self.assertIsInstance(v, dict, msg = "value_iteration needs to return a dictionary")
        # Correct values
        v_correct = {(0, 1): 1.8238205241911116,
                     (2, 1): 2.29341219866735,
                     (0, 0): 2.166637350797169,
                     (1, 1): 2.1666373507971692,
                     (0, 2): 2.29341219866735,
                     (2, 2): 1.7940038893976213,
                     (1, 0): 1.5860931388905264}
        
        for s in v:
            self.assertAlmostEqual(v[s],v_correct[s],
                                   msg="Values differ for GridMDP example 1. Check value_iteration and value_of")
            
    def test_4_GridMDP_2(self):
        """ 
        Test based on GridMDP.
        """
        
        gdp = GridMDP(["...+",
                       ".#.-",
                       "...."])
        gamma = 0.8
        epsilon = 0.01
        v = value_iteration(gdp, gamma, epsilon)
        # If value_iteration has not been implemented the return value is None.        
        self.assertIsNotNone(v, msg = "Check if value_iteration returns a value.")
        # It needs to return a dictionary.
        self.assertIsInstance(v, dict, msg = "value_iteration needs to return a dictionary")
        # Correct values
        v_correct = {(0, 1): 1.6360669646671202,
                     (1, 2): 1.601186507019843,
                     (2, 1): 1.329565025014288,
                     (0, 0): 2.1870595721840265,
                     (0, 3): 1.7541002681521682,
                     (2, 0): 1.7072985613492146,
                     (2, 3): 2.195548536530376,
                     (0, 2): 2.1870595721840265,
                     (2, 2): 1.7072985613492149,
                     (1, 0): 1.601186507019843,
                     (1, 3): 2.1785706078376768}
        for s in v:
            self.assertAlmostEqual(v[s],v_correct[s],
                                   msg="Values differ for GridMDP example 2. Check value_iteration and value_of")
        
    def test_5_GridMDP_3(self):
        """ 
        Test based on GridMDP.
        """
        gdp = GridMDP([".......",
                       ".......",
                       "..-+*..",
                       ".......",
                       "......."],
                tile_rewards = {'-':-1,'+':2,'*':-9})
        gamma = 0.5
        epsilon = 0.01
        v = value_iteration(gdp, gamma, epsilon)
        # If value_iteration has not been implemented the return value is None.
        self.assertIsNotNone(v, msg = "Check if value_iteration returns a value.")
        # It needs to return a dictionary.
        self.assertIsInstance(v, dict, msg = "value_iteration needs to return a dictionary")
        # Correct values
        v_correct = {(0, 0): 0.06923166565000002,
                     (0, 1): 0.15219732941875,
                     (0, 2): 0.3263233622117188,
                     (0, 3): 0.6949951367398438,
                     (0, 4): 0.3023821894531251,
                     (0, 5): 0.13224802740000002,
                     (0, 6): 0.05748010718750003,
                     (1, 0): 0.11720394525625003,
                     (1, 1): 0.27672302730000004,
                     (1, 2): 0.6639185143695313,
                     (1, 3): 1.65763275834375,
                     (1, 4): 0.20867435252734376,
                     (1, 5): 0.08997256726250003,
                     (1, 6): 0.04989554753750002,
                     (2, 0): 0.05178080005000003,
                     (2, 1): 0.09780469322343754,
                     (2, 2): 1.6803751711750001,
                     (2, 3): 0.038477230092187675,
                     (2, 4): 1.6348903455125,
                     (2, 5): 0.018513058725000007,
                     (2, 6): 0.02613983570000001,
                     (3, 0): 0.11720394525625003,
                     (3, 1): 0.27672302730000004,
                     (3, 2): 0.6639185143695313,
                     (3, 3): 1.65763275834375,
                     (3, 4): 0.2086743525273438,
                     (3, 5): 0.08997256726250003,
                     (3, 6): 0.04989554753750002,
                     (4, 0): 0.06923166565000002,
                     (4, 1): 0.15219732941875,
                     (4, 2): 0.3263233622117188,
                     (4, 3): 0.6949951367398438,
                     (4, 4): 0.30238218945312506,
                     (4, 5): 0.13224802740000002,
                     (4, 6): 0.05748010718750003}
        for s in v:
            self.assertAlmostEqual(v[s],v_correct[s],
                                   msg="Values differ for GridMDP example 3. Check value_iteration and value_of")
            
                          
        
class TestValueIterationsTSM(unittest.TestCase):
    """
    Tests using the TwoStateMachine
    NOTE: IF these fail, check that test_twostatemachine.py passes all tests first.
    """
    def setUp(self):
        self.tsm = TwoStateMachine()

    def test_TSM_value_of(self):
        """
        This function uses TwoStateMachine to test different aspects
        of valueiteration.py 
        Note: Assumes a correct implementation of TwoStateMachine.
        """
        gamma = 0.5
        # Call one step of value_of using some dummy values
        x = value_of(self.tsm, TwoStateMachine.States.upright,
                     TwoStateMachine.Actions.walk,
                     {TwoStateMachine.States.upright : 0,
                      TwoStateMachine.States.prone : 0},
                     gamma)

        # If value_of is not implemented it will return None
        self.assertIsNotNone(x, msg = "Check TASKs 1.x and 2.1.")
        # Compare with correct value.
        self.assertAlmostEqual(x, 18.0, places = 4,
                               msg = "Check TASKs 1.x and 2.1.")
        
    def test_TSM_valueiteration(self):
        """
        This function uses TwoStateMachine to test different aspects
        of valueiteration.py 
        Note: Assumes a correct implementation of TwoStateMachine.
        """
        gamma = 0.5
        epsilon = 0.01
        # Call value_iteration
        vi = value_iteration(self.tsm, gamma, epsilon)
        # If value_iteration has not been implemented the return value is None.
        self.assertIsNotNone(vi, msg = "Check TASKS 1.x and 2.2.")
        # It needs to return a dictionary.
        self.assertIsInstance(vi, dict, msg = "Check TASKs 1.x and 2.2")

        # Compute the analytic solution and compare values.
        va = self.tsm.analytic(gamma)
        
        # Analytic and value iteration algorithm close enough?
        self.assertAlmostEqual(vi[TwoStateMachine.States.upright],
                               va[TwoStateMachine.States.upright],
                               places=2,
                               msg = "TwoStateMachine value_iteration and analytic differs substantially.")
        self.assertAlmostEqual(vi[TwoStateMachine.States.prone],
                               va[TwoStateMachine.States.prone],
                               places=2,
                               msg = "TwoStateMachine value_iteration and analytic differs substantially.")
        
        # Make and test policy. Doesn't make much sense for
        # the TSM as it only has one action. 
        pi = make_policy(self.tsm, vi, gamma)
        # Policy when standing is to walk
        self.assertEqual(pi[TwoStateMachine.States.upright],
        TwoStateMachine.Actions.walk,
                         msg = "Wrong policy for TwoStateMachine.")
        # Policy when prone is to stand
        self.assertEqual(pi[TwoStateMachine.States.prone],
                         TwoStateMachine.Actions.stand,
                         msg = "Wrong policy for TwoStateMachine.")


            

if __name__ == "__main__":
    unittest.main()
