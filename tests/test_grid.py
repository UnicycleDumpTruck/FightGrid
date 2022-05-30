"""Test cases for grid module."""
import pytest

import fightgrid.config as cfg
from fightgrid import grid


@pytest.fixture
def default_grid() -> grid.Grid:
    return grid.Grid(cfg.GRID_SIZE)


def test_create_square() -> None:
    """Test creation and storage of attributes."""
    sq = grid.Square(x=0, y=1, label="T", highlight="y")
    assert sq.x == 0
    assert sq.y == 1
    assert sq.label == "T"
    assert sq.highlight == "y"


def test_create_grid(default_grid: grid.Grid) -> None:
    """Test creation of Grid full of squares."""
    coords = [
        [grid.Square(x, y) for x in range(cfg.GRID_SIZE)] for y in range(cfg.GRID_SIZE)
    ]
    for y, row in enumerate(coords):
        for x, sq in enumerate(row):
            g_sq = default_grid.get_square(sq)
            assert g_sq == sq
            assert sq.x == x
            assert sq.y == y


def test_get_square_xy(default_grid: grid.Grid) -> None:
    """Test if x & y match for returned Square."""
    coords = [
        [grid.Square(x, y) for x in range(cfg.GRID_SIZE)] for y in range(cfg.GRID_SIZE)
    ]
    for y, row in enumerate(coords):
        for x, sq in enumerate(row):
            g_sq = default_grid.get_square_xy(x, y)
            assert g_sq == sq
            assert sq.x == x
            assert sq.y == y


def test_moved_in_bounds(default_grid: grid.Grid) -> None:
    """Testing projected movement in bounds around grid."""
    start = default_grid.get_square_xy(0, 0)
    if top_right := default_grid.projected_from(
        start, grid.Direction.RIGHT, cfg.GRID_SIZE - 1
    ):
        if bottom_right := default_grid.projected_from(
            top_right, grid.Direction.DOWN, cfg.GRID_SIZE - 1
        ):
            if bottom_left := default_grid.projected_from(
                bottom_right, grid.Direction.LEFT, cfg.GRID_SIZE - 1
            ):
                end = default_grid.projected_from(
                    bottom_left, grid.Direction.UP, cfg.GRID_SIZE - 1
                )
            else:
                pytest.xfail()
        else:
            pytest.xfail()
    else:
        pytest.xfail()
    assert start is end


def test_square_valid(default_grid: grid.Grid) -> None:
    """Test square in bounds is valid."""
    for y in range(cfg.GRID_SIZE):
        for x in range(cfg.GRID_SIZE):
            assert default_grid.square_valid(grid.Square(x=x, y=y))


def test_square_neg_x_invalid(default_grid: grid.Grid) -> None:
    """Test Square valid with negative x."""
    assert default_grid.square_valid(grid.Square(-1, 0)) is False


def test_square_neg_y_invalid(default_grid: grid.Grid) -> None:
    """Test Square valid with negative x."""
    assert default_grid.square_valid(grid.Square(0, -1)) is False


def test_square_y_over_invalid(default_grid: grid.Grid) -> None:
    """Test Square valid with negative x."""
    assert default_grid.square_valid(grid.Square(0, cfg.GRID_SIZE + 1)) is False


def test_square_x_over_invalid(default_grid: grid.Grid) -> None:
    """Test Square valid with negative x."""
    assert default_grid.square_valid(grid.Square(cfg.GRID_SIZE + 1, 0)) is False


def test_valid_above(default_grid: grid.Grid) -> None:
    """Test returns valid square above."""
    start = default_grid.get_square_xy(0, 1)
    assert default_grid.above(start) == default_grid.get_square_xy(0, 0)


def test_none_above(default_grid: grid.Grid) -> None:
    """Test returns none for top row."""
    start = default_grid.get_square_xy(0, 0)
    assert default_grid.above(start) is None


def test_valid_left(default_grid: grid.Grid) -> None:
    """Test returns valid square left."""
    start = default_grid.get_square_xy(1, 0)
    assert default_grid.left(start) == default_grid.get_square_xy(0, 0)


def test_none_left(default_grid: grid.Grid) -> None:
    """Test returns none for left row."""
    start = default_grid.get_square_xy(0, 0)
    assert default_grid.left(start) is None


def test_valid_right(default_grid: grid.Grid) -> None:
    """Test returns valid square right."""
    start = default_grid.get_square_xy(cfg.GRID_SIZE - 2, 0)
    assert default_grid.right(start) == default_grid.get_square_xy(cfg.GRID_SIZE - 1, 0)


def test_none_right(default_grid: grid.Grid) -> None:
    """Test returns none for right row."""
    start = default_grid.get_square_xy(cfg.GRID_SIZE - 1, 0)
    assert default_grid.right(start) is None


def test_valid_below(default_grid: grid.Grid) -> None:
    """Test returns valid square right."""
    start = default_grid.get_square_xy(0, cfg.GRID_SIZE - 2)
    assert default_grid.below(start) == default_grid.get_square_xy(0, cfg.GRID_SIZE - 1)


def test_none_below(default_grid: grid.Grid) -> None:
    """Test returns none for right row."""
    start = default_grid.get_square_xy(0, cfg.GRID_SIZE - 1)
    assert default_grid.below(start) is None


def test_valid_lower_right(default_grid: grid.Grid) -> None:
    """Test returns valid square right."""
    start = default_grid.get_square_xy(0, cfg.GRID_SIZE - 2)
    assert default_grid.lower_right(start) == default_grid.get_square_xy(
        0, cfg.GRID_SIZE - 1
    )


def test_none_lower_right(default_grid: grid.Grid) -> None:
    """Test returns none for right row."""
    start = default_grid.get_square_xy(0, cfg.GRID_SIZE - 1)
    assert default_grid.lower_right(start) is None
