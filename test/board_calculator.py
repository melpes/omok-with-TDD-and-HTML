from enum import Enum, auto

import numpy as np
from numpy import ndarray


class BoardErrors:
    pass

    class PutEmptyStoneError(Exception):
        def __str__(self) -> str:
            error: str = "빈칸을 의미하는 돌은 놓을 수 없음"
            return super().__str__() + error

    class NotEmptyBoardError(Exception):
        def __str__(self) -> str:
            error: str = "보드에 돌을 놓으려는 자리가 빈칸이 아님"
            return super().__str__() + error

    class MinusIndexError(Exception):
        def __str__(self) -> str:
            error: str = "예외적인 상황을 배제하기 위해 마이너스 인덱싱은 금지"
            return super().__str__() + error
    
    class PutSameAgainError(Exception):
        def __str__(self) -> str:
            error: str = "연속으로 같은 돌을 놓을 수 없음"
            return super().__str__() + error
    
    class UseSliceError(Exception):
        def __str__(self) -> str:
            error: str = "슬라이싱을 이용하여 돌을 놓을 수 없음"
            return super().__str__() + error
    
    class WinError(Exception):
        def __str__(self) -> str:
            error: str = "한쪽 돌이 승리하여 더 이상 게임이 진행되지 못함"
            return super().__str__() + error
    
    class BlackFirstError(Exception):
        def __str__(self) -> str:
            error: str = "게임 첫 수는 흑돌이어야 함"
            return super().__str__() + error


class Stone(Enum):
    """오목판에 놓이는 돌의 종류"""
    WHITE = auto()
    "백돌"
    BLACK = auto()
    "흑돌"
    EMPTY = auto()
    "빈칸"


class Board:
    """오목판을 제공하고 오목 규칙들을 적용하여 게임을 진행함"""

    class InitBoard:
        """게임 규칙에서 벗어나 ndarray 인덱싱으로 여러 수를 놓을 수 있음"""
        def __init__(self, board: np.ndarray) -> None:
            self.__board: np.ndarray = board
    
        def __setitem__(self, idx, stones):
            self.__board[idx] = stones


    def __init__(self) -> None:
        self.__board: np.ndarray = np.full([15, 15], Stone.EMPTY, dtype=Stone)
        "오목판"
        self.__last_stone: Stone = Stone.EMPTY
        self.init_board: Board.InitBoard = Board.InitBoard(self.__board)
        """게임 규칙에서 벗어나 ndarray 인덱싱으로 여러 수를 놓을 수 있음"""

    @property
    def last_stone(self):
        return self.__last_stone

    @property
    def ndim(self):
        return self.__board.ndim

    @property
    def shape(self):
        return self.__board.shape

    def viewcopy(self) -> np.ndarray:
        return self.__board.copy()

    def __str__(self) -> str:
        """print(board)로 보드판 현황 표현"""
        result = "\n\n"
        result += "Board Shape : " + str(self.shape) + "\n"
        result += "Last Stone : " + str(self.last_stone) + "\n"
        result += "\nBoard View\n"
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

    def print(self, arr: np.ndarray):
        """ndarray의 구성요소 시각화"""
        result = ""
        if arr.ndim == 1:
            for stone in arr:
                if stone == Stone.EMPTY:
                    result += '`' + ' '
                elif stone == Stone.WHITE:
                    result += '○' + ' '
                elif stone == Stone.BLACK:
                    result += '●' + ' '
        elif arr.ndim == 2:
            for line in arr:
                for stone in line:
                    if stone == Stone.EMPTY:
                        result += '`' + ' '
                    elif stone == Stone.WHITE:
                        result += '○' + ' '
                    elif stone == Stone.BLACK:
                        result += '●' + ' '
                result += '\n'
        print(result)

    def __getitem__(self, idx) -> Stone:
        return self.__board[idx]

    def __setitem__(self, idx, stone: Stone) -> None:
        if type(idx) != tuple:
            raise BoardErrors.UseSliceError
        npidx = np.array(idx)
        if npidx.ndim > 1:
            raise BoardErrors.UseSliceError
        if npidx.dtype == object:
            raise BoardErrors.UseSliceError

        if self.__board[idx] != Stone.EMPTY:
            raise BoardErrors.NotEmptyBoardError
        if stone == Stone.EMPTY:
            raise BoardErrors.PutEmptyStoneError
        if idx[0] < 0 or idx[1] < 0:
            raise BoardErrors.MinusIndexError
        if self.__last_stone == stone:
            raise BoardErrors.PutSameAgainError
        if self.__last_stone == Stone.EMPTY and stone == Stone.WHITE:
            raise BoardErrors.BlackFirstError

        self.__board[idx] = stone
        self.__last_stone = stone

        self.judge_win()

    def judge_win(self):
        board = self.__board.copy()
        for i in range(self.__board.shape[0]):
            line: np.ndarray = board[i,:]
            self.__find_5_stack(line)

        for i in range(self.__board.shape[1]):
            line: np.ndarray = board[:,i]
            self.__find_5_stack(line)

        for i in range(self.__board.shape[0]):
            line: np.ndarray = board.diagonal(i)
            self.__find_5_stack(line)

        for i in range(self.__board.shape[1]):
            line: np.ndarray = board.diagonal(-i)
            self.__find_5_stack(line)

        for i in range(self.__board.shape[0]):
            line: np.ndarray = np.fliplr(board).diagonal(i)
            self.__find_5_stack(line)

        for i in range(self.__board.shape[1]):
            line: np.ndarray = np.fliplr(board).diagonal(-i)
            self.__find_5_stack(line)

    def __find_5_stack(self, line: np.ndarray):
        """입력받은 line에 대해 같은 돌이 5번 연속이면 WinError"""
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
                raise BoardErrors.WinError

    def deepcopy(self):
        newboard: Board = Board()
        newboard.init_board[:] = self.__board
        return newboard

