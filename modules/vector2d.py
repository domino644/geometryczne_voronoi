from math import sqrt


class Vector2d:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2d(self.x + other.x, self.y+other.y)

    def __sub__(self, other):
        return Vector2d(self.x - other.x, self.y-other.y)

    def mulByScalar(self, scalar):
        return Vector2d(self.x*scalar, self.y * scalar)

    def det(self, other):
        return self.x*other.y - self.y*other.x

    def asTuple(self):
        return (self.x, self.y)

    @property
    def orthogonal(self):
        return Vector2d(-self.y, self.x)

    @property
    def norm(self):
        return sqrt(self.x*self.x+self.y*self.y)

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"
