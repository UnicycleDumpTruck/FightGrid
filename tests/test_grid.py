"""Test cases for grid module."""
import pytest

from fightgrid import grid
import fightgrid.config as cfg


def test_create_square() -> None:
    """Test creation and storage of attributes."""
    sq = grid.Square(x=0, y=1, label="T", highlight="y")
    assert sq.x == 0
    assert sq.y == 1
    assert sq.label == "T"
    assert sq.highlight == "y"


def test_create_grid() -> None:
    """Test creation of Grid full of squares."""
    gr = grid.Grid(cfg.GRID_SIZE)
    coords = [
        [grid.Square(x, y) for x in range(cfg.GRID_SIZE)] for y in range(cfg.GRID_SIZE)
    ]
    for y, row in enumerate(coords):
        for x, sq in enumerate(row):
            g_sq = gr.get_square(sq)
            assert g_sq == sq
            assert sq.x == x
            assert sq.y == y
