from enum import Enum, auto

import numpy as np


class NotEmptyBoardError(Exception):
    pass
class PutEmptyStoneError(Exception):
    pass
class MinusIndexError(Exception):
    pass
class PutSameAgainError(Exception):
    pass
class WinError(Exception):
    pass


class Stone(Enum):
    WHITE = auto()
    BLACK = auto()
    EMPTY = auto()


class Board:
    def __init__(self) -> None:
        self.__board: np.ndarray = np.full([10, 10], Stone.EMPTY, dtype=Stone)
        self.__last_stone: Stone = Stone.EMPTY
        self.init_board: InitBoard = InitBoard(self.__board)

    @property
    def shape(self):
        return self.__board.shape

    def __str__(self) -> str:
        result = ""
        for line in self.__board:
            for stone in line:
                if stone == Stone.EMPTY:
                    result += '`' + ' '
                elif stone == Stone.WHITE:
                    result += '○' + ' '
                elif stone == Stone.BLACK:
                    result += '●' + ' '
            result += '\n'
        return result

    def __getitem__(self, idx) -> Stone:
        return self.__board[idx]

    def __setitem__(self, idx, stone: Stone) -> None:
        if type(idx) != tuple:
            raise PutSameAgainError
        if type(idx[0]) != int or type(idx[1]) != int:
            raise PutSameAgainError
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

    def judge_win(self):
        for i in range(self.__board.shape[1]):
            line: np.ndarray = self.__board[:,i].copy()
            stack: int = 0
            last_stone: Stone = Stone.EMPTY

            for stone in line:
                if stone == Stone.EMPTY:
                    stack = 0
                elif last_stone != stone:
                    last_stone = stone
                    stack = 1
                elif last_stone == stone:
                    stack += 1
                if stack == 5:
                    raise WinError

        for i in range(self.__board.shape[0]):
            line: np.ndarray = self.__board[i,:].copy()
            stack: int = 0
            last_stone: Stone = Stone.EMPTY

            for stone in line:
                if stone == Stone.EMPTY:
                    stack = 0
                elif last_stone != stone:
                    last_stone = stone
                    stack = 1
                elif last_stone == stone:
                    stack += 1
                if stack == 5:
                    raise WinError

class InitBoard:
    def __init__(self, board: np.ndarray) -> None:
        self.__board: np.ndarray = board

    def __setitem__(self, idx, stone: Stone):
        self.__board[idx] = stone