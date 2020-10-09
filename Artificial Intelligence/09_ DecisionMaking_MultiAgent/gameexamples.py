#!/usr/bin/python3

import sys
write = sys.stdout.write

# The games are defined in terms of a 'state' class, which represents
# the possible states of the game.
# The __init__ constructor builds the state of the game, possibly
#   with additional configuration options.
# applicableActions(player) returns all actions possible in the state
#   for the given player.
# successor(player,action) returns the successor state of a state
#   with respect to the tiven player taking the given action.
# show() visualizes the state of the game textually.
# value() returns the numeric value of the state, with small values
#   good for player 0 and big values good for player 1.
#
# The game representation assumes that the players are 0 and 1.

# The game of tic tac toe in a 3 by 3 grid
# grid is represented as a list
# [ , , ,
#   , , ,
#   , ,  ]
# where -1 denotes that the cell is empty, 0 denotes piece placed
# by player 0, and denotes piece placed by player 1.

class TicTacToeState:
  def __init__(self,cs = [-1,-1,-1,-1,-1,-1,-1,-1,-1]):
    self.cells=cs

  def applicableActions(self,player):
    if self.value() == 0:
      return [i for i in range(0,9) if self.cells[i]==-1]
    else:
      return []

  def successor(self,player,action):
    if self.cells[action] == -1:
      return TicTacToeState(self.cells[0:action] + [player] + self.cells[action+1:])
    else:
      return self

  def showLine(self,l):
    for e in l:
      if e==-1:
        write(".")
      else:
        write(str(e))
    print("")
  
  def show(self):
    print("===")
    self.showLine(self.cells[0:3])
    self.showLine(self.cells[3:6])
    self.showLine(self.cells[6:9])

  # The values of final states are
  # -1 : player 1 loses
  #  0 : game not finished, or draw
  #  1 : player 1 wins

  def value(self):
    # rows 0
    if self.cells[0:3] == [0,0,0] or self.cells[3:6] == [0,0,0] or self.cells[6:9] == [0,0,0]:
      return -1
    # rows 1
    if self.cells[0:3] == [1,1,1] or self.cells[3:6] == [1,1,1] or self.cells[6:9] == [1,1,1]:
      return 1
    # 0 columns
    if self.cells[0]==0 and self.cells[3]==0 and self.cells[6]==0:
      return -1
    if self.cells[1]==0 and self.cells[4]==0 and self.cells[7]==0:
      return -1
    if self.cells[2]==0 and self.cells[5]==0 and self.cells[8]==0:
      return -1
    # 1 columns
    if self.cells[0]==1 and self.cells[3]==1 and self.cells[6]==1:
      return 1
    if self.cells[1]==1 and self.cells[4]==1 and self.cells[7]==1:
      return 1
    if self.cells[2]==1 and self.cells[5]==1 and self.cells[8]==1:
      return 1
    # 0 diagonals
    if self.cells[0]==0 and self.cells[4]==0 and self.cells[8]==0:
      return -1
    if self.cells[2]==0 and self.cells[4]==0 and self.cells[6]==0:
      return -1
    # 1 diagonals
    if self.cells[0]==1 and self.cells[4]==1 and self.cells[8]==1:
      return 1
    if self.cells[2]==1 and self.cells[4]==1 and self.cells[6]==1:
      return 1
    return 0

# Pursuit Evasion game
# The Police chase a Crook in a grid. Some squares yield a reward of 1
# to the Crook, and the Police capturing the Crook (entering the same
# grid cell) imposes a penalty of 1000 (a reward of -1000) to the Crook.

# components of a grid
# xMax: maximum x-coordinate of range 0..xMax
# yMax: maximum y-coordinate of range 0..yMax
# list of lists of grid cells with
#   -1 denoting a cell that cannot be entered (wall)
#    n denoting reward n for player 1
# x0,y0,x1,y1: initial locations for player 0 (police) and player 1 (crook)

class PursuitState:
  def __init__(self,xm,ym,cells,x0,y0,x1,y1,rewards):
    self.xMax = xm
    self.yMax = ym
    self.grid = cells
    self.x0 = x0
    self.y0 = y0
    self.x1 = x1
    self.y1 = y1
    self.rewards = rewards

  NORTH = 1
  SOUTH = 2
  WEST = 3
  EAST = 4
  ACTIONS = [NORTH,SOUTH,WEST,EAST]

  def showAction(self,a):
    if a==self.NORTH:
      write("NORTH")
    elif a==self.SOUTH:
      write("SOUTH")
    elif a==self.EAST:
      write("EAST")
    else:
      write("WEST")

  def possible(self,player,action):
    if player==0:
      x=self.x0
      y=self.y0
    else:
      x=self.x1
      y=self.y1
    if action==self.NORTH and y==0:
      return False
    if action==self.SOUTH and y==self.yMax:
      return False
    if action==self.WEST and x==0:
      return False
    if action==self.EAST and x==self.xMax:
      return False
    if action==self.NORTH:
      y -= 1
    if action==self.SOUTH:
      y += 1
    if action==self.WEST:
      x -= 1
    if action==self.EAST:
      x += 1
    if self.grid[y][x] == -1:
      return False
    return True

  def applicableActions(self,player):
    return [x for x in self.ACTIONS if self.possible(player,x)]

  def successor(self,player,action):
    if player==0:
      x=self.x0
      y=self.y0
    else:
      x=self.x1
      y=self.y1
    if action==self.NORTH and y==0:
       return self
    if action==self.SOUTH and y==self.yMax:
       return self
    if action==self.WEST and x==0:
       return self
    if action==self.EAST and x==self.xMax:
       return self
    if action==self.NORTH:
       y -= 1
    if action==self.SOUTH:
       y += 1
    if action==self.WEST:
       x -= 1
    if action==self.EAST:
       x += 1
    if self.grid[y][x] == -1:
      return self
    newrewards = self.rewards
    if player==0:
      if(x==self.x1 and y==self.y1):
        newrewards -= 1000
      return PursuitState(self.xMax,self.yMax,self.grid,x,y,self.x1,self.y1,newrewards)
    else:
      if(self.x0==x and self.y0==y):
        newrewards -= 1000
      newrewards += self.grid[y][x]
      return PursuitState(self.xMax,self.yMax,self.grid,self.x0,self.y0,x,y,newrewards)

  def value(self):
    return self.rewards

  def show(self):
    print("--------------------")
    print("Crook score: " + str(self.rewards))
    for y in range(0,self.yMax+1):
      for x in range(0,self.xMax+1):
        if self.x0==x and self.y0==y and self.x1==x and self.y1==y:
          write("X")
        elif self.x0==x and self.y0==y:
          write("P")
        elif self.x1==x and self.y1==y:
          write("C")
        elif self.grid[y][x] == -1:
          write("#")
        else:
          write(str(self.grid[y][x]))
      print("")
