#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 18 23:02:30 2020

@author: jiayizhang
"""

#!/usr/bin/python3

#
# Author: Jussi Rintanen, (C) Aalto University.
# Only for student use on the Aalto course CS-E4800/CS-EJ4801.
# Do not redistribute.
#

# NOTE: It is recommended to only modify the block of the code
# indicated by "### Insert your code here ###"
#
# NOTE 2: Do not change the name of the class or the methods, as
# the automated grader relies on the names.


# State space search problems are represented in terms of states.
# For each state there are a number of actions that are applicable in
# that state. Any of the applicable actions will produce a successor
# state for the state. To use a state space in search algorithms, we
# also need functions for producing a hash value for a state
# (the function hash) and for testing equality of two states.
#
# In this exercise (and at least one other in the next weeks), we
# will represent states as Python classes of the following form.
#
# Functions in class STATETYPE
#   __init__    To create a state (a starting state for search)
#   __repr__    To construct a string that represents the state
#   __hash__    Hash function for states
#   __eq__      Equality for states
#   successors  Returns [(a1,s1),...,(aN,sN)] where each si is
#               the successor state when action called ai is taken.
#               Here the name ai of an action is a string.

# In this exercise your task is to implement the moves of knights
# on a Chess board. The state consists of the locations of one or more
# knights. The possible moves of the knight in the cell (x,y) are
# to cells that add +1 or -1 to x and +2 or -2 to y, or that add
# +1 or -1 to y and +2 or -2 to x, and the resulting coordinates
# are within the 8 X 8 grid with coordinates 0..7 and 0..7.

# You are free to represent the state as you like. The simplest
# representation, perhaps, is as a list of triples (x,y,isblack),
# where x and y are the integer coordinates of a knight, and isblack
# is a Boolean value that is 'true' if the piece is black and 'false'
# if the piece if white.
# NOTE: This representation is part of the code template, so it reduces
#       your work load if you decide to use this representation.
# The main problem one needs to solve with this representation is
# how the functions __hash__ and __eq__ should work.
# For __hash__ and __eq__ an issue is that the lists
# [(1,1,False),(2,2,True)] and [(2,2,True),(1,1,False)]
# both represent the same state, and therefore they both have to
# map to the same hash value (otherwise they would be treated as
# two different states by whatever code uses the hash values.)
# One natural option is to always order the triples in a specific way.
# For example, order (x0,y0,b0) before (x1,y1,b1) whenever x0 < x1, or
# x0 = x1 and y0 < y1 (the lexicographic ordering.) With this ordering,
# the states are the same if and only if the lists contain the same
# elements in the same order. As there is exactly one list representing
# any given state, the problem of different hash values for different
# representations of the same state does not arise.

import time
import queue

class KnightState:

    # Construct the canonical state, with knights' coordinates
    # ordered lexicographically.
    
    def canonize(self):
        self.occupied.sort(key = lambda t: t[0]*1000+t[1])

    # Creating a state:
    # initialLocations is a list of triples (x,y,b), where
    # (x,y) is the coordinates of a knight, and b is 'true'
    # iff the knight is black.
    
    def __init__(self,initialLocations):
        self.occupied = initialLocations
        self.canonize()

    # Construct a string representing a state.

    def __repr__(self):
        s = ""
        for x,y,b in self.occupied:
            if b:
                color = "B"
            else:
                color = "W"
            s = s + "(" + str(x) + "," + str(y) + "," + color + ")"
        return s

    # The hash function for states, mapping each state to an integer

    def __hash__(self):
        h = 0
        for x,y,b in self.occupied:
            h = 2*(h * 64 + x + 8 * y)+b
        return h

    # Equality of states. Here we assume that 'canonize' has been
    # applied when creating each state.

    def __eq__(self,other):
        return (self.occupied == other.occupied)

    # All successor states w.r.t. a legal knight move

    def successors(self):
        
        
        list_for_8_choices=[(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]
        
        results=[]
        
        for knight in self.occupied:
            
            for m in list_for_8_choices:
                all_knights = self.occupied[:]
                new_knight =list(knight)
                new_knight[0]=knight[0]+m[0]
                new_knight[1]=knight[1]+m[1]
                new_knight=tuple(new_knight)
                if new_knight[0]<=7 and new_knight[1]<=7 and new_knight[0]>=0 and new_knight[1]>=0:
                    
                    validation=True
                    for n in all_knights:
                        if new_knight[0]==n[0] and new_knight[1]==n[1]:
                            validation=False
                    if validation:
                        all_knights[all_knights.index(knight)] = new_knight
                        results.append(("{} to {}".format(knight, new_knight), KnightState(all_knights)))
            
        return results
    
     
       
    


# The following is a standard breadth-first search algorithm, which
# first finds all states one step from the initial state, then all
# states two steps from the initial states, and so on.
# It is guaranteed to find the shortest sequence  of actions that
# reaches a goal state.

DEBUG = True

def breadthFirstSearch(initialstate,goaltest):
    statExpansions = 0 # number of expanded states
    statVisits = 0 # number of encountered states

    starttime = time.process_time()
    
    visited = dict() # dictionary (hash table) for holding visited states
        
    Q = queue.Queue(maxsize=0) # first-in-first-out queue for breadth-first search

    print("Initial state is " + str(initialstate))
    Q.put( (initialstate,[]) ) # Insert the initial state in the queue
    
   
    while not Q.empty():
        state,path = Q.get() # Next un-expanded state from the queue
        if DEBUG:
            print("Expanding state " + str(state))
        statExpansions += 1
        for aname,s in state.successors(): # Go through all successors of state
            if s not in visited: # Is state in the dictionary?
                if DEBUG:
                    print("New state " + str(s))
                statVisits += 1
                if goaltest(s):
                    print("Goal state " + str(s) + " reached")
                    endtime = time.process_time()
                    print(str(statExpansions) + " expansions, " + str(statVisits) + " visits")
                    print(path + [aname])
                    print("Elapsed time ",str(endtime-starttime))
                    print()
                    return
                visited[s] = 1
                Q.put( (s,path + [aname] ) )
    print("All states visited")

'''

# The following code runs the breadth-first search algorithm with
# different initial states and goal states.
# The goal states are represented by an unnamed function that
# returns 'true'if the given state is a goal state. All of
# the functions below have a unique goal state, so the test
# is simply whether the given state equals the goal state.
#
# The last two problem instances take a long time to compute,
# in the order of 1/2 hour or more. You might want to skip them.

# Swap the locations of two knights
#
# ........ ........
# ........ ........
# ........ ........
# ........ ........
# ........ ........
# ........ ........
# ........ ........
# WB...... BW......

breadthFirstSearch(KnightState([(0,0,False),(0,1,True)]),
                   lambda state: (state.occupied == [(0,0,True),(0,1,False)]))

# Move four knights in a 2 by 2 formation 2 steps diagonally
#
# ........ ........
# ........ ........
# ........ ........
# ........ ........
# ........ ..BB....
# ........ ..BB....
# BB...... ........
# BB...... ........

breadthFirstSearch(KnightState([(0,0,True),(0,1,True),(1,0,True),(1,1,True)]),
                   lambda state: (state.occupied == [(2,2,True),(2,3,True),(3,2,True),(3,3,True)]))

# Move five knights in a 3+2 formation 2 steps diagonally
#
# ........ ........
# ........ ........
# ........ ........
# ........ ........
# ........ ..BB....
# ........ ..BBB...
# BB...... ........
# BBB..... ........

print("This probably takes about 20 seconds to solve.\n")

breadthFirstSearch(KnightState([(0,0,True),(0,1,True),(0,2,True),(1,0,True),(1,1,True)]),
                   lambda state: (state.occupied == [(2,2,True),(2,3,True),(2,4,True),(3,2,True),(3,3,True)]))

# Move six knights in a 3 by 2 formation 2 steps up and 1 step right
#
# ........ ........
# ........ ........
# ........ ........
# ........ ........
# ........ .BBB....
# ........ .BBB....
# BBB..... ........
# BBB..... ........

print("This probably takes about 5 seconds to solve.\n")

breadthFirstSearch(KnightState([(0,0,True),(0,1,True),(0,2,True),(1,0,True),(1,1,True),(1,2,True)]),
                   lambda state: (state.occupied == [(2,1,True),(2,2,True),(2,3,True),(3,1,True),(3,2,True),(3,3,True)]))

# Move six knights in a 3 by 2 formation 2 steps diagonally
#
# ........ ........
# ........ ........
# ........ ........
# ........ ........
# ........ ..BBB...
# ........ ..BBB...
# BBB..... ........
# BBB..... ........

print("This probably takes about one minute to solve.\n")

breadthFirstSearch(KnightState([(0,0,True),(0,1,True),(0,2,True),(1,0,True),(1,1,True),(1,2,True)]),
                   lambda state: (state.occupied == [(2,2,True),(2,3,True),(2,4,True),(3,2,True),(3,3,True),(3,4,True)]))


# Move six knights in a 3 by 2 formation 3 steps diagonally
#
# ........ ........
# ........ ........
# ........ ........
# ........ ...BBB..
# ........ ...BBB..
# ........ ........
# BBB..... ........
# BBB..... ........

#print("This will probably take more than 40 minutes to solve.\n")
#
#breadthFirstSearch(KnightState([(0,0,True),(0,1,True),(0,2,True),(1,0,True),(1,1,True),(1,2,True)]),
#                   lambda state: (state.occupied == [(3,3,True),(3,4,True),(3,5,True),(4,3,True),(4,4,True),(4,5,True)]))

# Move nine knights in a 3 by 3 formation 2 steps up and 1 step left
#
# ........ ........
# ........ ........
# ........ ........
# ........ .BBB....
# ........ .BBB....
# BBB..... .BBB....
# BBB..... ........
# BBB..... ........

#print("This will take more than 16 hours and over 200 of GB of memory to solve.\n")
#
#breadthFirstSearch(KnightState([(0,0,True),(0,1,True),(0,2,True),(1,0,True),(1,1,True),(1,2,True),(2,0,True),(2,1,True),(2,2,True)]),
#                   lambda state: (state.occupied == [(1,2,True),(2,2,True),(3,2,True),(1,3,True),(2,3,True),(3,3,True),(1,4,True),(2,4,True),(3,4,True)]))


'''
