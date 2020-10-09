import mdp

from gridactions import ManhattanMoves

class GridMDP(mdp.MDP):
    """
    Represents a Markov Decision Process on a square grid with wrap-around.
    
    - The grid is square of n_rows x n_columns.
    - Each location on the grid is associated with a tile, represented as a
    character string.
    - Tiles are used to denote rewards associated with a specific grid location.
    - Tiles can also denote 'walls'. These are invalid locations.
    
    States are pairs of (row,column), and every location within the grid is a 
    valid state unless that location is occupied by a wall tile.

    There are four basic actions: going north (decrease row index), south (increase
    row index), east (increase column index), or west (decrease column index).
    
    An action is applicable if the move does not end up in a state (grid location)
    with a wall tile.

    A move action may lead to a maximum of three different states
    1) With probability 0.8 the end state is the one indicated by the chosen action.
    2) With prob. 0.1 the end state is the one 90 deg clockwise.
    3) With prob. 0.1 the end state is the one 90 deg counter-clockwise.

    So for example. If the action north is chosen, from some state s, 
    with prob. 0.8 the next state is grid location one above (one row index lower)
    of s, but with prob. 0.1 it is the one to the right of s (clockwise of north = east),
    with prob. 0.1 it is the one to the left of s (counter clockwise of north = west).
    
    This class inherits from mpd.MDP and implements the require methods in this class.
    
    """
    
    def __init__(self, terrain, wall_tiles = {'#'}, tile_rewards = {'+':1, '-': -1}):
        """
        Create a GridMDP given a specific terrain layout, wall tiles, and rewards.
        
        Parameters
        ----------
        terrain : list of strings
           Each string denotes a row, and character in the string denotes the 
           tile on the corresponding column
        wall_tiles : set of characters
           Any character in this set denotes a wall tile.
        tile_rewards : dictionary string : float
           Maps from tile character to reward. Any character not in this set
           will have reward 0.

        A 3x5 grid can for example look like this:

        ..+..
        ..#..
        -....

        Each character is a 'tile'. Using default wall_tiles denotes # as walls.
        Every other kind of tile is then an allowed state.
        Using default tile_rewards associates + and - with some rewards +1, -1.
        As . is unspecified it will have reward value 0.

        It would be created as GridMDP(["..+..",
                                        "..#..",
                                        "-...."])

        """
        # Occupy terrain. Represent it internally as a dictionary from (row,col)
        # to tile character.
        self._terrain = {}
        # Assume square grid, and raise error if not.
        self.n_rows = len(terrain)
        self.n_cols = len(terrain[0])
        for r in range(self.n_rows):
            if len(terrain[r]) != self.n_cols:
                raise Exception("terrain not square grid")
            for c in range(self.n_cols):
                self._terrain[(r,c)] = terrain[r][c]
        # Create an internal representation of the actions.
        # These are dependent on the number of rows and columns.
        # See gridactions.py
        self._Actions = ManhattanMoves(self.n_rows,self.n_cols)

        # Just for convenience get the set of actions.
        self._actions = self._Actions.all_actions()

        self._rewards = tile_rewards
        
        self._wall_tiles = wall_tiles

        # Valid states are those (row,column) pairs with terrain not designated 'wall'
        self._states  = {s for s,t in self._terrain.items() if t not in self._wall_tiles}


    def P(self,s1,a,s2):
        """
        See doc for class MDP in mdp.py
        """
        # Get all arcs with probabilities
        arcs = self._arcs(s1,a)
        # Return the prob. for arc to s2, if existing. Otherwise 0.0.
        return arcs.get(s2,0.0)

    def R(self,s1,a,s2):
        """
        See doc for class MDP in mdp.py
        """
        # The reward is only dependent on the destination state tile.
        # Look up its terrain and then the corresponding reward.
        t = self._terrain[s2]
        # Look up, if not in the rewards then use 0.
        return self._rewards.get(t, 0.0)
        

    def _arcs(self,s,a):
        # Helper function to get process arcs (edges) given a start state an
        # a 'choice' of action.
        # Choosing action a means that it gets executed w. prob 0.8, but with
        # prob. 0.1 and 0.1 respectively we might also go in clockwise or
        # counter-clockwise direction (e.g. east and west is clockwise and
        # counter-clockwise respectively of north).
        # However, if there is a wall-tile in the destination state, the
        # corresponding move is not valid, and as a result the action will
        # lead to the same state.
        # So, the possible successor states is a subset of four different
        # states, the one corresponding to a(s), the action clockwise, and
        # counter-clockwise of a (applied to s), and s itself.
        # All depending on tiles.

        ss = {}
        # Go over set of possible successor states and probabilities
        for (s2,p) in ((a(s),0.8),
                   (self._Actions.left90(a)(s), 0.1),
                   (self._Actions.right90(a)(s),0.1)):
            # If the tile at s2 is a wall tile, then
            # we stand still, so s2 = s
            if self._terrain[s2] in self._wall_tiles:
                s2 = s
            # Update value in the state set with probability.
            ss[s2] = ss.get(s2,0.0) + p
        return ss
    
    def successor_states(self,s,a):
        """
        See doc for class MDP in mdp.py
        """
        # Return set of keys in arcs.
        # which is the possible successor_states.
        return self._arcs(s,a).keys()

    def applicable_actions(self,s):
        """
        See doc for class MDP in mdp.py
        """
        # By default, all actions are applicable
        # However, if the destination is a wall,
        # it is excluded.
        aa = []
        for a in self._actions:
            if self._terrain[a(s)] not in self._wall_tiles:
                aa.append(a)
        return set(aa)

    def states(self):
        """
        See doc for class MDP in mdp.py
        """
        return self._states
              

    def __str__(self):
        """
        Visualize terrain as grid.
        """
        grid = "\n".join(["".join([self._terrain[(r,c)] for c in range(self.n_cols)]) for r in range(self.n_rows)])
        return grid

    

