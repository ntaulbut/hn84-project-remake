import unittest

from vec2 import Vec2, vec_add, vec_invert


class MyTestCase(unittest.TestCase):
    def test_vec_add(self):
        self.assertEqual(vec_add(Vec2(1, 2), Vec2(1, 2)), Vec2(2, 4))
        self.assertEqual(vec_add(Vec2(-1, -2), Vec2(1, 2)), Vec2(0, 0))
        self.assertEqual(vec_add(Vec2(1, 2), Vec2(0, 0)), Vec2(1, 2))

    def test_vec_invert(self):
        self.assertEqual(vec_invert(Vec2(5, 9)), Vec2(-5, -9))
        self.assertEqual(vec_invert(Vec2(0, 0)), Vec2(0, 0))
        self.assertEqual(vec_invert(Vec2(-1, 2)), Vec2(1, -2))


if __name__ == "__main__":
    unittest.main()
