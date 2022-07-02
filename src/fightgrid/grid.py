"""Define coordinate system and grid."""
from enum import Enum
from enum import auto
from typing import List
from typing import Optional

import fightgrid.config as cfg


class Direction(Enum):
    """Direction for reference and moving entities."""

    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    UP_LEFT = auto()
    UP_RIGHT = auto()
    DOWN_LEFT = auto()
    DOWN_RIGHT = auto()
    FLIP = auto()
    NONE = auto()


class SqState(Enum):
    """General state of Grid Square."""

    EMPTY = auto()
    HIDDEN = auto()
    HIT = auto()
    MISS = auto()
    SUNK = auto()


class Square:
    """A single location on the grid."""

    def __init__(
        self,
        x: int,
        y: int,
        pub_label: Optional[str] = None,
        prv_label: Optional[str] = None,
        highlight: Optional[str] = None,
    ) -> None:
        """Initialize grid Square with at least x and y."""
        self.x = x
        self.y = y
        self.pub_label = pub_label
        self.prv_label = prv_label
        self.highlight = highlight
        self.state = SqState.EMPTY

    def __eq__(self: "Square", other: object) -> bool:
        """Test equality."""
        return (
            self.x == other.x and self.y == other.y
            if isinstance(other, Square)
            else False
        )

    def __repr__(self) -> str:
        """Represent Square object as string."""
        state_str = str(self.state).split(".")[1]
        return f"Sq x{self.x} y{self.y} pub:{self.pub_label} prv:{self.prv_label} state:{state_str}"


class Grid:
    """Grid of Squares."""

    def __init__(
        self,
        side_length: int = cfg.GRID_SIZE,
        def_pub_label: Optional[str] = None,
        def_prv_label: Optional[str] = None,
    ) -> None:
        """Initialize Grid."""
        self._grid = [
            [
                Square(x, y, pub_label=def_pub_label, prv_label=def_prv_label)
                for x in range(side_length)
            ]
            for y in range(side_length)
        ]

    def get_square(self, sq: Square) -> Square:
        """Given Square, return Square from grid with same x & y."""
        return self._grid[sq.y][sq.x]

    def get_square_xy(self, x: int, y: int) -> Square:
        """Given x and y coordinates, return the Square from the grid."""
        return self._grid[y][x]

    def projected_from(
        self, sq: Square, direction: Direction, distance: int = 1
    ) -> Optional[Square]:
        """Returns Square from grid a distance and direction away."""
        # if not sq:
        #     raise ValueError("Starting Square cannot be None.")
        if direction == Direction.UP:
            p = Square(y=(sq.y - distance), x=sq.x)
            return self.get_square(p) if self.square_valid(p) else None
        if direction == Direction.UP_LEFT:
            p = Square(y=(sq.y - distance), x=(sq.x - distance))
            return self.get_square(p) if self.square_valid(p) else None
        if direction == Direction.UP_RIGHT:
            p = Square(y=(sq.y - distance), x=(sq.x + distance))
            return self.get_square(p) if self.square_valid(p) else None
        if direction == Direction.DOWN:
            p = Square(y=(sq.y + distance), x=sq.x)
            return self.get_square(p) if self.square_valid(p) else None
        if direction == Direction.DOWN_LEFT:
            p = Square(y=(sq.y + distance), x=(sq.x - 1))
            return self.get_square(p) if self.square_valid(p) else None
        if direction == Direction.DOWN_RIGHT:
            p = Square(y=(sq.y + distance), x=(sq.x + 1))
            return self.get_square(p) if self.square_valid(p) else None
        if direction == Direction.LEFT:
            p = Square(y=sq.y, x=(sq.x - distance))
            return self.get_square(p) if self.square_valid(p) else None
        if direction == Direction.RIGHT:
            p = Square(y=sq.y, x=(sq.x + distance))
            return self.get_square(p) if self.square_valid(p) else None
        return None
        # raise ValueError("Invalid direction given, can't project movement.")

    def square_valid(self, sq: Square) -> bool:
        """Returns True if point is within grid bounds."""
        if (sq.x < 0) or (cfg.GRID_SIZE <= sq.x):
            return False
        if (sq.y < 0) or (cfg.GRID_SIZE <= sq.y):
            return False
        return True

    def surrounding_squares(self, sq: Square) -> List[Square]:
        """Return Squares that are up, down, left, right from given."""
        surrounding = [
            self.projected_from(sq, Direction.UP),
            self.projected_from(sq, Direction.LEFT),
            self.projected_from(sq, Direction.RIGHT),
            self.projected_from(sq, Direction.DOWN),
        ]
        return list(filter(None, surrounding))

    def reticle_squares(self, sq: Square) -> List[Square]:
        """Return all surrounding squares."""
        corners = [
            self.projected_from(sq, Direction.UP_LEFT),
            self.projected_from(sq, Direction.UP),
            self.projected_from(sq, Direction.UP_RIGHT),
            self.projected_from(sq, Direction.LEFT),
            self.projected_from(sq, Direction.RIGHT),
            self.projected_from(sq, Direction.DOWN_LEFT),
            self.projected_from(sq, Direction.DOWN),
            self.projected_from(sq, Direction.DOWN_RIGHT),
        ]
        return list(filter(None, corners))

    def grid_string_labels(self, prv: Optional[bool] = False) -> str:
        """Return simple string representation of grid.

        Args:
        prv (bool, optional): Flag to show private label
        for each square. Defaults to False, showing each
        square's public label.

        Returns:
        str: String representation of grid. Spaces between
        squares on a row, newlines between rows.
        """
        return "\n".join(
            " ".join([(s.prv_label if prv else s.pub_label) or " " for s in row])
            for row in self._grid
        )

    def __repr__(self) -> str:
        """Return a string representation of Grid."""
        return self.grid_string_labels()
