"""Test cases for grid module."""
import pytest

import fightgrid.config as cfg
from fightgrid import grid


@pytest.fixture
def default_grid() -> grid.Grid:
    """Pytest fixture with grid of default size."""
    return grid.Grid(side_length=cfg.GRID_SIZE, def_pub_label="w", def_prv_label="x")


def test_create_square() -> None:
    """Test creation and storage of attributes."""
    sq = grid.Square(x=0, y=1, pub_label="T", prv_label="X", highlight="y")
    assert sq.x == 0
    assert sq.y == 1
    assert sq.pub_label == "T"
    assert sq.prv_label == "X"
    assert sq.highlight == "y"
    assert sq.__repr__() == "Sq x0 y1 pub:T prv:X state:EMPTY"


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


def test_moved_around_bounds(default_grid: grid.Grid) -> None:
    """Testing projected movement in bounds around grid."""
    start = default_grid.get_square_xy(0, 0)
    assert start is not None
    top_right = default_grid.projected_from(
        start, grid.Direction.RIGHT, cfg.GRID_SIZE - 1
    )
    assert top_right is not None
    bottom_right = default_grid.projected_from(
        top_right, grid.Direction.DOWN, cfg.GRID_SIZE - 1
    )
    assert bottom_right is not None
    bottom_left = default_grid.projected_from(
        bottom_right, grid.Direction.LEFT, cfg.GRID_SIZE - 1
    )
    assert bottom_left is not None
    end = default_grid.projected_from(bottom_left, grid.Direction.UP, cfg.GRID_SIZE - 1)
    assert start is end


# def test_projected_from_none_square_raises(default_grid: grid.Grid) -> None:
#     """Pass none to projected_from to test raises ValueError."""
#     with pytest.raises(ValueError):
#         default_grid.projected_from(None, grid.Direction.UP)  # type: ignore


# def test_projected_from_none_direction_raises(default_grid: grid.Grid) -> None:
#     """Pass none to projected_from to test raises ValueError."""
#     with pytest.raises(ValueError):
#         default_grid.projected_from(grid.Square(0, 0), None)  # type: ignore


def test_projected_out_of_bounds_returns_none(default_grid: grid.Grid) -> None:
    """Test for None returned when projecting out of bounds."""
    start = default_grid.get_square_xy(0, 0)
    end = default_grid.projected_from(start, grid.Direction.DOWN, cfg.GRID_SIZE)
    assert end is None


def test_projected_bad_direction_returns_none(default_grid: grid.Grid) -> None:
    """Test for None returned when projecting out of bounds."""
    start = default_grid.get_square_xy(0, 0)
    end = default_grid.projected_from(start, grid.Direction.FLIP, cfg.GRID_SIZE)
    assert end is None


def test_moved_around_single_square(default_grid: grid.Grid) -> None:
    """Project movement using all directions."""
    dg = default_grid
    start = dg.get_square_xy(1, 1)
    coords = [(0, 0), (1, 0), (2, 0), (0, 1), (2, 1), (0, 2), (1, 2), (2, 2)]
    squares = [
        dg.projected_from(start, grid.Direction.UP_LEFT),
        dg.projected_from(start, grid.Direction.UP),
        dg.projected_from(start, grid.Direction.UP_RIGHT),
        dg.projected_from(start, grid.Direction.LEFT),
        dg.projected_from(start, grid.Direction.RIGHT),
        dg.projected_from(start, grid.Direction.DOWN_LEFT),
        dg.projected_from(start, grid.Direction.DOWN),
        dg.projected_from(start, grid.Direction.DOWN_RIGHT),
    ]
    for pair in zip(coords, squares):
        assert dg.get_square_xy(*pair[0]) is pair[1]


def test_surrounding_squares(default_grid: grid.Grid) -> None:
    """Project movement using all directions."""
    dg = default_grid
    coords = [(1, 0), (0, 1), (2, 1), (1, 2)]
    squares = dg.surrounding_squares(dg.get_square_xy(1, 1))
    for pair in zip(coords, squares):
        assert dg.get_square_xy(*pair[0]) is pair[1]


def test_reticle_squares(default_grid: grid.Grid) -> None:
    """Project movement using all directions."""
    dg = default_grid
    coords = [(0, 0), (1, 0), (2, 0), (0, 1), (2, 1), (0, 2), (1, 2), (2, 2)]
    squares = dg.reticle_squares(dg.get_square_xy(1, 1))
    for pair in zip(coords, squares):
        assert dg.get_square_xy(*pair[0]) is pair[1]


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


def test_grid_string_labels_pub(default_grid: grid.Grid) -> None:
    """Test grid string generation with public labels."""
    expected = """w w w w w w w w w
w w w w w w w w w
w w w w w w w w w
w w w w w w w w w
w w w w w w w w w
w w w w w w w w w
w w w w w w w w w
w w w w w w w w w
w w w w w w w w w"""
    assert expected == default_grid.grid_string_labels()
    assert expected == default_grid.__repr__()


def test_grid_string_labels_prv(default_grid: grid.Grid) -> None:
    """Test grid string generation with private labels."""
    expected = """x x x x x x x x x
x x x x x x x x x
x x x x x x x x x
x x x x x x x x x
x x x x x x x x x
x x x x x x x x x
x x x x x x x x x
x x x x x x x x x
x x x x x x x x x"""
    assert expected == default_grid.grid_string_labels(prv=True)
