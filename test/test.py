import unittest

import numpy as np
from board_calculator import (
    Board,
    BoardErrors,
    OmokAi,
    OmokAiErrors,
    Stone,
)


class TestBoard(unittest.TestCase):
    def test_is_ndim_two(self):
        """board가 2차원 배열인가"""
        board: Board = Board()
        self.assertEqual(board.ndim, 2)

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
        self.__assert_is_board_changed(
            board=board,
            pos=(0,0),
            stone_to_put=Stone.BLACK
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

    def test_can_add_stone_on_stone(self):
        """이미 돌이 있는 칸에 돌을 올리는 경우 NotEmptyBoardError"""
        board: Board = Board()
        board.init_board[4,4] = Stone.WHITE
        
        with self.assertRaises(BoardErrors.NotEmptyBoardError):
            board[4,4] = Stone.BLACK
        
        with self.assertRaises(BoardErrors.NotEmptyBoardError):
            board[4,4] = Stone.WHITE

    def test_put_empty_error(self):
        """Stone.EMPTY를 올리는 경우 PutEmptyStoneError"""
        board: Board = Board()
        with self.assertRaises(BoardErrors.PutEmptyStoneError):
            board[3,5] = Stone.EMPTY

    def test_shape_immutable(self):
        """board.shape를 변경할 수 없어야 함"""
        board: Board = Board()
        with self.assertRaises(AttributeError):
            board.shape = (5,5)
        with self.assertRaises(TypeError):
            board.shape[0] = 5

    def test_ndim_immutable(self):
        """board.ndim을 변경할 수 없어야 함"""
        board: Board = Board()
        with self.assertRaises(AttributeError):
            board.ndim = 1

    def test_last_stone_immutable(self):
        """board.last_stone을 변경할 수 없어야 함"""
        board: Board = Board()
        with self.assertRaises(AttributeError):
            board.last_stone = Stone.WHITE
    
    def test_put_out_of_range(self):
        """board 크기 밖에 Stone을 올리는 경우 IndexError"""
        board: Board = Board()
        with self.assertRaises(IndexError):
            board[board.shape[0],0] = Stone.BLACK
        with self.assertRaises(IndexError):
            board[0,board.shape[1]] = Stone.BLACK

    def test_put_minus_position(self):
        """board의 좌표는 음수를 허용하지 않음"""
        board: Board = Board()
        with self.assertRaises(BoardErrors.MinusIndexError):
            board[-1,-3] = Stone.BLACK

    def test_put_same_stone_twice(self):
        """같은 돌을 연속해서 두는 경우 PutSameAgainError"""
        board: Board = Board()
        board[0,0] = Stone.BLACK
        
        with self.assertRaises(BoardErrors.PutSameAgainError):
            board[2,3] = Stone.WHITE
            board[2,4] = Stone.WHITE

        board[3,4] = Stone.BLACK
        board[5,4] = Stone.WHITE
        with self.assertRaises(BoardErrors.PutSameAgainError):
            board[6,3] = Stone.BLACK
            board[1,4] = Stone.BLACK

    def test_put_use_np_slicing(self):
        """슬라이싱, 행/열 할당 등으로 한번에 돌을 두는 경우 UseSliceError"""
        board: Board = Board()
        with self.assertRaises(BoardErrors.UseSliceError):
            board[1,2:5] = Stone.BLACK
            
        with self.assertRaises(BoardErrors.UseSliceError):
            board[1:3,2] = Stone.BLACK
            
        with self.assertRaises(BoardErrors.UseSliceError):
            board[1:3,2:5] = Stone.BLACK

        with self.assertRaises(BoardErrors.UseSliceError):
            board[1] = Stone.BLACK

        with self.assertRaises(BoardErrors.UseSliceError):
            board[[1,2]] = Stone.BLACK

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
        board.init_board[1,2:5] = Stone.WHITE
        board.init_board[1:3,2] = Stone.BLACK
        board.init_board[1:3,2:5] = Stone.WHITE
        board.init_board[[2,3]] = Stone.BLACK
        board.init_board[(2,3),(4,3)] = Stone.WHITE

    def test_print_board(self):
        """print(board)로 보드 보여주기"""
        self.assertFalse(True)

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
        with self.assertRaises(BoardErrors.WinError):
            board: Board = Board()
            board.init_board[idx] = Stone.WHITE
            board._Board__judge_win()
        with self.assertRaises(BoardErrors.WinError):
            board: Board = Board()
            board.init_board[idx] = Stone.BLACK
            board._Board__judge_win()

    def test_condition_to_win(self):
        """한 종류의 stone이 오목을 완성하면 WinError"""
        self.__assert_judge_win(((4,4,4,4,4),(1,2,3,4,5)))
        self.__assert_judge_win(((1,2,3,4,5),(1,1,1,1,1)))
        self.__assert_judge_win(1)
        self.__assert_judge_win((slice(15), 1))
        self.__assert_judge_win((slice(1,6), 1))
        self.__assert_judge_win((1, slice(1,6)))
        self.__assert_judge_win((slice(1,6), slice(1,6)))
        self.__assert_judge_win([1,2,0])

        self.__assert_judge_win(((1,2,3,4,5),(1,2,3,4,5)))
        self.__assert_judge_win(((1,2,3,4,5),(5,4,3,2,1)))
        board: Board = Board()
        board.init_board[(1,2,3,4,5),(5,4,3,2,1)] = Stone.WHITE
        board.init_board[3,3] = Stone.BLACK
        board._Board__judge_win()

    def test_black_first(self):
        """마지막으로 둔 수가 EMPTY일때 WHITE가 두면 BlackFirstError"""
        board: Board = Board()
        with self.assertRaises(BoardErrors.BlackFirstError):
            board[5,5] = Stone.WHITE

    def test_play(self):
        """설정한 오목 규칙으로 플레이가 가능한지 테스트"""
        board: Board = Board()
        board[5,5] = Stone.BLACK
        board[6,5] = Stone.WHITE
        board[6,6] = Stone.BLACK
        board[5,6] = Stone.WHITE
        board[7,7] = Stone.BLACK
        board[8,8] = Stone.WHITE
        board[4,4] = Stone.BLACK
        board[4,7] = Stone.WHITE
        with self.assertRaises(BoardErrors.WinError):
            board[3,3] = Stone.BLACK

    def test_viewcopy_integrity(self):
        """board.viewcopy() 값을 변경해도 원본에 영향이 없는지 확인"""
        board: Board = Board()
        arr: np.ndarray = board.viewcopy()
        arr[3] = Stone.BLACK
        self.assertTrue((board[:] == Stone.EMPTY).all())

    def test_deepcopy_integrity(self):
        """board.deepcopy() 기능이 board에 대해 깊은 복사인지 확인"""
        board: Board = Board()
        boardcopy: Board = board.deepcopy()
        self.assertTrue((boardcopy.viewcopy() == board.viewcopy()).all())
        boardcopy.init_board[3] = Stone.BLACK
        self.assertFalse((boardcopy.viewcopy() == board.viewcopy()).all())


class TestOmokAi(unittest.TestCase):
    def test_has_its_color_var(self):
        """어떤 Stone을 본인의 수로 계산할지 설정할 수 있어야 함"""
        board: Board = Board()
        ai: OmokAi = OmokAi(board, Stone.BLACK)
        self.assertIsInstance(ai.mystone, Stone)

    def test_has_empty_mystone(self):
        """Stone.EMPTY를 ai.mystone으로 가질 수 없음"""
        board: Board = Board()
        with self.assertRaises(OmokAiErrors.EmptyMystoneError):
            OmokAi(board, Stone.EMPTY)
        
    def test_is_scoring_system_readonly(self):
        """내부 점수 시스템은 외부에서 읽을 수만 있고 변경이 불가해야 함"""
        board: Board = Board()
        ai: OmokAi = OmokAi(board, Stone.BLACK)
        self.assertIsNotNone(ai.view_scoreboard)
        
        ai.view_scoreboard[0,0] = 100
        self.assertNotEqual(ai.view_scoreboard[0,0], 100)

    def test_has_scoingboard_same_shape_with_Board(self):
        """scoreboard는 보드와 같은 shape을 가져야 함"""
        board: Board = Board()
        ai: OmokAi = OmokAi(board, Stone.BLACK)
        self.assertEqual(ai.view_scoreboard.shape, board.shape)

    def untest_has_output_to_board(self):
        """스스로 보드에 착수할 수 있어야 함"""
        board: Board = Board()
        ai: OmokAi = OmokAi(board, Stone.BLACK)
        boardcopy = board.deepcopy()
        self.assertTrue((boardcopy.viewcopy() == board.viewcopy()).all())
        ai.put_stone()
        self.assertFalse((boardcopy.viewcopy() == board.viewcopy()).all())

    def test_no_changed_board(self):
        """ai.put_stone()이 돌을 착수하지 않을 경우 NoStoneChangedError"""
        board: Board = Board()
        ai_b: OmokAi = OmokAi(board, Stone.BLACK)
        ai_w: OmokAi = OmokAi(board, Stone.WHITE)

        with self.assertRaises(OmokAiErrors.NoStoneChangedError):
            for _ in range(5):
                ai_b.put_stone()
                ai_w.put_stone()

    def test_basic_scoring(self):
        """해당 줄에서 돌이 연속된 정도에 비례해 점수 부여"""
        board: Board = Board()
        ai_b: OmokAi = OmokAi(board, Stone.BLACK)
        board.init_board[7,7] = Stone.BLACK
        ai_b.scoring()
        print(board)
        print(ai_b)
        self.assertTrue((ai_b.view_scoreboard[(5,6,8,9),(5,6,8,9)] == ai_b.unit).all())
        self.assertTrue((ai_b.view_scoreboard[(5,6,8,9),(9,8,6,5)] == ai_b.unit).all())
        self.assertTrue((ai_b.view_scoreboard[(7,7,7,7),(5,6,8,9)] == ai_b.unit).all())
        self.assertTrue((ai_b.view_scoreboard[(5,6,8,9),(7,7,7,7)] == ai_b.unit).all())

        board.init_board[7,8] = Stone.BLACK
        ai_b.scoring()
        print(board)
        print(ai_b)
        
        self.assertTrue((ai_b.view_scoreboard[(7,7,7,7),(5,6,9,10)] == ai_b.unit*2).all())
        self.assertTrue((ai_b.view_scoreboard[(6,6,8,8),(7,8,7,8)] == ai_b.unit*2).all())
        self.assertTrue((ai_b.view_scoreboard[(6,8,6,8),(6,6,9,9)] == ai_b.unit).all())
        self.assertTrue((ai_b.view_scoreboard[(5,5,5,5,5,5),(5,6,7,8,9,10)] == ai_b.unit).all())
        self.assertTrue((ai_b.view_scoreboard[(9,9,9,9,9,9),(5,6,7,8,9,10)] == ai_b.unit).all())

    
    def test_can_follow_rule(self):
        """Board의 룰에 어긋나지 않는 착수를 해야 함"""
        board: Board = Board()
        ai_b: OmokAi = OmokAi(board, Stone.BLACK)
        ai_w: OmokAi = OmokAi(board, Stone.WHITE)
        
        print()

        for i in range(4):
            ai_b.put_stone()
            ai_w.put_stone()
            print(i)
        self.assertFalse(True)

if __name__ == "__main__":
    unittest.main()