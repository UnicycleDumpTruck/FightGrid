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


class Square:
    """A single location on the grid."""

    def __init__(
        self,
        x: int,
        y: int,
        label: Optional[str] = None,
        highlight: Optional[str] = None,
    ) -> None:
        """Initialize grid Square with at least x and y."""
        self.x = x
        self.y = y
        self.label = label
        self.highlight = highlight

    def __eq__(self: "Square", other: object) -> bool:
        """Test equality."""
        return (
            self.x == other.x and self.y == other.y
            if isinstance(other, Square)
            else False
        )

    def __repr__(self) -> str:
        """Represent Square object as string."""
        return f"Sq x:{self.x} y:{self.y} lbl:{self.label} hl:{self.highlight}"


class Grid:
    """Grid of Squares."""

    def __init__(self, side_length: int = cfg.GRID_SIZE) -> None:
        """Initialize Grid."""
        self._grid = [
            [Square(x, y) for x in range(cfg.GRID_SIZE)] for y in range(cfg.GRID_SIZE)
        ]

    def get_square(self, sq: Square) -> Square:
        """Given Square, return Square from grid with same x & y. Label and hl may differ."""
        return self._grid[sq.y][sq.x]

    def get_square_xy(self, x: int, y: int) -> Square:
        """Given x and y coordinates, return the Square from the grid."""
        return self._grid[y][x]

    def projected_from(
        self, sq: Square, direction: Direction, distance: int = 1
    ) -> Optional[Square]:
        """Returns Square from grid a distance and direction away."""
        if not sq:
            raise ValueError("Starting Square cannot be None.")
        if direction == Direction.UP:
            p = Square(y=(sq.y - distance), x=sq.x)
            return self.get_square(p) if self.square_valid(p) else None
        if direction == Direction.DOWN:
            p = Square(y=(sq.y + distance), x=sq.x)
            return self.get_square(p) if self.square_valid(p) else None
        if direction == Direction.LEFT:
            p = Square(y=sq.y, x=(sq.x - distance))
            return self.get_square(p) if self.square_valid(p) else None
        if direction == Direction.RIGHT:
            p = Square(y=sq.y, x=(sq.x + distance))
            return self.get_square(p) if self.square_valid(p) else None
        raise ValueError("Invalid direction given, can't project movement.")

    def square_valid(self, sq: Square) -> bool:
        """Returns True if point is within grid bounds."""
        if (sq.x < 0) or (cfg.GRID_SIZE <= sq.x):
            return False
        if (sq.y < 0) or (cfg.GRID_SIZE <= sq.y):
            return False
        return True

    def above(self, sq: Square) -> Optional[Square]:
        """Return Square with coords above self."""
        return None if sq.y < 1 else self.get_square_xy(sq.x, sq.y - 1)

    def left(self, sq: Square) -> Optional[Square]:
        return None if sq.x < 1 else self.get_square_xy(sq.x - 1, sq.y)

    def upper_left(self, sq: Square) -> Optional[Square]:
        if sq.y < 1 or sq.x < 1:
            return None
        return self.get_square_xy(x=sq.x - 1, y=sq.y - 1)

    def upper_right(self, sq: Square) -> Optional[Square]:
        if sq.y < 1 or sq.x > cfg.GRID_SIZE - 2:
            return None
        return self.get_square_xy(x=sq.x + 1, y=sq.y - 1)

    def lower_left(self, sq: Square) -> Optional[Square]:
        if sq.y > cfg.GRID_SIZE - 2 or sq.x < 1:
            return None
        return self.get_square_xy(x=sq.x - 1, y=sq.y + 1)

    def lower_right(self, sq: Square) -> Optional[Square]:
        if sq.y > cfg.GRID_SIZE - 2 or sq.x > cfg.GRID_SIZE - 2:
            return None
        return self.get_square_xy(x=sq.x + 1, y=sq.y + 1)

    def right(self, sq: Square) -> Optional[Square]:
        return None if sq.x > cfg.GRID_SIZE - 2 else self.get_square_xy(sq.x + 1, sq.y)

    def below(self, sq: Square) -> Optional[Square]:
        return None if sq.y > cfg.GRID_SIZE - 2 else self.get_square_xy(sq.x, sq.y + 1)

    def surrounding_points(self, sq: Square) -> List[Square]:
        funcs = [self.above, self.left, self.right, self.below]
        surrounding = [f(sq) for f in funcs]
        return list(filter(None, surrounding))

    def reticle_points(self, sq: Square) -> List[Square]:
        """Return out corner surrounding squares."""
        funcs = [
            self.upper_left,
            self.lower_left,
            self.upper_right,
            self.lower_right,
        ]
        corners = [f(sq) for f in funcs]
        return list(filter(None, corners))
