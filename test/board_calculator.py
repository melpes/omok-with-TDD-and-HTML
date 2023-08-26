import numpy as np
from enum import Enum, auto

class NotEmptyBoardError(Exception):
    pass
class PutEmptyStoneError(Exception):
    pass
class MinusIndexError(Exception):
    pass
class PutSameAgainError(Exception):
    pass


class Stone(Enum):
    WHITE = auto()
    BLACK = auto()
    EMPTY = auto()


class Board:
    def __init__(self) -> None:
        self.__board: np.ndarray = np.full([10, 10], Stone.EMPTY, dtype=Stone)
        self.__last_stone: Stone = Stone.EMPTY

    @property
    def shape(self):
        return self.__board.shape

    def __getitem__(self, idx) -> Stone:
        return self.__board[idx]

    def __setitem__(self, idx, stone: Stone) -> None:
        if self.__board[idx] != Stone.EMPTY:
            raise NotEmptyBoardError
        if stone == Stone.EMPTY:
            raise PutEmptyStoneError
        if idx[0] < 0 or idx[1] < 0:
            raise MinusIndexError
        if self.__last_stone == stone:
            raise PutSameAgainError

        self.__board[idx] = stone
        self.__last_stone = stone