from unittest import TestCase

from vec2 import vec_add, Vec2, vec_invert, vec_scalar_multiply


class Test(TestCase):
    def test_vec_add(self):
        assert vec_add(Vec2(1, 2), Vec2(1, 2)) == Vec2(2, 4)
        assert vec_add(Vec2(-1, -2), Vec2(1, 2)) == Vec2(0, 0)
        assert vec_add(Vec2(1, 2), Vec2(0, 0)) == Vec2(1, 2)

    def test_vec_scalar_multiply(self):
        assert vec_scalar_multiply(Vec2(2, 3), 3) == Vec2(6, 9)
        assert vec_scalar_multiply(Vec2(2, 3), 0) == Vec2(0, 0)
        assert vec_scalar_multiply(Vec2(0, 0), 3) == Vec2(0, 0)
        assert vec_scalar_multiply(Vec2(2, 3), -2) == Vec2(-4, -6)
        assert vec_scalar_multiply(Vec2(-2, -3), 1) == Vec2(-2, -3)

    def test_vec_invert(self):
        assert vec_invert(Vec2(5, 9)) == Vec2(-5, -9)
        assert vec_invert(Vec2(0, 0)) == Vec2(0, 0)
        assert vec_invert(Vec2(-1, 2)) == Vec2(1, -2)
