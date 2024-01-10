from modules.visualizer.main import Visualizer
from modules.halfedge import HalfEdge
from modules.vertex import Vertex
from modules.beachline import Beachline
from queue import PriorityQueue
from modules.site import Site
from modules.vector2d import Vector2d
from modules.event import Event
from modules.arc import Arc
from modules.diagram import Diagram
from math import inf
from modules.box import Box


class Fortune:

    def __init__(self, points: tuple[int, int]) -> None:
        self.BL = Beachline()
        self.EQ = PriorityQueue()
        tab = []
        for x, y in points:
            tab.append(Vector2d(x=x, y=y))
        self.diagram = Diagram(tab)
        self.sweepline = 0

    @property
    def vertices(self):
        return self.diagram.vertices

    @property
    def edges(self):
        return self.diagram.halfEdges

    @property
    def faces(self):
        return self.diagram.faces

    def run(self, visualize: bool = False, box: Box = None, vis: Visualizer = None):
        for site in self.diagram.sites:
            self.EQ.put(Event(type=Event.SITE, site=site))
        while not self.EQ.empty():
            event: Event = self.EQ.get()
            if event.type == Event.CIRCLE and event.active:
                self.sweepline = event.y_to_comp
                self.handleCircleEvent(event)
                if visualize and box is not None and vis is not None:
                    self.diagram.drawStep(
                        box=box, sweepline=self.sweepline, vis=vis, BL=self.BL, message=f"Zdarzenie kołowe w punkcie {event.site.point}")
            elif event.type == Event.SITE:
                self.sweepline = event.site.point.y
                self.handleSiteEvent(event)
                if visualize and box is not None and vis is not None:
                    self.diagram.drawStep(
                        box=box, sweepline=self.sweepline, vis=vis, BL=self.BL, message=f"Zdarzenie punktowe w punkcie {event.site.point}")
        if visualize and box is not None and vis is not None:
            self.diagram.drawResult(box, vis, self.BL, False).show()

    def handleSiteEvent(self, event: Event):
        if self.BL.isEmpty:
            arc = self.BL.createArc(event.site)
            self.BL.setRoot(arc)
            self.diagram.arcs.append(arc)
            return
        arcToBreak: Arc = self.BL.locateArcAbove(
            event.site.point, self.sweepline)
        if arcToBreak.event is not None:
            arcToBreak.event.remove()

        middleArc = self.breakArc(arcToBreak, event.site)
        leftArc = middleArc.prev
        rightArc = middleArc.next
        self.diagram.arcs.append(middleArc)
        self.diagram.arcs.append(leftArc)
        self.diagram.arcs.append(rightArc)

        self.addEdge(leftArc, middleArc)
        middleArc.rightHalfEdge = middleArc.leftHalfEdge
        rightArc.leftHalfEdge = leftArc.rightHalfEdge

        if leftArc.prev is not self.BL.guardian:
            self.addEvent(leftArc.prev, leftArc, middleArc)

        if rightArc.next is not self.BL.guardian:
            self.addEvent(middleArc, rightArc, rightArc.next)

    def handleCircleEvent(self, event: Event):
        current_point: Vector2d = event.site.point
        arc: Arc = event.arc

        vertex: Vertex = self.diagram.createVertex(current_point)

        leftArc = arc.prev
        rightArc = arc.next

        if leftArc.event is not None:
            leftArc.event.remove()

        if rightArc.event is not None:
            rightArc.event.remove()

        self.removeArc(arc, vertex)

        self.diagram.circle = (current_point, event.radius)

        if leftArc.prev is not self.BL.guardian:
            self.addEvent(leftArc.prev, leftArc, rightArc)

        if rightArc.next is not self.BL.guardian:
            self.addEvent(leftArc, rightArc, rightArc.next)

    def breakArc(self, arc: Arc, site: Site):
        middleArc = self.BL.createArc(site)
        leftArc = self.BL.createArc(arc.site, Arc.LEFT)
        leftArc.leftHalfEdge = arc.leftHalfEdge
        rightArc = self.BL.createArc(arc.site, Arc.RIGHT)
        rightArc.rightHalfEdge = arc.rightHalfEdge

        self.BL.replace(arc, middleArc)
        self.BL.insertBefore(middleArc, leftArc)
        self.BL.insertAfter(middleArc, rightArc)

        self.diagram.arcs.remove(arc)
        del arc

        return middleArc

    def removeArc(self, arc: Arc, vertex: Vertex):
        self.setDestination(arc.prev, arc, vertex)
        self.setDestination(arc, arc.next, vertex)

        arc.leftHalfEdge.next = arc.rightHalfEdge
        arc.rightHalfEdge.prev = arc.leftHalfEdge

        self.BL.remove(arc)

        prevHalfEdge = arc.prev.rightHalfEdge
        nextHalfEdge = arc.next.leftHalfEdge

        self.addEdge(arc.prev, arc.next)
        self.setOrigin(arc.prev, arc.next, vertex)

        self.setPrevHalfEdge(arc.prev.rightHalfEdge, prevHalfEdge)
        self.setPrevHalfEdge(nextHalfEdge, arc.next.leftHalfEdge)

        self.diagram.arcs.remove(arc)

        del arc

    def addEdge(self, left: Arc, right: Arc):
        left.rightHalfEdge = self.diagram.createHalfEdge(left.site.face)
        right.leftHalfEdge = self.diagram.createHalfEdge(right.site.face)

        left.rightHalfEdge.twin = right.leftHalfEdge
        right.leftHalfEdge.twin = left.rightHalfEdge

    def setOrigin(self, left: Arc, right: Arc, vertex: Vertex):
        left.rightHalfEdge.destination = vertex
        right.leftHalfEdge.origin = vertex

    def setDestination(self, left: Arc, right: Arc, vertex: Vertex):
        left.rightHalfEdge.origin = vertex
        right.leftHalfEdge.destination = vertex

    def setPrevHalfEdge(self, prev: HalfEdge, next: HalfEdge):
        prev.next = next
        next.prev = prev

    def isMovingRight(self, left: Arc, right: Arc):
        return left.site.point.y < right.site.point.y

    def getInitialX(self, left: Arc, right: Arc, movingRight: bool):
        return left.site.point.x if movingRight else right.site.point.x

    def addEvent(self, left: Arc, middle: Arc, right: Arc):
        convergencePoint, radius, lowestPoint = self.computeConvergencePoint(
            left.site.point, middle.site.point, right.site.point)

        if lowestPoint - Beachline.eps > self.sweepline:
            return

        leftBreakpointMovingRight = self.isMovingRight(left, middle)
        rightBreakpointMovingRight = self.isMovingRight(middle, right)
        leftInitialX = self.getInitialX(
            left, middle, leftBreakpointMovingRight)
        rightInitialX = self.getInitialX(
            middle, right, rightBreakpointMovingRight)
        if (not (not leftBreakpointMovingRight and rightBreakpointMovingRight) and
            ((leftBreakpointMovingRight and leftInitialX <= convergencePoint.x) or
            (not leftBreakpointMovingRight and leftInitialX >= convergencePoint.x)) and
            ((rightBreakpointMovingRight and rightInitialX <= convergencePoint.x) or
                (not rightBreakpointMovingRight and rightInitialX >= convergencePoint.x))):
            event = Event(type=Event.CIRCLE, site=Site(
                point=convergencePoint), lowest=lowestPoint, arc=middle, radius=radius)
            middle.event = event
            self.EQ.put(event)

    def computeConvergencePoint(self, point1: Vector2d, point2: Vector2d, point3: Vector2d):
        v1 = (point1-point2).orthogonal
        v2 = (point2 - point3).orthogonal
        delta = (point3-point1).mulByScalar(0.5)
        denom = v1.det(v2)

        if abs(denom) <= Beachline.eps:
            return Vector2d(inf, inf), 0, inf

        t = delta.det(v2) / denom
        center = (point1 + point2).mulByScalar(0.5) + v1.mulByScalar(t)
        r = (center - point1).norm
        lowestPoint = center.y - r
        return center, r, lowestPoint
