from typing import NamedTuple


class Vec2(NamedTuple):
    x: int
    y: int


def vec_add(a: Vec2, b: Vec2) -> Vec2:
    return Vec2(a.x + b.x, a.y + b.y)


def vec_scalar_multiply(a: Vec2, b: int) -> Vec2:
    return Vec2(a.x * b, a.y * b)


def vec_invert(a: Vec2) -> Vec2:
    return Vec2(a.x * -1, a.y * -1)
