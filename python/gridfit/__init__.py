from .gridfit_interp import (
    GridFit as _GridFit,
    interp as _interp,
    trilinear as _trilinear,
)
import numpy as np


class GridFit:
    def __init__(self, x, y, z, values, order=2):
        # Ensure contiguous and right dtype
        # IMPORTANT: Store references to keep arrays alive!
        self._x = np.ascontiguousarray(x, dtype=np.float32)
        self._y = np.ascontiguousarray(y, dtype=np.float32)
        self._z = np.ascontiguousarray(z, dtype=np.float32)
        self._values = np.ascontiguousarray(values, dtype=np.float32)

        # C++ stores pointers to these arrays (zero-copy!)
        self._grid = _GridFit(self._x, self._y, self._z, self._values, order)

    def interpolate(self, points):
        points = np.ascontiguousarray(points, dtype=np.float32)
        return self._grid.interpolate(points)

    def details(self):
        return self._grid.details()


# Keep standalone functions
def trilinear(x, y, z, values, points):
    x = np.ascontiguousarray(x, dtype=np.float32)
    y = np.ascontiguousarray(y, dtype=np.float32)
    z = np.ascontiguousarray(z, dtype=np.float32)
    values = np.ascontiguousarray(values, dtype=np.float32)
    points = np.ascontiguousarray(points, dtype=np.float32)
    return _trilinear(x, y, z, values, points)


interp = _interp
