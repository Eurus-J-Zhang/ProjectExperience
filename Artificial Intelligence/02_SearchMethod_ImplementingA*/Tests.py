#!/usr/bin/python3

#
# Author: Jussi Rintanen, (C) Aalto University.
# Only for student use on the Aalto course CS-E4800/CS-EJ4801.
# Do not redistribute.
#

import time
import queue
import itertools

from MAPP import MAPPGridState, MAPPdistance, MAPPdistance0, createMAPPgrid
from BFS import breadthFirstSearch
from Astar import ASTAR

grid3I= ["........",
         "........",
         "........",
         "........",
         "........",
         "32......",
         "14......"]

grid3G= ["........",
         "........",
         "........",
         "..31....",
         "..24....",
         "........",
         "........"]

#plan,cost = breadthFirstSearch(MAPPGridState(init3,xsize=xs3,ysize=ys3,walls=w3),
#                               lambda state: (state.agents == goal3))
print("CORRECT RESULT: optimal cost is 16.0")
print("RUNTIME ESTIMATE: < 5 seconds")
init3,xs3,ys3,w3 = createMAPPgrid(grid3I)
goal3,xs3,ys3,w3 = createMAPPgrid(grid3G)
plan,cost = ASTAR(MAPPGridState(init3,xsize=xs3,ysize=ys3,walls=w3),
                  lambda state: (state.agents == goal3), # goal test
                  MAPPdistance(goal3)) # function: distance to goal
for s in plan:
    s.show()
    
print(cost)

grid1I= ["...#.........",
         "...#.........",
         "...#.........",
         "...########..",
         "..12......34.",
         "...###..###..",
         "...######....",
         "........#....",
         "........#...."]

grid1G= ["...#.........",
         "...#.........",
         "...#.........",
         "...########..",
         "...34.....21.",
         "...###..###..",
         "...######....",
         "........#....",
         "........#...."]

print("CORRECT RESULT: optimal cost is 34.0")
print("RUNTIME ESTIMATE: < 15 seconds")
init1,xs1,ys1,w1 = createMAPPgrid(grid1I)
goal1,xs1,ys1,w1 = createMAPPgrid(grid1G)
plan,cost = ASTAR(MAPPGridState(init1,xsize=xs1,ysize=ys1,walls=w1),
                  lambda state: (state.agents == goal1), # goal test
                  MAPPdistance(goal1)) # function: distance to goal
for s in plan:
    s.show()

print(cost)

grid0I= ["...........",
         "...........",
         "..12.......",
         "..34.......",
         "...........",
         "...........",
         "..........."]

grid0G= ["...........",
         "...........",
         "...........",
         "...........",
         "...........",
         "........12.",
         "........34"]

print("CORRECT RESULT: optimal cost is 36.0")
print("RUNTIME ESTIMATE: < 40 seconds")
init0,xs0,ys0,w0 = createMAPPgrid(grid0I)
goal0,xs0,ys0,w0 = createMAPPgrid(grid0G)
plan,cost = ASTAR(MAPPGridState(init0,xsize=xs0,ysize=ys0,walls=w0),
                  lambda state: (state.agents == goal0), # goal test
                  MAPPdistance(goal0)) # function: distance to goal
for s in plan:
    s.show()


print(cost)

grid2I= ["..1#....",
         "..2#....",
         "........",
         "...#3...",
         "...#4...",
         "...#...."]

grid2G= ["...#1...",
         "...#2...",
         "........",
         "..3#....",
         "..4#....",
         "...#...."]
init2,xs,ys,w = createMAPPgrid(grid1I)
goal2,xs,ys,w = createMAPPgrid(grid1G)

print("CORRECT RESULT: optimal cost is 24.0")
print("RUNTIME ESTIMATE: < 5 minutes")
init2,xs2,ys2,w2 = createMAPPgrid(grid2I)
goal2,xs2,ys2,w2 = createMAPPgrid(grid2G)
plan,cost = ASTAR(MAPPGridState(init2,xsize=xs2,ysize=ys2,walls=w2),
                  lambda state: (state.agents == goal2), # goal test
                  MAPPdistance(goal2)) # function: distance to goal
for s in plan:
    s.show()
