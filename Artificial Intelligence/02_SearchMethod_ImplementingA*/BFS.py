#!/usr/bin/python3

#
# Author: Jussi Rintanen, (C) Aalto University
# Only for student use on the Aalto course CS-E4800/CS-EJ4801.
# Do not redistribute.
#

#
# Functions in classes that represent state space search problems
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

# Enable debugging output

DEBUG = False
#DEBUG = True

# Breadth-First Search (uninformed)

def breadthFirstSearch(initialstate,goaltest):
    statExpansions = 0 # number of expanded states
    statVisits = 0 # number of encountered states

    starttime = time.process_time()

    if(goaltest(initialstate)):
       print("Initial state is a goal state, terminating...")
       return
    
    visited = dict() # dictionary (hash table) for holding visited states
    predecessor = dict() # dictionary (hash table) for holding predecessors
        
    Q = queue.Queue(maxsize=0) # first-in-first-out queue

    print("BFS: Initial state is " + str(initialstate))
    Q.put( (initialstate,[]) ) # Insert the initial state in the queue
    visited[initialstate] = 1
    
    while not Q.empty():
        state,path = Q.get() # Next un-expanded state from the queue
        if DEBUG:
            print("Expanding state " + str(state))
        statExpansions += 1
        for aname,s,cost in state.successors(): # Go through all successors of state
            if s not in visited: # Is state in the dictionary?
                predecessor[s] = state
                if DEBUG:
                    print("New state " + str(s))
                statVisits += 1
                if goaltest(s):
                    print("Goal state " + str(s) + " reached")
                    endtime = time.process_time()
                    print(str(statExpansions) + " expansions, " + str(statVisits) + " visits " + str(len(path + [aname])) + " actions in solution path")
                    print(path + [aname])
                    print("Elapsed time ",str(endtime-starttime))
                    print()
                    return
                visited[s] = 1
                Q.put( (s,path + [aname] ) )
    print("All states visited")

