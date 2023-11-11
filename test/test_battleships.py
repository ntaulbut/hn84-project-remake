import unittest
from vec2 import Vec2
from battleships.battleships import SquareState, new_board, decode_notation


class MyTestCase(unittest.TestCase):
    def test_new_board(self):
        self.assertEqual(
            new_board(SquareState.EMPTY, 3, 2),
            [
                [SquareState.EMPTY, SquareState.EMPTY],
                [SquareState.EMPTY, SquareState.EMPTY],
                [SquareState.EMPTY, SquareState.EMPTY],
            ],
        )

    def test_decode_notation(self):
        board = new_board(SquareState.EMPTY, 7, 7)
        self.assertEqual(decode_notation("a0", board), Vec2(0, 0))
        self.assertEqual(decode_notation("c4", board), Vec2(4, 2))
        self.assertEqual(decode_notation("C4", board), Vec2(4, 2))
        self.assertEqual(decode_notation("z4", board), None)
        self.assertEqual(decode_notation("c9", board), None)
        self.assertEqual(decode_notation("", board), None)
        self.assertEqual(decode_notation("***", board), None)
        self.assertEqual(decode_notation("4c", board), None)


if __name__ == "__main__":
    unittest.main()
