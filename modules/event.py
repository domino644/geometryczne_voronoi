class Event:
    CIRCLE = 0
    SITE = 1

    def __init__(self, type, site, lowest=None, arc=None, radius=None) -> None:
        self.type = type
        self.site = site
        self.arc = arc
        self.lowest = lowest
        self.active = True
        self.radius = radius

    def remove(self):
        self.active = False

    @property
    def y_to_comp(self):
        if self.type == Event.CIRCLE:
            return self.lowest
        else:
            return self.site.point.y

    def __lt__(self, other):
        return (-self.y_to_comp, self.site.point.x) < (-other.y_to_comp, other.site.point.x)

    def __gt__(self, other):
        return (-self.y_to_comp, self.site.point.x) > (-other.y_to_comp, other.site.point.x)

    def __le__(self, other):
        return (-self.y_to_comp, self.site.point.x) <= (-other.y_to_comp, other.site.point.x)

    def __ge__(self, other):
        return (-self.y_to_comp, self.site.point.x) >= (-other.y_to_comp, other.site.point.x)

    def __eq__(self, other):
        return self.site.point.y == other.site.point.y and self.site.point.x == other.site.point.x

    def __ne__(self, other):
        return not self == other
