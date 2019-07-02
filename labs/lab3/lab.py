"""6.009 Lab 3 -- HyperMines"""

import sys
sys.setrecursionlimit(10000)
# NO ADDITIONAL IMPORTS


class HyperMinesGame:
    def __init__(self, dimensions, bombs):
        """Start a new game.

        This method should properly initialize the "board", "mask",
        "dimensions", and "state" attributes.

        Args:
           dimensions (list): Dimensions of the board
           bombs (list): Bomb locations as a list of lists, each an
                         N-dimensional coordinate
        """
        raise NotImplementedError

    def get_coords(self, coords):
        """Get the value of a square at the given coordinates on the board.

        (Optional) Implement this method to return the value of a square at the given
        coordinates.

        Args:
            coords (list): Coordinates of the square

        Returns:
            any: Value of the square
        """
        raise NotImplementedError

    def set_coords(self, coords, value):
        """Set the value of a square at the given coordinates on the board.

        (Optional) Implement this method to set the value of a square at the given
        coordinates.

        Args:
            coords (list): Coordinates of the square
        """
        raise NotImplementedError

    def make_board(self, dimensions, elem):
        """Return a new game board

        (Optional) Implement this method to return a board of N-Dimensions.

        Args:
            dimensions (list): Dimensions of the board
            elem (any): Initial value of every square on the board

        Returns:
            list: N-Dimensional board
        """
        raise NotImplementedError # Remove this if you decide not to implement this method

    def is_in_bounds(self, coords):
        """Return whether the coordinates are within bound

        (Optional) Implement this method to check boundaries for N-Dimensional boards.

        Args:
            coords (list): Coordinates of a square

        Returns:
            boolean: True if the coordinates are within bound and False otherwise
        """
        raise NotImplementedError # Remove this if you decide not to implement this method

    def neighbors(self, coords):
        """Return a list of the neighbors of a square

        (Optional) Implement this method to return the neighbors of an N-Dimensional square.

        Args:
            coords (list): List of coordinates for the square (integers)

        Returns:
            list: coordinates of neighbors
        """
        raise NotImplementedError # Remove this if you decide not to implement this method


    def is_victory(self):
        """Returns whether there is a victory in the game.

        A victory occurs when all non-bomb squares have been revealed.
        (Optional) Implement this method to properly check for victory in an N-Dimensional board.

        Returns:
            boolean: True if there is a victory and False otherwise
        """
        raise NotImplementedError # Remove this if you decide not to implement this method

    def dig(self, coords):
        """Recursively dig up square at coords and neighboring squares.

        Update the mask to reveal square at coords; then recursively reveal its
        neighbors, as long as coords does not contain and is not adjacent to a
        bomb.  Return a number indicating how many squares were revealed.  No
        action should be taken and 0 returned if the incoming state of the game
        is not "ongoing".

        The updated state is "defeat" when at least one bomb is visible on the
        board after digging, "victory" when all safe squares (squares that do
        not contain a bomb) and no bombs are visible, and "ongoing" otherwise.

        Args:
           coords (list): Where to start digging

        Returns:
           int: number of squares revealed
        """
        raise NotImplementedError


    def render(self, xray=False):
        """Prepare the game for display.

        Returns an N-dimensional array (nested lists) of "_" (hidden squares),
        "." (bombs), " " (empty squares), or "1", "2", etc. (squares
        neighboring bombs).  The mask indicates which squares should be
        visible.  If xray is True (the default is False), the mask is ignored
        and all cells are shown.

        Args:
           xray (bool): Whether to reveal all tiles or just the ones allowed by
                        the mask

        Returns:
           An n-dimensional array (nested lists)
        """
        raise NotImplementedError

    # ***Methods below this point are for testing and debugging purposes only. Do not modify anything here!***

    def dump(self):
        """Print a human-readable representation of this game."""
        lines = ["dimensions: %s" % (self.dimensions, ),
                 "board: %s" % ("\n       ".join(map(str, self.board)), ),
                 "mask:  %s" % ("\n       ".join(map(str, self.mask)), ),
                 "state: %s" % (self.state, )]
        print("\n".join(lines))

    @classmethod
    def from_dict(cls, d):
        """Create a new instance of the class with attributes initialized to
        match those in the given dictionary."""
        game = cls.__new__(cls)
        for i in ('dimensions', 'board', 'state', 'mask'):
            setattr(game, i, d[i])
        return game
