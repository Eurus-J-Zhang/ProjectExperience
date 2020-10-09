#!/usr/bin/python3

import random

# Evaluate a state
# Monte Carlo search: randomly choose actions

def monteCarloTrial(player,state,stepsLeft):
  """
  Perform recursive Mote Carlo Trials, transitioning between states by randomly
  choosing among available actions.
  
  Performs at most stepsLeft moves, if stepsLeft = 0 or if there are no 
  applicable actions for `player` in `state`, it will return the state value.

  Parameters
  ----------
  player : int in {0,1}
     Current player.
  state : Object representing game state. 
     See `gameexamples.py` for examples.
  stepsLeft : int >= 0
     Maximum number of recursive levels to perform.

  Returns
  -------
  float 
     Value of final state.
  """
  if stepsLeft==0:
    return state.value()
### WRITE YOUR CODE HERE.
### Your code randomly chooses one action, executes it to obtain
### a successor state, and continues simulation recursively
### from that successor state, until there are no steps left.

def monteCarloSearch(player,state,trials):
  """
  Repeatedly perform Monte Carlo Trials and return the average value.

  Parameters
  ----------
  player : int in {0,1}
     Current player.
  state : Object representing game state. 
     See `gameexamples.py` for examples.
  trials : int > 0
     Number of Monte Carlo Trials to perform.

  Returns
  -------
  float
     Average value of the trials.

  """


  sum = 0
  for x in range(0,trials):
    sum += monteCarloTrial(player,state,20)
  return sum / trials

### TOP-LEVEL PROCEDURE FOR USING MONTE CARLO SEARCH
### The game is played by each player alternating
### with a choice of their best possible action,
### which is chosen by evaluating all possible
### actions in terms of the value of the random
### walk in the state space a.k.a. Monte Carlo Search.

def executeWithMC(player,state,stepsLeft,trials):
  """
  Recursively play a game using Mote Carlo Search printing successive states.

  Function alternates between players.

  Parameters
  ----------
  player : int in {0,1}
     Current player.
  state : Object representing game state. 
     See `gameexamples.py` for examples.
  stepsLeft : int >= 0
     Number of moves to simulate.
  trials : int > 0
     Number of Monte Carlo Trials in each sample.

  Returns
  -------
  None
  """
  
  if stepsLeft==0:
    return
  state.show()
  if player==0:
    bestScore = float("inf") # Default score for minimizing player
  else:
    bestScore = 0-float("inf") # Default score for maximizing player
  actions = state.applicableActions(player)
  if actions==[]:
    return
  for action in actions:
    state0 = state.successor(player,action)
    v = monteCarloSearch(1-player,state0,trials)
    if player==1 and v > bestScore: # Maximizing player chooses highest score
      bestAction = action
      bestScore = v
    if player==0 and v < bestScore: # Minimizing player chooses lowest score
      bestAction = action
      bestScore = v
  state2 = state.successor(player,bestAction)
  executeWithMC(1-player,state2,stepsLeft-1,trials)
