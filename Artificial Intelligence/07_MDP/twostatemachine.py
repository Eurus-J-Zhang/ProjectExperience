import mdp
from enum import Enum

class TwoStateMachine(mdp.MDP):
    """
    A very basic Markov Process with two states and two actions.
    
    It is based on a simple model of a toy walking: they toy can either be 
    upright, or prone (these are the two states). If it is upright it can
    try to walk, and if it is prone it can stand up (these are the two 
    actions).
    
    The model is described in doc/TwoStateMachine.pdf section 1.1

    """

    # Use python's Enum class to describe the available actions and states.
    # Store as class members as the actions/states are same for all instances.
    # E.g. The action 'stand' is now encoded as TwoStateMachine.Actions.stand.
    Actions = Enum("Actions", "stand walk")
    States = Enum("States", "upright prone")

    def __init__(self):
        # So few arcs in graph that they can be explicitly listed.
        # self._rewards is a dictionary mapping from a triplet of (state, action, state)
        # to a reward.
        self._rewards = {
            # Encodes the reward (0) of arc upright -> prone by action walk.
            ( TwoStateMachine.States.upright,
              TwoStateMachine.Actions.walk,
              TwoStateMachine.States.prone ) : 0,
            ( TwoStateMachine.States.upright,
              TwoStateMachine.Actions.walk,
              TwoStateMachine.States.upright ) : 20,
            ( TwoStateMachine.States.prone,
              TwoStateMachine.Actions.stand,
              TwoStateMachine.States.upright ) : 0
            # -------- TASK 1.1 ------------------------------------------------
            # TASK: Complete the dictionary by encoding the other rewards
            # described in section 1.1 of doc/TwoStateMachine.pdf by adding
            # more entries to the dictionary here.
            #
            # CODE HERE CODE HERE CODE HERE
        }

        # Likewise self._probs is a dictionary from (state,action,state) to a probability.
        self._probs = {
            ( TwoStateMachine.States.upright,
              TwoStateMachine.Actions.walk,
              TwoStateMachine.States.prone ) : 0.1,
            ( TwoStateMachine.States.upright,
              TwoStateMachine.Actions.walk,
              TwoStateMachine.States.upright ) : 0.9,
            ( TwoStateMachine.States.prone,
              TwoStateMachine.Actions.stand,
              TwoStateMachine.States.upright ) : 1
            # -------- TASK 1.2 ------------------------------------------------
            # TASK: Encode the probabilities described in section 1.1. of
            # doc/TwoStateMachine.pdf as (state, action, state) : probability
            # Structure the same as self._rewards
            #
            # CODE HERE CODE HERE CODE HERE
        }
    
    def R(self, s1, a, s2):
        """
        Get reward.
        s1,s2 are in TwoStateMachine.States
        a is in TwoStateMachine.Actions

        See doc for class MDP.
        """
        return self._rewards[(s1,a,s2)]

    def P(self, s1, a, s2):
        """
        Get probability.
        s1,s2 are in TwoStateMachine.States
        a is in TwoStateMachine.Actions

        See doc for class MDP.
        """
        return self._probs[(s1,a,s2)]

    def applicable_actions(self, s):
        """
        Get actions available in state s.
        s in TwoStateMachine.States

        See doc for class MDP.
        """
        # An action is applicable if it is possible to use it to transition from s to any
        # state in the process (including s itself). In other words, if the action
        # is associated with an arc leading out from state s.
        #
        # The applicable actions for a state can be found by going through all actions
        # a and states s2, and checking if the triplet (s,a,s2) is present in the
        # dictionary _rewards.
        aa = []
        for s2 in TwoStateMachine.States:
            for a in TwoStateMachine.Actions:
                if (s,a,s2) in self._rewards:
                    aa.append(a)
        # Note, this could also have been expressed using list comprehension as:
        # aa = [a for a in TwoStateMachine.Actions for s2 in TwoStateMachine.States if (s,a,s2) in self._rewards]
        
        return set(aa)

    def successor_states(self, s, a):
        """
        Get states reachable from state s using action a.
        s is in TwoStateMachine.States
        a is in TwoStateMachine.Actions

        See doc for class MDP.
        """
        # A successor state of s given action a is any state which can be
        # reached from s using action a.
        # In other words, a state s' in S is included if there is an arc associated
        # with action a leading from s to s'.
        ss = []
        for s2 in TwoStateMachine.States:
            if (s,a,s2) in self._rewards:
                ss.append(s2)
        # -------- TASK 1.3 ----------------------------------------------------
        # TASK: Update/populate the list ss with all successor states to state s
        # given action a. This can for instance be done by checking if (s,a,s2)
        # for any s2 exists among the rewards (or probabilities).
        #
        # CODE HERE CODE HERE CODE HERE
        
        return set(ss)

    def states(self):
        """
        Seem doc for class MDP.
        """
        return set(self.States)
    
    def analytic(self,gamma):
        """
        Compute solution using analytic formula.
        
        Possible in this case.
        NOTE: coded using assumptions on P and R.

        Parameters
        ----------
        gamma : float in ]0,1[
           Discount factor

        Returns
        -------
        dict of state : float
           Values for each state.
        """
        # Calculate values
        p11 = self._probs[(TwoStateMachine.States.upright,
                           TwoStateMachine.Actions.walk,
                           TwoStateMachine.States.upright)]
        r11 = self._rewards[(TwoStateMachine.States.upright,
                             TwoStateMachine.Actions.walk,
                             TwoStateMachine.States.upright)]
        p12 = self._probs[(TwoStateMachine.States.upright,
                           TwoStateMachine.Actions.walk,
                           TwoStateMachine.States.prone)]
        v1 = p11 * r11 / (1 - p11 * gamma - p12*gamma*gamma)
        v2 = gamma * v1
        # Create a dictionary with value in each of the two possible states.
        return {TwoStateMachine.States.upright : v1,
                TwoStateMachine.States.prone : v2}

if __name__ == "__main__":
    # Very basic example, not using value iteration. Simply creating a machine
    # and computing the analytic solution.
    # For automatic tests run test_twostatemachine.py

    tsm = TwoStateMachine()    
    print("Computing tsm.analytic(0.5)")
    va = tsm.analytic(0.5)
    print("Value of state upright: {0}".format(va[TwoStateMachine.States.upright]))
    print("Correct value: 34.285714285714285")
