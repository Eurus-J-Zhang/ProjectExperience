#!/usr/bin/python3

from gametrees import *
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

# Next tests try the Minimax and Alpha-beta implementations.

tictactoe.show()
gamevalue(tictactoe,12)

print("CORRECT VALUE for TicTacToe: 0 (Optimally played Tic Tac Toe -> draw)")

testgrid1.show()
gamevalue(testgrid1,18)

print("CORRECT VALUE for testgrid1: -993 (Crook is always captured)")

testgrid2.show()
gamevalue(testgrid2,16)

print("CORRECT VALUE for testgrid2: -3998 (Crook is always captured)")

testgrid3.show()
gamevalue(testgrid3,18)

print("CORRECT VALUE for testgrid3: 0 (Crook can run around the obstacle indefinitely)")

testgrid4.show()
gamevalue(testgrid4,16)

print("CORRECT VALUE for testgrid4: -3998 (Crook is always captured)")
