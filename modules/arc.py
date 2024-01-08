from modules.event import Event
from modules.site import Site


class Arc:
    RED = 0
    BLACK = 1
    
    LEFT = 2
    RIGHT = 3

    def __init__(self) -> None:
        self.parent: Arc = None
        self.left: Arc = None
        self.right: Arc = None

        self.site: Site = None
        self.leftHalfEdge = None
        self.rightHalfEdge = None
        self.event: Event = None

        self.prev: Arc = None
        self.next: Arc = None

        self.color = None
        self.side = None

    def get_plot(self, x, sweepline):
        i = self.site.point

        if i.y - sweepline == 0:
            return None

        u = 2 * (i.y - sweepline)

        v = (x ** 2 - 2 * i.x * x + i.x ** 2 + i.y ** 2 - sweepline ** 2)
        y = v/u

        return x, y

    def __repr__(self) -> str:
        return f"Arc, {self.site.point}"

    def __str__(self) -> str:
        return f"Arc, {self.site.point}"
