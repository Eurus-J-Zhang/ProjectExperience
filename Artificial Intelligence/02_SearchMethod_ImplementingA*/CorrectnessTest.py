#!/usr/bin/python3

#
# Author: Jussi Rintanen, (C) Aalto University
# Only for student use on the Aalto course CS-E4800/CS-EJ4801.
# Do not redistribute.
#

#
# Functions in classes representing state spaces
#   __init__    To create a state (a starting state for search)
#   __repr__    To construct a string that represents the state
#   __hash__    Hash function for states
#   __eq__      Equality for states
#   successors  Returns [(a1,s1,c1),...,(aN,sN,cN)] where each si is
#               the successor state when action called ai is taken,
#               and ci is the associated cost.
#               Here the name ai of an action is a string.

import time
import queue
import itertools

from Astar import ASTAR

# This is a simple test for the A* termination
# The first path to a goal state is not an optimal one.
# Further expansions are needed.

class TermTestState:

    def __init__(self,stateindex = 1):
        self.state = stateindex

    # Construct a string representing a state.

    def __repr__(self):
        return str(self.state)

    # The hash function for states, mapping each state to an integer

    def __hash__(self):
        return self.state

    # Equality of states.

    def __eq__(self,other):
        return (self.state == other.state)

    # queue.PriorityQueue needs an ordering of states
    
    def __lt__(self,other):
        return False

    # Compute all successors
    # 1 has 2, 3
    # 2 has 0 (the goal state)
    # 3 has 4
    # 4 has 5
    # 5 has 6
    # 6 has 0

    def successors(self):
        if self.state == 1:
            return [ ("1to2",TermTestState(2),1.0), ("1to3",TermTestState(3),1.0) ]
        elif self.state == 2:
            return [ ("2toG",TermTestState(0),5.0) ]
        elif self.state == 3:
            return [ ("3to4",TermTestState(4),0.5) ]
        elif self.state == 4:
            return [ ("4to5",TermTestState(5),0.5) ]
        elif self.state == 5:
            return [ ("5to6",TermTestState(6),0.5) ]
        elif self.state == 6:
            return [ ("6toG",TermTestState(0),0.5) ]
        elif self.state == 0:
            return []
        else:
            return []


# Create an h-function so that the path to 0 through 2
# is found first, and the optimal path (which is longer)
# is found later.

def TermTestH(s):
    if s.state == 0:
        return 0.0
    elif s.state == 1:
        return 2.0
    elif s.state == 2:
        return 1.0
    elif s.state == 3:
        return 2.0
    elif s.state == 4:
        return 1.5
    elif s.state == 5:
        return 1.0
    elif s.state == 6:
        return 0.5
    else:
        return 0.0

print("CORRECT RESULT: optimal cost is 3.0")
print("RUNTIME ESTIMATE: < 1 millisecond")
plan,cost = ASTAR(TermTestState(),
                  lambda state: (state.state == 0), # goal test
                  TermTestH) # function: distance to goal
print(plan)
