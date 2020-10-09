#!/usr/bin/python3

# The MDPs consists of a range of integers 0..stateMax which represent
# the states of the MDP, a set of actions. The rewards and transition
# probabilities are accessed with some of the functions below defined
# for the Python classes that represent MDPs.
#
#  - The __init__ constructor builds the state of the MDP, possibly
#       with additional configuration options.
#  - applicableActions(state) returns all actions possible in a state.
#  - successors(state,action) returns the information about possible
#    successor state of a state. It is a triple (s,p,r) where
#           - s is a successor state,
#           - p is the probability of reaching s from state, and
#           - r is the reward/cost when going from state to s.
#  - stateMax is the maximum state index. The minimum is 0.
#  - show() visualizes the MDP in whatever way it can be visualized.

# The example MDP class provided for this exercise is a grid navigation
# problem, in which an agent can move to the four cardinal directions
# in a finite rectangular grid.
#    The move actions are nondeterministic: with 0.8 probability the move
# is to the nominal direction (N,S,E,W), but with 0.1+0.1 probabilities
# the move is to one of the direction 90 degrees off the nominal direction.
# So, when trying to move North, with probability 0.8 the move actually
# is to North, but it will be to the East with probability 0.1 and to
# the West with probability 0.1.
#    Grid cells are associated with rewards/costs, obtained when reaching
# the cell. 99 is a special number in the grid cell which indicates that
# the cell cannot be entered. Moves to these 99 cells or against the outside
# wall of the grid will result in the agent not moving anywhere.
#    The example MDP has a 'teleport' feature which may be turned on when
# creating the MDP: all moves from the NE corner will lead to the SW corner.

class GridMDP:
  def __init__(self,xs,ys,cells,teleport=False):
    self.xSize = xs		# number of columns
    self.ySize = ys		# number of rows
    self.stateMax = xs*ys-1	# index of last (SE corner) cell
    self.grid = cells		# List for rewards/costs of all cells
    self.teleport = teleport

  NORTH = 1
  SOUTH = 2
  WEST = 3
  EAST = 4
  ACTIONS = [NORTH,SOUTH,WEST,EAST]

  def turnleft(self,a):
    if a==self.NORTH:
      return self.WEST
    elif a==self.WEST:
      return self.SOUTH
    elif a==self.SOUTH:
      return self.EAST
    else:
      return self.NORTH

  def turnright(self,a):
    if a==self.NORTH:
      return self.EAST
    elif a==self.EAST:
      return self.SOUTH
    elif a==self.SOUTH:
      return self.WEST
    else:
      return self.NORTH

  def actionName(self,a):
    if a==self.NORTH:
      return "N"
    elif a==self.SOUTH:
      return "S"
    elif a==self.EAST:
      return "E"
    else:
      return "W"

  def possible(self,action,state):
    if self.grid[state] == 99:
        return False
    else: 
        return True

  def applicableActions(self,state):
      return [x for x in self.ACTIONS if self.possible(x,state)]

  # For every state and action, compute list of (state',P,R)
  # where state' is a successor of state
  #       P is the probability of reaching state'
  #       R is the reward obtained when reaching state'
  # Triples with the same state' will be merged.
  # The sum of the probabilities P is always 1.

  def addmove(self,state,direction,prob,dict):
    if direction==self.NORTH and state >= self.xSize and self.grid[state-self.xSize] != 99:
      state2 = state-self.xSize
    elif direction==self.SOUTH and state <= self.stateMax-self.xSize and self.grid[state+self.xSize] != 99:
      state2 = state+self.xSize
    elif direction==self.EAST and (state+1) % self.xSize > 0 and self.grid[state+1] != 99:
      state2 = state+1
    elif direction==self.WEST and state % self.xSize > 0 and self.grid[state-1] != 99:
      state2 = state-1
    else:
      state2 = state
    if self.teleport and state == self.xSize-1: # Teleport from the NE corner
      state2 = self.stateMax-self.xSize+1 # to the SW corner
    reward = self.grid[state2]
    if state2 in dict:
        tmp = dict[state2]
        dict[state2] = (tmp[0]+prob,reward) # Sum the probabilities when merging.
    else:
        dict[state2] = (prob,reward)

  # Compute all successor state of state, with their probabilities and rewards
  def successors(self,state,action):
    dict = {}
    self.addmove(state,self.turnleft(action),0.1,dict),
    self.addmove(state,self.turnright(action),0.1,dict),
    self.addmove(state,action,0.8,dict)
    succlist = []
    for state2,value in dict.items():
        tmp = (state2,value[0],value[1])
        succlist.append(tmp)
    return succlist

  # Show the rewards of all grid cells

  def show(self):
    print("--------------------")
    for y in range(0,self.ySize):
      for x in range(0,self.xSize):
        i = y*self.xSize+x
        if self.grid[i] == 99: # wall cell inside the grid
          print("##", end="")
        elif self.grid[i] == 0: # 0 reward cells shown as .
          print(" .", end="")
        else:
          print("%2d" % (self.grid[i]), end="")
      print("")

  # Show the policy/plan for a grid MDP
  # MDP policies represented as dictionaries with the state
  # indices 0..stateMax as the dictionary keys, and the actions
  # as the values.

  def showPolicy(self,policy):
    print("--------------------")
    for y in range(0,self.ySize):
      for x in range(0,self.xSize):
        i = y*self.xSize+x
        if self.grid[i] == 99:
          print("#", end="")
        else:
          print(self.actionName(policy[i]),end="")
      print("")

  def showValues(self,V):
    print("--------------------")
    for y in range(0,self.ySize):
      for x in range(0,self.xSize):
        i = y*self.xSize+x
        print(" %3.3f" % V[i], end='')
      print("")

