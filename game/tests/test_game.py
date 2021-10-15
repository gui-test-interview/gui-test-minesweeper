import pytest

from game.models import Game, GameState

pytestmark = pytest.mark.django_db


@pytest.fixture
def game_simple():
    game = Game(width=9, height=9, mines=10)
    game.initialize()
    return game


def test_game_initialize(game_simple):
    assert game_simple.width == 9
    assert game_simple.height == 9
    assert game_simple.mines == 10
    assert game_simple.state == GameState.STARTED
    assert game_simple.progress == 0
    assert len(game_simple.board) == 9
    assert all(len(row) == 9 for row in game_simple.board)
    assert sum(cell.mine for row in game_simple.board for cell in row) == 10


def test_game_flag(game_simple):
    game_simple.toggle_flag(0, 0)
    assert game_simple.board[0][0].flagged
    game_simple.toggle_flag(0, 0)
    assert not game_simple.board[0][0].flagged
    game_simple.toggle_flag(0, 0, True)
    assert game_simple.board[0][0].flagged
    game_simple.toggle_flag(0, 0, True)
    assert game_simple.board[0][0].flagged
    game_simple.toggle_flag(0, 0, False)
    assert not game_simple.board[0][0].flagged
    game_simple.toggle_flag(0, 0, False)
    assert not game_simple.board[0][0].flagged


def test_game_lost(game_simple):
    game_simple.lose()
    assert game_simple.state == GameState.LOST
    assert game_simple.date_ended is not None


def test_game_won(game_simple):
    game_simple.win()
    assert game_simple.state == GameState.WON
    assert game_simple.date_ended is not None


def test_game_neighbors(game_simple):
    assert list(game_simple.neighbors(0, 0)) == [(0, 1), (1, 0), (1, 1)]
    assert list(game_simple.neighbors(8, 8)) == [(7, 7), (7, 8), (8, 7)]
    assert list(game_simple.neighbors(1, 0)) == [(0, 0), (0, 1), (1, 1), (2, 0), (2, 1)]
    assert list(game_simple.neighbors(7, 8)) == [(6, 7), (6, 8), (7, 7), (8, 7), (8, 8)]
    assert list(game_simple.neighbors(1, 1)) == [
        (0, 0),
        (0, 1),
        (0, 2),
        (1, 0),
        (1, 2),
        (2, 0),
        (2, 1),
        (2, 2),
    ]
