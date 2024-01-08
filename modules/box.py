from modules.vector2d import Vector2d
from math import inf


class Intersection:
    def __init__(self, point: Vector2d = None, side=None) -> None:
        self.point = point
        self.side = side


class Box:
    LEFT = 0
    BOTTOM = 1
    RIGHT = 2
    TOP = 3

    def __init__(self, left, right, top, bottom) -> None:
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom

    def contains(self, point: Vector2d):
        return self.left <= point.x <= self.right and self.bottom <= point.y <= self.top

    def getFirstIntersection(self, origin: Vector2d, direction: Vector2d):

        intersection = Intersection()
        t = inf
        k = inf
        if direction.x > 0:
            t = (self.right - origin.x) / direction.x
            intersection.side = Box.RIGHT
            intersection.point = direction.mulByScalar(t) + origin
        elif (direction.x < 0):
            t = (self.left - origin.x) / direction.x
            intersection.side = Box.LEFT
            intersection.point = direction.mulByScalar(t) + origin
        if direction.y > 0:
            k = (self.top - origin.y) / direction.y
            if k < t:
                intersection.side = Box.TOP
                intersection.point = direction.mulByScalar(k) + origin
        elif direction.y < 0:
            k = (self.bottom - origin.y) / direction.y
            if (k < t):
                intersection.side = Box.BOTTOM
                intersection.point = direction.mulByScalar(k) + origin

        return intersection

    # def getIntersections(self, origin: Vector2d, destination: Vector2d, left_bound: float, right_bound: float):
    #     direction = destination - origin
    #     t = [inf, inf]
    #     i = 0
    #     intersections: list[Intersection] = [None, None]

    #     if origin.x < self.left or destination.x < self.left:
    #         if direction.x != 0:
    #             t[i] = (self.left - origin.x)/direction.x
    #             if left_bound < t[i] < right_bound:
    #                 intersections[i] = Intersection(
    #                     side=Box.LEFT, point=direction.mulByScalar(t[i]) + origin)
    #                 if self.bottom <= intersections[i].point.y <= self.top:
    #                     i += 1
    #         else:
    #             t[i] = self.left - origin.x
    #             intersections[i] = Intersection(
    #                 side=Box.LEFT, point=Vector2d(self.left, origin.y))
    #             if self.bottom <= intersections[i].point.y <= self.top:
    #                 i += 1

    #     if origin.x > self.right or destination.x > self.right:
    #         if direction.x != 0:
    #             t[i] = (self.right - origin.x) / direction.x
    #             if left_bound < t[i] < right_bound:
    #                 intersections[i] = Intersection(
    #                     side=Box.RIGHT, point=direction.mulByScalar(t[i]) + origin)
    #                 if self.bottom <= intersections[i].point.y <= self.top:
    #                     i += 1
    #         else:
    #             t[i] = self.right - origin.x
    #             intersections[i] = Intersection(
    #                 side=Box.RIGHT, point=Vector2d(self.right, origin.y))
    #             if self.bottom <= intersections[i].point.y <= self.top:
    #                 i += 1

    #     if origin.y < self.bottom or destination.y < self.bottom:
    #         if direction.y != 0:
    #             t[i] = (self.bottom - origin.y) / direction.y
    #             if i < 2 and (left_bound < t[i] < right_bound):
    #                 intersections[i] = Intersection(
    #                     side=Box.BOTTOM, point=direction.mulByScalar(t[i]) + origin)
    #                 if self.left <= intersections[i].point.x <= self.right:
    #                     i += 1
    #         elif i < 2:
    #             t[i] = self.bottom - origin.y
    #             intersections[i] = Intersection(
    #                 side=Box.BOTTOM, point=Vector2d(origin.x, self.BOTTOM))
    #             if self.left <= intersections[i].point.x <= self.right:
    #                 i += 1

    #     if origin.y > self.top or destination.y > self.top:
    #         if direction.y != 0:
    #             t[i] = (self.top - origin.y) / direction.y
    #             if i < 2 and (left_bound < t[i] < right_bound):
    #                 intersections[i] = Intersection(
    #                     side=Box.TOP, point=direction.mulByScalar(t[i])+origin)
    #                 if self.left <= intersections[i].point.x <= self.right:
    #                     i += 1
    #         elif i < 2:
    #             t[i] = self.top - origin.y
    #             intersections[i] = Intersection(
    #                 side=Box.TOP, point=Vector2d(origin.x, self.TOP))
    #             if self.left <= intersections[i].point.x <= self.right:
    #                 i += 1

    #     if i == 2 and t[0] > t[1]:
    #         intersections[0], intersections[1] = intersections[1], intersections[0]

    #     return i, intersections

    def getCoordinates(self):
        return ((self.left, self.bottom), (self.right, self.bottom), (self.right, self.top), (self.left, self.top))
