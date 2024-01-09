from modules.vector2d import Vector2d
from math import inf
from modules.intersection import Intersection


class Box:

    def __init__(self, left, right, top, bottom) -> None:
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom

    def contains(self, point: Vector2d):
        return self.left <= point.x <= self.right and self.bottom <= point.y <= self.top

    def getIntersection(self, origin: Vector2d, direction: Vector2d):
        intersection = Intersection()
        t = inf
        k = inf
        if direction.x > 0:
            t = (self.right - origin.x) / direction.x
            intersection.point = direction.mulByScalar(t) + origin
        elif (direction.x < 0):
            t = (self.left - origin.x) / direction.x
            intersection.point = direction.mulByScalar(t) + origin
        if direction.y > 0:
            k = (self.top - origin.y) / direction.y
            if k < t:
                intersection.point = direction.mulByScalar(k) + origin
        elif direction.y < 0:
            k = (self.bottom - origin.y) / direction.y
            if (k < t):
                intersection.point = direction.mulByScalar(k) + origin

        return intersection
