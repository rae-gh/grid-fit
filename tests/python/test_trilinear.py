# Test for gridfit.trilinear dummy output
import numpy as np
from gridfit import trilinear


def test_trilinear_dummy():
    x = np.array([0.0, 1.0], dtype=np.float32)
    y = np.array([0.0, 1.0], dtype=np.float32)
    z = np.array([0.0, 1.0], dtype=np.float32)
    values = np.array([0, 1, 1, 0, 1, 0, 0, 1], dtype=np.float32)
    points = np.array([[0.5, 0.5, 0.5], [0.1, 0.2, 0.3]], dtype=np.float32)
    out = trilinear(x, y, z, values, points)
    assert np.all(out == 42)
