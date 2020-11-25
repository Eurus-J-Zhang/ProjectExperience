#!/usr/bin/python3

#
# Author: Jussi Rintanen, (C) Aalto University
# Only for student use on the Aalto course CS-E4800/CS-EJ4801.
# Do not redistribute.
#

# NOTE: Copy this file to 'Astar.py' before modifying.
#
# NOTE: It is recommended to only modify the block of the code
# indicated by "### Insert your code here ###"
#
# NOTE: Do not change the name of the class or the methods, as
# the automated grader relies on the names.


#
# Functions in classes representing state space search problems:
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

DEBUG=False
#DEBUG=True

# A*

def ASTAR(initialstate,goaltest,h):
    predecessor = dict() # dictionary for predecessors
    g = dict() # dictionary for holding cost-so-far






# You can base your code on BFS.py
# ASTAR has to return a pair (plan,cost)
# where
#   plan is the sequence of states on an optimal path to goals,
#   cost is the sum of the costs of actions on that path.
# You can assume the h-function to be monotone.
