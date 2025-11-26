
from .gridfit_interp import interp as _interp, trilinear as _trilinear
import numpy as np

def trilinear(x, y, z, values, points):
	x = np.ascontiguousarray(x, dtype=np.float32)
	y = np.ascontiguousarray(y, dtype=np.float32)
	z = np.ascontiguousarray(z, dtype=np.float32)
	values = np.ascontiguousarray(values, dtype=np.float32)
	points = np.ascontiguousarray(points, dtype=np.float32)
	return _trilinear(x, y, z, values, points)

interp = _interp