class OmokAiErrors:
    pass
    
    class EmptyMystoneError(Exception):
        def __str__(self) -> str:
            error: str = "Stone.EMPTY를 ai.mystone으로 가질 수 없음"
            return super().__str__() + error
    
    class NoStoneChangedError(Exception):
        def __str__(self) -> str:
            error: str = "ai.put_stone()이 돌을 착수하지 않음"
            return super().__str__() + error
    
    class Error(Exception):
        def __str__(self) -> str:
            error: str = ""
            return super().__str__() + error

class OmokAi:
    def __init__(self, board: Board, mystone: Stone) -> None:
        if mystone == Stone.EMPTY:
            raise OmokAiErrors.EmptyMystoneError

        self.__board: Board = board
        self.mystone: Stone = mystone
        self.__scoreboard: np.ndarray = np.zeros(board.shape, dtype=int)

    @property
    def scoreboard(self):
        return self.__scoreboard

    def __init_scoreboard(self):
        self.__scoreboard: np.ndarray = np.zeros(self.__board.shape, dtype=int)

    def __str__(self) -> str:
        result = "\n"
        result += "mystone : " + str(self.mystone) + '\n'
        result += "\nScore View\n"
        for line in self.__scoreboard:
            for score in line:
                result += str(score) + ' '                
            result += '\n'
        return result
        

    def put_stone(self) -> None:
        before: np.ndarray = self.__board.viewcopy()

        pass

        after: np.ndarray = self.__board.viewcopy()
        if (before == after).all():
            raise OmokAiErrors.NoStoneChangedError

    def scoring(self):
        self.__init_scoreboard()
        for line, flag, i in self.__line_range():
            stack: int = 0
            line = np.concatenate([line, [Stone.EMPTY]])
            line_score: np.ndarray = np.zeros(line.size, int)
            for j, stone in enumerate(line):
                if stone == self.mystone:
                    stack += 1
                elif stack != 0:
                    self.__spread_stack(line, line_score, stack, j)
                    stack = 0
            line_score = line_score[:-1]
            match flag:
                case 'x':
                    self.__scoreboard[i,:] += line_score
                case 'y':
                    self.__scoreboard[:,i] += line_score
                case 'xy+':
                    self.__scoreboard += np.diag(line_score, k=i)
                case 'xy-':
                    self.__scoreboard += np.diag(line_score, k=-i)
                case 'yx+':
                    self.__scoreboard += np.fliplr(np.diag(line_score, k=i))
                case 'yx-':
                    self.__scoreboard += np.fliplr(np.diag(line_score, k=-i))

    def __spread_stack(self,
        line: ndarray, line_score: ndarray, stack: int, j: int
    ) -> None:
        self.unit: int = 1
        target_idx: tuple = j, j+1, j-stack-1, j-stack-2
        
        for idx in target_idx:
            if idx >= line.size or idx < 0:
                continue
            
            if line[idx] == Stone.EMPTY:
                line_score[idx] += stack * self.unit
                

    def __line_range(self):
        board = self.__board.viewcopy()
        self.__board.print(board)
        for i in range(self.__board.shape[0]):
            line: np.ndarray = board[i,:]
            yield line, "x", i

        for i in range(self.__board.shape[1]):
            line: np.ndarray = board[:,i]
            yield line, "y", i

        for i in range(self.__board.shape[0]):
            line: np.ndarray = board.diagonal(i)
            yield line, "xy+", i

        for i in range(1, self.__board.shape[1]):
            line: np.ndarray = board.diagonal(-i)
            yield line, "xy-", i

        for i in range(self.__board.shape[0]):
            line: np.ndarray = np.fliplr(board).diagonal(i)
            yield line, "yx+", i

        for i in range(1, self.__board.shape[1]):
            line: np.ndarray = np.fliplr(board).diagonal(-i)
            yield line, "yx-", i
