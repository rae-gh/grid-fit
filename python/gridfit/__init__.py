from .gridfit_interp import (
    GridFit as _GridFit,
    interp as _interp,
    trilinear as _trilinear,
)
import numpy as np


# Wrapper class that handles numpy conversions
class GridFit:
    def __init__(self, x, y, z, values, order=2):
        # Just ensure contiguous and right dtype
        # C++ handles multidimensional arrays automatically!
        x = np.ascontiguousarray(x, dtype=np.float32)
        y = np.ascontiguousarray(y, dtype=np.float32)
        z = np.ascontiguousarray(z, dtype=np.float32)
        values = np.ascontiguousarray(values, dtype=np.float32)

        # C++ constructor handles flattening via buffer access
        self._grid = _GridFit(x, y, z, values, order)

    def interpolate(self, points):
        # Convert points to contiguous float32
        points = np.ascontiguousarray(points, dtype=np.float32)

        # C++ wrapper handles shape detection and flattening
        return self._grid.interpolate(points)

    def details(self):
        return self._grid.details()


# Keep standalone trilinear function for backwards compatibility
def trilinear(x, y, z, values, points):
    x = np.ascontiguousarray(x, dtype=np.float32)
    y = np.ascontiguousarray(y, dtype=np.float32)
    z = np.ascontiguousarray(z, dtype=np.float32)
    values = np.ascontiguousarray(values, dtype=np.float32)
    points = np.ascontiguousarray(points, dtype=np.float32)
    return _trilinear(x, y, z, values, points)


# Expose the simple interp function
interp = _interp
