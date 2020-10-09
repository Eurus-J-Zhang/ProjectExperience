import unittest

from twostatemachine import TwoStateMachine


class TestTSM(unittest.TestCase):

    def setUp(self):
        self.tsm = TwoStateMachine()

    def test_1_rew_prob_size(self):
        # Check that _rewards and _probs have the same size.
        self.assertEqual(len(self.tsm._probs), len(self.tsm._rewards),
                         msg = "Number of rewards must equal number of probabilities. Check TASK 1.1 and 1.2")
        
    def test_2_R(self):
        # Check that some rewards exist
        # If this fails, check your self._rewards
        # Get some values
        self.assertIn((TwoStateMachine.States.upright,
                         TwoStateMachine.Actions.walk,
                         TwoStateMachine.States.prone),
                        self.tsm._rewards,
                        msg = "Check TASK 1.1")
        
        self.assertIn((TwoStateMachine.States.prone,
                         TwoStateMachine.Actions.stand,
                         TwoStateMachine.States.upright),
                        self.tsm._rewards,
                        msg = "Check TASK 1.1")
        
        self.assertIn((TwoStateMachine.States.upright,
                         TwoStateMachine.Actions.walk,
                         TwoStateMachine.States.upright),
                        self.tsm._rewards,
                        msg = "Check TASK 1.1")
        
        
    def test_3_P(self):
        # If this fails, check your self._probs
        # Get some probabilities.
        self.assertIn((TwoStateMachine.States.prone,
                         TwoStateMachine.Actions.stand,
                         TwoStateMachine.States.upright),
                        self.tsm._probs,
                        msg = "Check TASK 1.2")
                        
        self.assertIn((TwoStateMachine.States.upright,
                         TwoStateMachine.Actions.walk,
                         TwoStateMachine.States.upright),
                        self.tsm._probs,
                        msg = "Check TASK 1.2")
        
        
        self.assertIn((TwoStateMachine.States.upright,
                         TwoStateMachine.Actions.walk,
                         TwoStateMachine.States.prone),
                        self.tsm._probs,
                        msg = "Check TASK 1.2")

            
    def test_4_illegal_arcs(self):
        # Provide a couple of illegal transitions to R and P
        # expect key errors.
        with self.assertRaises(KeyError):
            # No way of standing if you are already up
            # should fail
            self.tsm.P(TwoStateMachine.States.upright,
                       TwoStateMachine.Actions.stand,
                       TwoStateMachine.States.upright)
        with self.assertRaises(KeyError):
            # No way of staying prone by walking
            # should fail.
            self.tsm.R(TwoStateMachine.States.prone,
                       TwoStateMachine.Actions.walk,
                       TwoStateMachine.States.prone)
            
    def test_5_analytic(self):
        # Test analytic solution to a few decimal places
        # If this fails, check your self._rewards and self._probs
        gamma = 0.5
        v = self.tsm.analytic(gamma)
        # Should have two states in output.
        self.assertEqual(len(v),2)
        # Check analytic solution to four decimal digits.
        self.assertAlmostEqual(v[TwoStateMachine.States.upright], 34.2857, places=4,
                               msg = "Analytic solution not close enough to theoretical. TASK 1.1 and 1.2")


    def test_6_successor_states(self):
        # Test successor state implementation
        # Check a few 
        # If this fails, check your successor states implementation.
        ssu = self.tsm.successor_states(TwoStateMachine.States.upright,
                                        TwoStateMachine.Actions.walk)
        self.assertIn(TwoStateMachine.States.upright, ssu)
        self.assertEqual(len(ssu),2,
                         msg = "There should be exactly two successor states of upright (action walk). Check TASK 1.3")

        ssu = self.tsm.successor_states(TwoStateMachine.States.upright,
                                        TwoStateMachine.Actions.stand)
        self.assertEqual(len(ssu),0, 
                         msg = "There should be no successor states of upright (action stand). Check TASK 1.3")

        ssu = self.tsm.successor_states(TwoStateMachine.States.prone,
                                        TwoStateMachine.Actions.stand)
        self.assertIn(TwoStateMachine.States.upright,ssu)
        self.assertEqual(len(ssu),1,
                         msg = "There should be exactly one successor state of prone (action stand). Check TASK 1.3")
        
        ssu = self.tsm.successor_states(TwoStateMachine.States.prone,
                                        TwoStateMachine.Actions.walk)
        self.assertEqual(len(ssu),0,
                         msg = "There should be no successor state of prone (action walk). Check TASK 1.3")

    def test_7_applicable_actions(self):
        # Test applicable actions in a state
        # Check a few
        # If these fail, check your applicable_actions implementation.
        aa = self.tsm.applicable_actions(TwoStateMachine.States.upright)
        self.assertIn(TwoStateMachine.Actions.walk, aa)
        self.assertEqual(len(aa),1)
        
        aa = self.tsm.applicable_actions(TwoStateMachine.States.prone)
        self.assertIn(TwoStateMachine.Actions.stand, aa)
        self.assertEqual(len(aa),1)

if __name__ == "__main__":
    unittest.main()
