from modules.arc import Arc
from modules.site import Site
from modules.vector2d import Vector2d
from math import sqrt, inf


class Beachline:
    eps = 10**-9

    def __init__(self) -> None:
        self.guardian = Arc()
        self.guardian.color = Arc.BLACK
        self.root = self.guardian

    def createArc(self, site: Site, side=Arc.LEFT):
        a = Arc()
        a.site = site
        a.color = Arc.RED
        a.left = self.guardian
        a.right = self.guardian
        a.next = self.guardian
        a.prev = self.guardian
        a.parent = self.guardian
        a.side = side
        return a

    @property
    def isEmpty(self):
        return self.root is self.guardian

    def setRoot(self, x: Arc):
        self.root = x
        self.root.color = Arc.BLACK

    def getMostLeft(self):
        x = self.root
        while x.prev is not self.guardian:
            x = x.prev
        return x

    def minimum(self, x: Arc):
        while x.left is not self.guardian:
            x = x.left
        return x

    def leftRotate(self, x: Arc):
        y: Arc = x.right
        x.right = y.left
        if y.left is not self.guardian:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is self.guardian:
            self.root = y
        elif x.parent.left == x:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def rightRotate(self, y: Arc):
        x = y.left
        y.left = x.right
        if x.right is not self.guardian:
            x.right.parent = y
        x.parent = y.parent
        if y.parent is self.guardian:
            self.root = x
        elif y.parent.left == y:
            y.parent.left = x
        else:
            y.parent.right = x
        x.right = y
        y.parent = x

    def removeFixup(self, x: Arc):
        while x is not self.root and x.color == Arc.BLACK:
            if x == x.parent.left:
                w = x.parent.right
                if w.color == Arc.RED:
                    w.color = Arc.BLACK
                    x.parent.color = Arc.RED
                    self.leftRotate(x.parent)
                    w = x.parent.right
                if w.left.color == Arc.BLACK and w.right.color == Arc.BLACK:
                    w.color = Arc.RED
                    x = x.parent
                else:
                    if w.right.color == Arc.BLACK:
                        w.left.color = Arc.BLACK
                        w.color = Arc.RED
                        self.rightRotate(w)
                        w = x.parent.right
                    w.color = x.parent.color
                    x.parent.color = Arc.BLACK
                    w.right.color = Arc.BLACK
                    self.leftRotate(x.parent)
                    x = self.root
            else:
                w = x.parent.left

                if w.color == Arc.RED:
                    w.color = Arc.BLACK
                    x.parent.color = Arc.RED
                    self.rightRotate(x.parent)
                    w = x.parent.left
                if w.left.color == Arc.BLACK and w.right.color == Arc.BLACK:
                    w.color = Arc.RED
                    x = x.parent
                else:
                    if w.left.color == Arc.BLACK:
                        w.right.color = Arc.BLACK
                        w.color = Arc.RED
                        self.leftRotate(w)
                        w = x.parent.left
                    w.color = x.parent.color
                    x.parent.color = Arc.BLACK
                    w.left.color = Arc.BLACK
                    self.rightRotate(x.parent)
                    x = self.root
        x.color = Arc.BLACK

    def insertFixup(self, z):
        while z.parent.color == Arc.RED:
            if z.parent == z.parent.parent.left:
                y = z.parent.parent.right
                if y.color == Arc.RED:
                    z.parent.color = Arc.BLACK
                    y.color = Arc.BLACK
                    z.parent.parent.color = Arc.RED
                    z = z.parent.parent
                else:
                    if z == z.parent.right:
                        z = z.parent
                        self.leftRotate(z)
                    z.parent.color = Arc.BLACK
                    z.parent.parent.color = Arc.RED
                    self.rightRotate(z.parent.parent)
            else:
                y = z.parent.parent.left
                if y.color == Arc.RED:
                    z.parent.color = Arc.BLACK
                    y.color = Arc.BLACK
                    z.parent.parent.color = Arc.RED
                    z = z.parent.parent
                else:
                    if z == z.parent.left:
                        z = z.parent
                        self.rightRotate(z)
                    z.parent.color = Arc.BLACK
                    z.parent.parent.color = Arc.RED
                    self.leftRotate(z.parent.parent)
        self.root.color = Arc.BLACK

    def transplant(self, u: Arc, v: Arc):
        if u.parent is self.guardian:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def insertBefore(self, x: Arc, y: Arc):
        if x.left is self.guardian:
            x.left = y
            y.parent = x
        else:
            x.prev.right = y
            y.parent = x.prev
        y.prev = x.prev
        if y.prev is not self.guardian:
            y.prev.next = y
        y.next = x
        x.prev = y
        self.insertFixup(y)

    def insertAfter(self, x: Arc, y: Arc):
        if x.right is self.guardian:
            x.right = y
            y.parent = x
        else:
            x.next.left = y
            y.parent = x.next
        y.next = x.next
        if y.next is not self.guardian:
            y.next.prev = y
        y.prev = x
        x.next = y

        self.insertFixup(y)

    def replace(self, x: Arc, y: Arc):
        self.transplant(x, y)
        y.left = x.left
        y.right = x.right
        if y.left is not self.guardian:
            y.left.parent = y
        if y.right is not self.guardian:
            y.right.parent = y
        y.prev = x.prev
        y.next = x.next
        if y.prev is not self.guardian:
            y.prev.next = y
        if y.next is not self.guardian:
            y.next.prev = y
        y.color = x.color

    def remove(self, z: Arc):
        y = z
        yOriginalColor = y.color
        x: Arc = self.guardian
        if z.left is self.guardian:
            x = z.right
            self.transplant(z, z.right)
        elif z.right is self.guardian:
            x = z.left
            self.transplant(z, z.left)
        else:
            y = self.minimum(z.right)
            yOriginalColor = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self.transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
            self.transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        if yOriginalColor == Arc.BLACK:
            self.removeFixup(x)
        if z.prev is not self.guardian:
            z.prev.next = z.next
        if z.next is not self.guardian:
            z.next.prev = z.prev

    @staticmethod
    def computeBreakpoint(point1: Vector2d, point2: Vector2d, sweepline: float, side):
        x1 = point1.x
        y1 = point1.y
        x2 = point2.x
        y2 = point2.y
        if abs(y1-y2) <= Beachline.eps:
            if x1 < x2:
                return (x1+x2)/2
            else:
                return -inf if side == Arc.LEFT else inf

        if abs(y1 - sweepline) <= Beachline.eps:
            return x1
        if abs(y2 - sweepline) <= Beachline.eps:
            return x2
        d1 = 1 / (2*(y1 - sweepline))
        d2 = 1 / (2*(y2 - sweepline))
        a = d1 - d2
        b = 2 * (x2 * d2 - x1 * d1)
        c = (y1 * y1 + x1 * x1 - sweepline*sweepline) * \
            d1 - (y2*y2 + x2*x2 - sweepline*sweepline) * d2
        delta = b*b - 4*a*c
        return (-b + sqrt(delta)) / (2*a)

    def locateArcAbove(self, point: Vector2d, sweepLine: float):
        node = self.root
        while True:
            bp_left = -inf
            bp_right = inf
            if node.prev is not self.guardian:
                bp_left = Beachline.computeBreakpoint(
                    node.prev.site.point, node.site.point, sweepLine, node.prev.side)
            if node.next is not self.guardian:
                bp_right = Beachline.computeBreakpoint(
                    node.site.point, node.next.site.point, sweepLine, node.next.side)
            if point.x < bp_left:
                node = node.left
            elif point.x > bp_right:
                node = node.right
            else:
                break
        return node

    def printTree(self, node: Arc, level=0):
        if node is not self.guardian:
            self.printTree(node.left, level+1)
            print(' ' * 4 * level + '-> ' + str(node.site.point))
            self.printTree(node.right, level+1)
