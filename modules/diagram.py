from modules.visualizer.figures.circle import Circle
from modules.visualizer.figures.line_segment import LineSegment
from modules.visualizer.figures.parabola import Parabola
from modules.visualizer.main import Visualizer
from modules.arc import Arc
from modules.beachline import Beachline
from modules.face import Face
from modules.halfedge import HalfEdge
from modules.vector2d import Vector2d
from modules.box import Box, Intersection
from modules.site import Site
from modules.vertex import Vertex
import numpy as np


class Diagram:
    def __init__(self, points) -> None:
        self.halfEdges: list[HalfEdge] = []
        self.vertices: list[Vertex] = []
        self.faces: list[Face] = []
        self.sites: list[Site] = []
        for i, point in enumerate(points):
            self.sites.append(Site(index=i, point=point, face=None))
            self.faces.append(Face(site=self.sites[-1], outerComponent=None))
            self.sites[-1].face = self.faces[-1]
        self.arcs: list[Arc] = []
        self.visibleParabolas: list[Parabola] = []
        self.visibleHalfEdges: list[LineSegment] = []
        self.visibleHalfEdgesCoord: list[tuple[tuple]] = []
        self.visibleSweepline: LineSegment = None
        self.circle: tuple[Vector2d, float] = None
        self.visibleCircle: Circle = None

    def createHalfEdge(self, face: Face):
        he = HalfEdge()
        he.incidentFace = face
        if face.outerComponent is None:
            face.outerComponent = he
        self.halfEdges.append(he)
        return he

    def createVertex(self, point: Vector2d, add: bool = True):
        vertex: Vertex = Vertex(point=point)
        if add:
            self.vertices.append(vertex)
        return vertex

    def drawResult(self, box: Box, visualizer: Visualizer, BL: Beachline, drawVertices: bool, title: str = "Diagram końcowy"):
        visualizer.clear()
        for site in self.sites:
            box.left = min(box.left, site.point.x)
            box.right = max(box.right, site.point.x)
            box.top = max(box.top, site.point.y)
            box.bottom = min(box.bottom, site.point.y)
            visualizer.add_point(site.point.asTuple(), color='blue', s=2)

        if not BL.isEmpty:
            arc: Arc = BL.getMostLeft()
            while arc.next is not BL.guardian:
                left: Arc = arc
                right: Arc = arc.next

                direction = (left.site.point -
                             right.site.point).orthogonal
                origin = (left.site.point +
                          right.site.point).mulByScalar(0.5)
                intersection: Intersection = box.getFirstIntersection(
                    origin, direction)
                vertex = self.createVertex(intersection.point, add=False)

                left.rightHalfEdge.origin = vertex
                right.leftHalfEdge.destination = vertex
                arc = arc.next
        if drawVertices:
            for vertex in self.vertices:
                if box.contains(vertex.point):
                    visualizer.add_point(
                        vertex.point.asTuple(), color="green")

        visualizer.add_line_segment(
            ((box.left, box.bottom), (box.right, box.bottom)))
        visualizer.add_line_segment(
            ((box.left, box.top), (box.right, box.top)))
        visualizer.add_line_segment(
            ((box.left, box.bottom), (box.left, box.top)))
        visualizer.add_line_segment(
            ((box.right, box.top), (box.right, box.bottom)))

        for site in self.sites:
            face = site.face
            halfEdge: halfEdge = face.outerComponent
            if halfEdge is None:
                continue
            while halfEdge.prev is not None:
                halfEdge = halfEdge.prev
                if halfEdge == face.outerComponent:
                    break
            start = halfEdge
            while halfEdge is not None:
                if halfEdge.origin is not None and halfEdge.destination is not None:
                    origin: Vector2d = halfEdge.origin.point
                    destination: Vector2d = halfEdge.destination.point
                    originInside = box.contains(origin)
                    destinationInside = box.contains(
                        destination)
                    if originInside and destinationInside:
                        visualizer.add_line_segment(
                            (origin.asTuple(), destination.asTuple()))
                    elif originInside and not destinationInside:
                        direction = destination - origin
                        intersection = box.getFirstIntersection(
                            origin, direction)
                        visualizer.add_line_segment(
                            (origin.asTuple(), intersection.point.asTuple()))
                    elif not originInside and destinationInside:
                        direction = origin - destination
                        intersection = box.getFirstIntersection(
                            destination, direction)
                        visualizer.add_line_segment(
                            (destination.asTuple(), intersection.point.asTuple()))
                halfEdge = halfEdge.next
                if halfEdge == start:
                    break
        visualizer.add_title(title)
        return visualizer

    def drawStep(self, box: Box, sweepline: float, vis: Visualizer, BL: Beachline, message: str = ""):
        vis.clear()
        if self.circle is not None:
            self.drawSites(vis)
            self.drawSweepline(sweepline, box, vis)
            self.drawArcs(box, sweepline, vis, BL)
            self.drawCircle(self.circle[0], self.circle[1], vis, box)
            self.drawVertices(box, vis)
            self.drawHalfEdges(box, vis)
        else:
            self.drawSweepline(sweepline=sweepline, box=box, vis=vis)
            self.drawVertices(box, vis)
            self.drawSites(vis)
            self.drawArcs(box, sweepline, vis, BL)
            self.drawHalfEdges(box, vis)
        vis.add_title(message)
        vis.show(x_lim=(box.left, box.right), y_lim=(box.bottom, box.top))

    def drawArcs(self, box: Box, sweepline: float, vis: Visualizer, BL: Beachline):
        for parabola in self.visibleParabolas:
            vis.remove_figure(parabola)
            self.visibleParabolas.remove(parabola)
        for arc in self.arcs:
            left = arc.prev
            middle = arc
            right = arc.next
            x_left = box.left
            if left is not BL.guardian:
                x_left = Beachline.computeBreakpoint(
                    left.site.point, middle.site.point, sweepline, left.side)
                x_left = max(x_left, box.left)
            x_right = box.right
            if right is not BL.guardian:
                x_right = Beachline.computeBreakpoint(
                    middle.site.point, right.site.point, sweepline, right.side)
                x_right = min(x_right, box.right)
            data = arc.get_plot(
                np.arange(x_left, x_right, 0.0001), sweepline=sweepline)
            if data is not None:
                parabola = vis.add_parabola(data=data, color="green")
                self.visibleParabolas.append(parabola)

    def clearArcs(self, vis: Visualizer):
        for parabola in self.visibleParabolas:
            vis.remove_figure(parabola)
            self.visibleParabolas.remove(parabola)

    def drawSites(self, vis: Visualizer):
        vis.add_point([site.point.asTuple()
                      for site in self.sites], color="blue", s=2)

    def drawVertices(self, box: Box, vis: Visualizer):
        vis.add_point([vertex.point.asTuple()
                      for vertex in self.vertices if box.contains(vertex.point)], color="purple", s=3)

    def drawHalfEdges(self, box: Box, vis: Visualizer):
        for edge in self.halfEdges:
            if edge.destination is None or edge.origin is None:
                continue
            originInside = box.contains(edge.origin.point)
            destinationInside = box.contains(edge.destination.point)
            origin: Vector2d = edge.origin.point
            destination: Vector2d = edge.destination.point
            seg = None
            if originInside and destinationInside:
                seg = vis.add_line_segment(
                    (edge.origin.point.asTuple(), edge.destination.point.asTuple()))
                self.visibleHalfEdgesCoord.append(
                    (edge.origin.point.asTuple(), edge.destination.point.asTuple()))
            elif originInside and not destinationInside:
                direction = destination - origin
                intersection = box.getFirstIntersection(
                    origin, direction)
                seg = vis.add_line_segment(
                    (origin.asTuple(), intersection.point.asTuple()))
                self.visibleHalfEdgesCoord.append(
                    (origin.asTuple(), intersection.point.asTuple()))
            elif not originInside and destinationInside:
                direction = origin - destination
                intersection = box.getFirstIntersection(
                    destination, direction)
                seg = vis.add_line_segment(
                    (destination.asTuple(), intersection.point.asTuple()))
                self.visibleHalfEdgesCoord.append(
                    (destination.asTuple(), intersection.point.asTuple()))
            if seg is not None:
                self.visibleHalfEdges.append(seg)

    def drawSweepline(self, sweepline: float, box: Box, vis: Visualizer):
        if self.visibleSweepline is not None:
            vis.remove_figure(self.visibleSweepline)

        self.visibleSweepline = vis.add_line_segment(
            ((box.left, sweepline), (box.right, sweepline)), color="brown")

    def drawCircle(self, center: Vector2d, radius: float, vis: Visualizer, box: Box):
        if self.visibleCircle is not None:
            vis.remove_figure(self.visibleCircle)
        self.visibleCircle = vis.add_circle(
            (center.x, center.y, radius), color="purple", fill=False)
        self.circle = None
        self.drawVertices(box, vis)
