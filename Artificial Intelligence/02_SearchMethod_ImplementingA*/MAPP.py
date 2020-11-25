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

# This is Multi-Agent Path planning (MAPP) in rectangular grids

class MAPPGridState:

    # Creating a state:
    # initialLocations is a list of coordinate pairs (x,y) for all agents,
    # (xsize,ysize) is the size of the grid with cells [0..xsize-1]X[0..ysize-1],
    # walls is a list of cells (x,y) that cannot be entered.
    
    def __init__(self,initialLocations,xsize=10,ysize=10,walls = []):
        self.agents = initialLocations
        self.xsize = xsize
        self.ysize = ysize
        self.walls = walls

    # Construct a string representing a state.

    def __repr__(self):
        s = ""
        for x,y in self.agents:
            s = s + "(" + str(x) + "," + str(y) + ")"
        return s

    # The hash function for states, mapping each state to an integer

    def __hash__(self):
        h = 0
        for x,y in self.agents:
            h = h * (self.xsize * self.ysize) + x + self.xsize * y
        return h

    # Equality of states.

    def __eq__(self,other):
        return (self.agents == other.agents)

    # queue.PriorityQueue needs an ordering of states
    
    def __lt__(self,other):
        return False

    # Test if cell (x,y) can be entered: is it a wall, or outside the grid?

    def hasWallAt(self,x,y):
        if x < 0 or y < 0 or x >= self.xsize or y >= self.ysize or (x,y) in self.walls:
            return True
        else:
            return False

    # Show state of the grid in a tabular form

    def show(self):
        for y in reversed(range(0,self.ysize)):
            for x in range(0,self.xsize):
                flag = 0
                for i in range(0,len(self.agents)):
                    if x == self.agents[i][0] and y == self.agents[i][1]:
                        print(str(i+1), end='')
                        flag = 1
                if self.hasWallAt(x,y):
                    print("#", end='')
                    flag = 1
                if flag == 0:
                    print(".", end='')
            print("")
        print("")

    # Possible successor coordinates

    # One can define simultaneous moves by agents different ways
    #
    # 1. The strictest definition requires that every agent is moving to
    #    an empty cell. Transition from ...12... to ....12.. is not allowed.
    #
    # 2. A looser definition does not allow any cycles in the moves.
    #    Transition from ...12... to ....12.. is OK
    #    but transition from ...12... to ...21... is not.
    # The definition below forbids cycles involving 2 agents. But longer cycles are OK,
    # for example
    # from ..12.. to ..31..
    #      ..34..    ..42..
    # as this does not involve agents jumping over each other.
    #
    # Our agents move to the 4 cardinal directions N, S, W and E only.
    # One could of course allow also the intermediate NE, NW, SE, SW.

    # Possible moves from (x,y) (one agent), excluding those hitting walls

    def succCoords(self,ox,oy):
        candidates = [(ox,oy,"-",0.0),(ox+1,oy,"E",1.0),(ox-1,oy,"W",1.0),(ox,oy+1,"N",1.0),(ox,oy-1,"S",1.0)]
        return [ (x,y,a,c) for (x,y,a,c) in candidates if not self.hasWallAt(x,y)]

    # Compute all moves for all agents 
 ##开始看不动了

    def successors(self):
        # Does the successor correspond to a legal move?
        def samecoord(c1,c2):
            if c1[0] == c2[0] and c1[1] == c2[1]:
                return True
            return False
        def goodSuccessor(oo,aa):
            for i in range(0,len(aa)):
                for j in range(0,len(oo)):
                    if i != j and samecoord(aa[i],aa[j]):
                        return False # Double occupancy
                    if i != j and samecoord(aa[i],oo[j]) and samecoord(aa[j],oo[i]):
                        return False # Agents swapped positions
            return True
        # Pick s from triples (x,y,s) and concatenate to an action name
        def mkName(a):
            return ",".join([ s for (x,y,s,c) in a])
        # Pick (x,y) from a list of (x,y,s,c)
        def mkCoordinates(a):
            return [ (x,y) for (x,y,s,c) in a]
        # Sum of the costs of the moves by each agent
        def mkCost(a):
            return sum([ c for (x,y,s,c) in a])

        # For each agent, all possible new coordinates (list of lists of tuples)
        cc = [ self.succCoords(x,y) for (x,y) in self.agents ]

        # Form the Cartesian product, i.e. combinations of new coordinates
        ss = [ (mkName(a),mkCoordinates(list(a)),mkCost(a)) for a in itertools.product(*cc) if goodSuccessor(self.agents,list(a)) ]
        # Create a new state for each coordinate combination
        return [ (actionname,MAPPGridState(new,xsize=self.xsize,ysize=self.ysize,walls=self.walls),cost) for (actionname,new,cost) in ss ]

##结束看不动了
# Create an h-function for a goal state in MAPPGridState
# The h-estimate is the maximum of the Manhattan distances
# to goal positions for each agent.

def MAPPdistance0(goalPositions):
    def manhattan(c1,c2):
        x1,y1 = c1
        x2,y2 = c2
        return abs(x1-x2) + abs(y1-y2)
    def distance(pp1,pp2):
        h = 0
        for i in range(0,len(pp1)): # find maximum distance for an agent
            h0 = manhattan(pp1[i],pp2[i])
            if h0 > h:
                h = h0
        return h
    return (lambda state: distance(state.agents,goalPositions))

# A more informative heuristic is the sum of the Manhattan distances.

def MAPPdistance(goalPositions):
    def manhattan(c1,c2):
        x1,y1 = c1
        x2,y2 = c2
        return abs(x1-x2) + abs(y1-y2)
    def distance(pp1,pp2):
        h = 0
        for i in range(0,len(pp1)): # find maximum distance for an agent
            h = h + manhattan(pp1[i],pp2[i])
        return h
    return (lambda state: distance(state.agents,goalPositions))


# To enable A* search with more agents and in larger grid, the heuristic
# should better take into account walls and/or the interactions between
# the agents. If the grid is not too large, one could solve the optimal
# single agent path planning problem separately for every agent and all
# possible cells, and use this as a part of the heuristic instead of
# the Manhattan distance.
    
# 就是把每个♟到🏁的值加到了一起

# Create a Grid map including walls and initial locations from
# a text representation of the grid.
# ....1.
# ..2...
# ...##.
# ......
# will yield [(4,3),(2,2)] for the locations of agents 1 and 2
# and [(3,1),(4,1)] for walls.
    
# #是wall的意思

def createMAPPgrid(ss):
    xsize = len(ss[0])
    ysize = len(ss)
    maxAgent = 0

    for s in ss: # Iterate over lines
        for c in s: # Iterate over chars on one line
            if '1' <= c and c <= '9':
                maxAgent = max(maxAgent,ord(c) - ord('1') + 1)

    initlocations = [ (0,0) for x in range(0,maxAgent) ]

    walls = []
    y = ysize
    for s in ss: # Iterate over lines
        y = y-1
        x = -1
        for c in s: # Iterate over chars on one line
            x = x + 1
            if '1' <= c and c <= '9':
                initlocations[ord(c)-ord('1')] = (x,y)
            if c == '#':
                walls = walls + [(x,y)]

    return (initlocations,xsize,ysize,walls)
