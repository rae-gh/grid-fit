# Test for gridfit.trilinear dummy output
import numpy as np
from gridfit import GridFit


def test_trilinear_dummy():
    x = np.array([0.0, 1.0], dtype=np.float32)
    y = np.array([0.0, 1.0], dtype=np.float32)
    z = np.array([0.0, 1.0], dtype=np.float32)
    values = np.array(
        [
            [[1, 2], [3, 4]],
            [[5, 6], [7, 8]],
        ],
        dtype=np.float32,
    )
    points = np.array([[0.5, 0.5, 0.5]], dtype=np.float32)
    gridfit = GridFit(x, y, z, values)
    out = gridfit.interpolate(points)
    print(out)
    assert out[0] == 4.5
