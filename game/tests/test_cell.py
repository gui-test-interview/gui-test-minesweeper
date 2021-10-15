import pytest

from game.models import Cell, CellState


def test_cell_default():
    cell = Cell()
    assert cell.count == 0
    assert cell.state == CellState.HIDDEN
    assert cell.mine is False


@pytest.mark.parametrize(
    "kwargs,expected",
    [
        ({}, 0),
        ({"count": 1}, 1),
        ({"count": 3}, 3),
        ({"mine": True}, 9),
        ({"count": 8, "state": CellState.REVEALED}, 18),
        ({"count": 2, "state": CellState.REVEALED}, 12),
        ({"state": CellState.REVEALED, "mine": True}, 19),
        ({"count": 4, "state": CellState.FLAGGED}, 24),
        ({"count": 1, "state": CellState.FLAGGED}, 21),
        ({"state": CellState.FLAGGED, "mine": True}, 29),
    ],
)
def test_cell_json_encode_decode_valid(kwargs, expected):
    assert Cell(**kwargs).to_int() == expected
    assert Cell.from_int(expected) == Cell(**kwargs)


def test_cell_json_encode_invalid():
    assert Cell(count=4, mine=True).to_int() == 9
    assert Cell(count=2, mine=True, state=CellState.REVEALED).to_int() == 19
    assert Cell(count=3, mine=True, state=CellState.FLAGGED).to_int() == 29
