from modules.vector2d import Vector2d


class Site:
    def __init__(self, point: Vector2d, face=None, index=None) -> None:
        self.point = point
        self.face = face
        self.index = index
