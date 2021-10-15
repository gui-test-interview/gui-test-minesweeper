import enum
import uuid
import json
import random
import datetime
import itertools
import dataclasses
from typing import Optional, Tuple, Iterator
from django.db import models
from django.urls import reverse
from django.utils import timezone


class CellState(enum.IntEnum):
    """
    Represents the state of a cell: hidden (default), revealed, or flagged.
    """

    HIDDEN = 0
    REVEALED = 1
    FLAGGED = 2


@dataclasses.dataclass
class Cell:
    """
    A single cell in a minesweeper board. This class is not a Django model! Rather, it
    is a dataclass which stores attributes related to a cell in a board, like whether it
    has a mine, if it is revealed or flagged, and how many mines are nearby. A cell is
    serialized in the database as a single integer with the following format:

        XY
         ^- 1's place: 0-8 number of mines nearby, or 9 if this cell is a mine
        ^-- 10's place: 0 for hidden, 1 for revealed, and 2 for flagged

    For example:

        01 = hidden cell with 1 neighboring mine
        13 = revealed cell with 3 neighboring mines
        29 = flagged cell containing a mine
    """

    mine: bool = False
    count: int = 0
    state: CellState = CellState.HIDDEN

    @property
    def visible(self) -> bool:
        return self.state == CellState.REVEALED

    @property
    def flagged(self) -> bool:
        return self.state == CellState.FLAGGED

    @classmethod
    def from_int(cls, val: int) -> "Cell":
        state = CellState(val // 10)
        mine = val % 10 == 9
        count = val % 10 if not mine else 0
        return cls(mine=mine, count=count, state=state)

    def to_int(self) -> int:
        return 10 * self.state + (9 if self.mine else self.count)


class BoardEncoder(json.JSONEncoder):
    """
    Custom JSON encoder which encodes Cells as integers, used as the encoder for the
    JSON field storing a board.
    """

    def default(self, o):
        if isinstance(o, Cell):
            return o.to_int()
        return super().default(o)


class BoardDecoder(json.JSONDecoder):
    """
    Custom JSON decoder which decodes all integers into Cells, used as the decoder for
    the JSON field storing a board.
    """

    def __init__(self, *args, **kwargs):
        kwargs["parse_int"] = lambda val: Cell.from_int(int(val))
        super().__init__(*args, **kwargs)


class GameState(models.IntegerChoices):
    """
    Represents the state of a game.
    """

    STARTED = 0
    WON = 1
    LOST = 2


class Game(models.Model):
    """
    A minesweeper game. The board state is represented as a list of lists of cells.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    width = models.PositiveSmallIntegerField()
    height = models.PositiveSmallIntegerField()
    mines = models.PositiveSmallIntegerField()
    board = models.JSONField(encoder=BoardEncoder, decoder=BoardDecoder)
    state = models.PositiveSmallIntegerField(
        choices=GameState.choices, default=GameState.STARTED
    )
    date_started: Optional[datetime.datetime] = models.DateTimeField(null=True)
    date_ended: Optional[datetime.datetime] = models.DateTimeField(null=True)

    def get_absolute_url(self) -> str:
        return reverse("game-detail", kwargs={"pk": self.id})

    def __repr__(self):
        return f"<Game({self.id}): {self.width}x{self.height}, {self.mines} mines>"

    @property
    def progress(self) -> float:
        """
        Returns the completion percentage of this game as a number between 0-1.
        """
        revealed = sum(cell.visible for row in self.board for cell in row)
        total = self.width * self.height - self.mines
        return revealed / total

    def clean(self):
        """
        Checks that the board is in a valid state, and re-initializes the game if
        necessary. This gets called when saving via a ModelForm (like in the admin).

        This game is valid if the board is a list of lists in the right shape (height
        and width) and has the correct number of mines present.
        """
        if (
            not self.board
            or len(self.board) != self.height
            or not all(len(row) == self.width for row in self.board)
            or sum(cell.mine for row in self.board for cell in row) != self.mines
        ):
            self.initialize()

    def initialize(self):
        """
        Re-initialize this game.
        """
        self.board = [[Cell() for j in range(self.width)] for i in range(self.height)]
        self.state = GameState.STARTED
        self.date_started = timezone.now()
        self.fill_mines()

    def fill_mines(self):
        """
        Fills the board with mines. Expects that the board is empty.
        """
        indices = list(itertools.product(range(self.height), range(self.width)))
        mines = random.sample(indices, self.mines)

        for i, j in mines:
            self.board[i][j].mine = True
            for ni, nj in self.neighbors(i, j):
                self.board[ni][nj].count += 1

    def neighbors(self, row: int, col: int) -> Iterator[Tuple[int, int]]:
        """
        Given a row, col position on the board, return an iterator over all neighbors of
        that cell.
        """
        for i in range(max(0, row - 1), min(row + 2, self.height)):
            for j in range(max(0, col - 1), min(col + 2, self.width)):
                if (i, j) != (row, col):
                    yield i, j

    def toggle_flag(self, row: int, col: int, val: Optional[bool] = None):
        """
        Toggles a flag in the given cell. If the cell is already revealed, this will
        do nothing. If a value is passed, sets the flag state rather than toggling.
        """
        cell = self.board[row][col]
        if cell.state == CellState.REVEALED:
            return
        flagged = not cell.flagged if val is None else val
        cell.state = [CellState.HIDDEN, CellState.FLAGGED][flagged]
        return cell.state

    def lose(self):
        """
        Transition this game to a lost state.
        """
        self.state = GameState.LOST
        self.date_ended = timezone.now()

    def win(self):
        """
        Transition this game to a won state.
        """
        self.state = GameState.WON
        self.date_ended = timezone.now()

    def reveal(self, row: int, col: int):
        """
        Reveal the given cell. If the cell is flagged or already revealed, this will
        do nothing. If the cell is a mine, the game is lost and all mines are revealed.
        Otherwise, the cell and (possibly) surrounding cells are revealed.
        """
        cell = self.board[row][col]

        if cell.flagged or cell.visible:
            return

        cell.state = CellState.REVEALED

        # TODO: check win/loss state.
        # TODO: implement expansion logic.
