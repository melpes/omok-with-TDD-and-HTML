import unittest

from board_calculator import (
    Board,
    MinusIndexError,
    NotEmptyBoardError,
    PutEmptyStoneError,
    PutSameAgainError,
    Stone,
    WinError,
)


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
        board[3,4] = Stone.BLACK
        board[5,4] = Stone.WHITE
        with self.assertRaises(PutSameAgainError):
            board[6,3] = Stone.BLACK
            board[1,4] = Stone.BLACK
        with self.assertRaises(PutSameAgainError):
            board[1,2:5] = Stone.WHITE
            
        with self.assertRaises(PutSameAgainError):
            board[1:3,2] = Stone.BLACK
            
        with self.assertRaises(PutSameAgainError):
            board[1:3,2:5] = Stone.WHITE

    def test_board_index_type(self):
        """다양한 종류의 idx 타입에 대응하는지 확인"""
        board: Board = Board()
        
        board[1,2]
        board[1,2:5]
        board[1:3,2]
        board[1:3,2:5]
        board[[2,3]]
        board[(2,3),(4,3)]

        board[1,2] = Stone.BLACK

    def test_print_board(self):
        """print(board)로 보드 보여주기"""

    def test_init_board(self):
        """board.init_board[idx]를 통해 stone 채우기"""
        board: Board = Board()
        
        board.init_board[(1,2,3),(1,2,3)] = Stone.WHITE
        self.assertTrue((board[(1,2,3),(1,2,3)] == Stone.WHITE).any())
        
        board.init_board[[1,2,3]] = Stone.BLACK
        self.assertTrue((board[[1,2,3]] == Stone.BLACK).any())
        
        board.init_board[1:3, 3:5] = Stone.WHITE
        self.assertTrue((board[1:3, 3:5] == Stone.WHITE).any())

    def __assert_judge_win(self, idx):
        with self.assertRaises(WinError):
            board: Board = Board()
            board.init_board[idx] = Stone.WHITE
            board.judge_win()
        with self.assertRaises(WinError):
            board: Board = Board()
            board.init_board[idx] = Stone.BLACK
            board.judge_win()

    def test_condition_to_win(self):
        """한 종류의 stone이 오목을 완성하면 WinError"""
        self.__assert_judge_win(((4,4,4,4,4),(1,2,3,4,5)))
        self.__assert_judge_win(1)
        self.__assert_judge_win((slice(10), 1))
        self.__assert_judge_win((slice(1,6), 1))
        self.__assert_judge_win((1, slice(1,6)))
        self.__assert_judge_win((slice(1,6), slice(1,6)))
        self.__assert_judge_win([1,2,0])

        self.__assert_judge_win(((1,2,3,4,5),(1,2,3,4,5)))

if __name__ == "__main__":
    unittest.main()