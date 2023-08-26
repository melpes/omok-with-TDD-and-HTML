import unittest
from board_calculator import Board, Stone
from board_calculator import NotEmptyBoardError
from board_calculator import PutEmptyStoneError
from board_calculator import MinusIndexError
from board_calculator import PutSameAgainError
import numpy as np


class TestBoard(unittest.TestCase):
    def __assert_is_board_changed(
        self,
        board: Board,
        pos: tuple,
        stone_to_put: Stone
    ):
        self.assertNotEqual(board[pos],stone_to_put)
        board[pos] = stone_to_put
        self.assertEqual(board[pos],stone_to_put)

    def test_can_put_stone_on_board(self):
        """보드 빈칸에 흑/백 돌을 올리는 경우"""
        board: Board = Board()
        try:
            self.__assert_is_board_changed(
                board=board,
                pos=(0,0),
                stone_to_put=Stone.WHITE
            )
            self.__assert_is_board_changed(
                board=board,
                pos=(0,1),
                stone_to_put=Stone.WHITE
            )
            self.__assert_is_board_changed(
                board=board,
                pos=(4,9),
                stone_to_put=Stone.BLACK
            )
            self.__assert_is_board_changed(
                board=board,
                pos=(5,9),
                stone_to_put=Stone.WHITE
            )
            self.__assert_is_board_changed(
                board=board,
                pos=(6,7),
                stone_to_put=Stone.BLACK
            )
        except PutSameAgainError:
            pass

    def test_can_add_stone_on_stone(self):
        """이미 돌이 있는 칸에 돌을 올리는 경우 NotEmptyBoardError"""
        board: Board = Board()
        board[4,4] = Stone.WHITE
        
        with self.assertRaises(NotEmptyBoardError):
            board[4,4] = Stone.BLACK
        
        with self.assertRaises(NotEmptyBoardError):
            board[4,4] = Stone.WHITE

    def test_put_empty_error(self):
        """Stone.EMPTY를 올리는 경우 PutEmptyStoneError"""
        board: Board = Board()
        with self.assertRaises(PutEmptyStoneError):
            board[3,5] = Stone.EMPTY

    def test_shape_immutable(self):
        """board.shape를 변경할 수 없어야 함"""
        board: Board = Board()
        with self.assertRaises(AttributeError):
            board.shape = (5,5)
    
    def test_put_out_of_range(self):
        """board 크기 밖에 Stone을 올리는 경우 IndexError"""
        board: Board = Board()
        with self.assertRaises(IndexError):
            board[board.shape[0],0] = Stone.WHITE        
        with self.assertRaises(IndexError):
            board[0,board.shape[1]] = Stone.WHITE

    def test_put_minus_position(self):
        """board의 좌표는 음수를 허용하지 않음"""
        board: Board = Board()
        with self.assertRaises(MinusIndexError):
            board[-1,-3] = Stone.BLACK

    def test_put_same_stone_twice(self):
        """같은 돌을 연속해서 두는 경우 PutSameAgainError"""
        board: Board = Board()
        with self.assertRaises(PutSameAgainError):
            board[2,3] = Stone.WHITE
            board[2,4] = Stone.WHITE

if __name__ == "__main__":
    unittest.main()