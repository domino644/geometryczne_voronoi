from modules.vertex import Vertex


class HalfEdge:
    def __init__(self) -> None:
        self.next: HalfEdge = None
        self.prev: HalfEdge = None
        self.origin: Vertex = None
        self.destination: Vertex = None
        self.twin: HalfEdge = None
        self.incidentFace = None
