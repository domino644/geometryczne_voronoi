from matplotlib.axes import Axes
from .figure import Figure
import numpy as np


class Parabola(Figure):
    def __init__(self, data, options):
        data = np.column_stack(data)
        super().__init__(data, options)

    def draw(self, ax: Axes):
        artist = []
        x_values = self.data[:, 0]
        y_values = self.data[:, 1]
        artist = ax.plot(x_values, y_values, **self.options)
        return artist
