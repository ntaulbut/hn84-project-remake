from unittest import TestCase

from battleships import SquareState, new_board, decode_notation
from vec2 import Vec2


class Test(TestCase):
    def test_new_board(self):
        assert new_board(SquareState.EMPTY, 3, 2) == [
            [SquareState.EMPTY, SquareState.EMPTY],
            [SquareState.EMPTY, SquareState.EMPTY],
            [SquareState.EMPTY, SquareState.EMPTY],
        ]

    def test_decode_notation(self):
        board = new_board(SquareState.EMPTY, 7, 7)
        assert decode_notation("a0", board) == Vec2(0, 0)
        assert decode_notation("c4", board) == Vec2(4, 2)
        assert decode_notation("C4", board) == Vec2(4, 2)
        assert decode_notation("z4", board) is None
        assert decode_notation("c9", board) is None
        assert decode_notation("", board) is None
        assert decode_notation("***", board) is None
        assert decode_notation("4c", board) is None
