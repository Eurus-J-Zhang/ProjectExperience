#!/usr/bin/python3

from mcs import *
from gameexamples import *

testgrid1 = PursuitState(6,4,[[ 0, 0, 0, 0, 0, 0, 0],
                              [ 0,-1, 0,-1, 0,-1, 0],
                              [ 0,-1, 0,-1, 0,-1, 0],
                              [ 1,-1, 1,-1, 1,-1, 1],
                              [ 1,-1, 1,-1, 1,-1, 1]],
                           0,0,6,0,0);

testgrid2 = PursuitState(3,3,[[ 0, 0, 0, 0],
                              [ 0, 0, 0, 0],
                              [ 0, 0, 0, 0],
                              [ 1, 0, 0, 0]],
                         0,0,3,0,0);

testgrid3 = PursuitState(3,3,[[ 0, 0, 0, 0],
                              [ 0, 0, 0, 0],
                              [ 0, 0,-1, 0],
                              [ 1, 0, 0, 0]],
                         0,0,3,0,0);

testgrid4 = PursuitState(3,3,[[ 0, 0, 0, 0],
                              [ 0,-1, 0, 0],
                              [ 0, 0, 0, 0],
                              [ 1, 0, 0, 0]],
                         0,0,3,0,0);

tictactoe = TicTacToeState();

# Next tests play the games by choosing the next actions according
# to the most promising action found by Monte Carlo Search.

print("###################### PLAY TIC TAC TOE ######################")

executeWithMC(0,tictactoe,12,5000)

print("###################### CHASE IN TEST GRID 1 ######################")
executeWithMC(0,testgrid1,20,2000)

print("###################### CHASE IN TEST GRID 2 ######################")
executeWithMC(0,testgrid2,30,3000)

print("###################### CHASE IN TEST GRID 3 ######################")
executeWithMC(0,testgrid3,30,2000)

print("###################### CHASE IN TEST GRID 4 ######################")
executeWithMC(0,testgrid4,30,2000)

# Comments:
# If both players play optimally, Tic Tac Toe ends in a draw. A basic tree
# search trivially finds the optimal moves for both players, but MCS even
# with thousands of simulations does not always yield the best moves, and
# the above simulation often ends up one player winning.
# The pursuit-escape game is played by MCS better. Only in testgrid3 can
# the crook evade capture by the police. MCS often chooses the best
# moves for the police, but not always.
