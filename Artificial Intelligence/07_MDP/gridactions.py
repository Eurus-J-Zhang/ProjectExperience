"""
Utility classes for GridMDP describing associated actions.
"""

class GridAction:
    """
    Implements and action on a row,column pair.
    
    Wrap-around, so that walking off the 'edge' leads to the other side.
    """
    def __init__(self, name, n_rows, n_cols, d_row, d_col):
        """
        Parameters
        ----------
        name : string
        n_rows : int
           Number of rows
        n_cols : int
           Number of columns
        d_row : int
           Difference in row coordinate by move.
        d_col : int
           Difference in column coordinate by move.
        """
        self._name = name
        self._n_rows = n_rows
        self._n_cols = n_cols
        self._dr = d_row
        self._dc = d_col

    def __call__(self,s):
        """
        Makes the instance callable.
        
        Parameters
        ----------
        s : pair of int
          (row,column)
        
        Returns
        -------
        pair of int
           Updated (row,column) pair.
        """
        r,c = s
        # When instance is called return a pair of row,col coordinates
        # 'wrapped around' by using modulo.
        return ((r + self._dr) % self._n_rows,
                    (c + self._dc) % self._n_cols)

    def __str__(self):
        return str(self._name)
        
class ManhattanMoves:
    """
    Class representing the set of Manhattan moves: north, south, east, and west.
    """
    def __init__(self,n_rows,n_cols):
        """
        Parameters
        ----------
        n_rows : int
           Number of rows.
        n_cols : int
           Number of columns.
        """
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.north = GridAction("North", self.n_rows, self.n_cols, -1, 0)
        self.south = GridAction("South", self.n_rows, self.n_cols, 1, 0)
        self.west = GridAction("West", self.n_rows, self.n_cols, 0, -1)
        self.east = GridAction("East", self.n_rows, self.n_cols, 0, 1)

    def all_actions(self):
        """
        Returns
        -------
        set of GridAction objects.
        """
        return {self.north, self.south, self.east, self.west}

    def left90(self,a):
        """
        Get the counter clockwise action of a.
        
        Parameters
        ----------
        a : GridAction in all_actions.

        Returns
        -------
        GridAction in all_actions
        """
        if self.north == a:
            return self.west
        elif self.west == a:
            return self.south
        elif self.south == a:
            return self.east
        elif self.east == a:
            return self.north
        else:
            raise ValueError(a)

    def right90(self,a):
        """
        Get the clockwise action of a.
        
        Parameters
        ----------
        a : GridAction in all_actions.

        Returns
        -------
        GridAction in all_actions
        """
        if self.north == a:
            return self.east
        elif self.west == a:
            return self.north
        elif self.south == a:
            return self.west
        elif self.east == a:
            return self.south
        else:
            raise ValueError(a)

