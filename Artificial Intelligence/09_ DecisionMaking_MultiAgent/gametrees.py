#!/usr/bin/python3

# Both the Minimax and the Alpha-beta algorithm represent the players
# as integers 0 and 1. The moves by the two players alternate 0, 1, 0, 1, ...,
# so in the recursive calls you can compute the next player as the subtraction
# 1-player.
# The minimizing player is always 0 and the maximizing 1.
# The number of recursive calls to the algorithms is kept track with
# the variable 'calls'. Let your implementation increase this variable
# by one in the beginning of each recursive call. This variable is
# also used as part of the evaluation of the implementations.

calls = 0

def minimax(player, state, depthLeft, best=None):
  """
  Perform recursive min-max search of a game tree rooted in `state`.
  
  Returns the best value in the min-max sense starting from `state` for `player`
  using at most `depthLeft`  recursive calls.

  Gives value of state if depthLeft = 0 or the state has no further actions 
  (a leaf in the game-tree).

  Parameters
  ----------
  player : int in {0,1}
     0 is the minimizing player, and 1 maximizing.
  state : Object representing game state. 
     See `gameexamples.py` for examples.
  depthLeft : int >= 0
     Maximum number of recursive levels to perform, including this this call to 
     minmax.

  Returns
  -------
  float
     Best value.

  """
  global calls
  calls += 1
  if depthLeft == 0:
    return state.value()

  if player == 0:
    best_value = float('inf')
  else:
    best_value = float('-inf')

  for action in state.applicableActions(player):
    state_2 = state.successor(player, action)
    v = minimax(1-player,state_2,depthLeft-1)
    if player == 0:
      best_value = min(best_value,v)
    else:
      best_value = max(best_value, v)

  return best_value

  ### INSERT YOUR IMPLEMENTATION OF MINIMAX HERE
  ### It should be recursively calling 'minimax'.

def alphabeta(player,state,depthLeft,alpha,beta):
  """
  Perform recursive alpha/beta search of game tree rooted in `state`.

  Returns the best value in the alpha/beta sense starting from `state` for `player`
  using at most `depthLeft`  recursive calls.

  Gives value of state if depthLeft = 0 or the state has no further actions 
  (a leaf in the game-tree).

  Parameters
  ----------
  player : int in {0,1}
     0 is the minimizing player, and 1 maximizing.
  state : Object representing game state. 
     See `gameexamples.py` for examples.
  depthLeft : int >= 0
     Maximum number of recursive levels to perform, including this call to 
     alphabeta.
  alpha : float
     Current alpha cut value.
  beta : float
     Current beta cut value.

  Returns
  -------
  float
     Best value.
 
  """
  global calls
  calls += 1
  if depthLeft == 0:
    return state.value()

  if player == 0:
    best_value = float('inf')
  else:
    best_value = float('-inf')

  for action in state.applicableActions(player):
    state_2 = state.successor(player, action)
    v = alphabeta(1-player,state_2,depthLeft-1,alpha,beta)
    if player == 0:
      best_value = min(best_value,v)
      beta = min(beta, v)
    else:
      best_value = max(best_value, v)
      alpha = max(alpha, v)
    if alpha >= beta:
      break

  return best_value

  ### INSERT YOUR IMPLEMENTATION OF ALPHABETA HERE
  ### It should be recursively calling 'alphabeta'.



def gamevalue(startingstate,depth):
  global calls
  calls = 0
  v = minimax(0,startingstate,depth)
  print(str(v) + " value with " + str(calls) + " calls with minimax to depth " + str(depth))
  calls = 0
  v = alphabeta(0,startingstate,depth,0-float("inf"),float("inf"))
  print(str(v) + " value with " + str(calls) + " calls with alphabeta to depth " + str(depth))
  calls = 0
