# Test for gridfit.trilinear dummy output
import gridfit
import numpy as np

def test_trilinear_dummy():
    x = np.ascontiguousarray(x, dtype=np.float32)
    y = np.ascontiguousarray(y, dtype=np.float32)
    z = np.ascontiguousarray(z, dtype=np.float32)
    values = np.ascontiguousarray(values, dtype=np.float32)
    points = np.ascontiguousarray(points, dtype=np.float32)
    result = gridfit.trilinear(x, y, z, values, points)
    assert np.all(result == 42.0), f"Expected all 42.0, got {result}"
