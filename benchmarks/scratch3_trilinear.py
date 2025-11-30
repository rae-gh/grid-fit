import numpy as np
from scipy.interpolate import RegularGridInterpolator
from gridfit import trilinear


def check_trilinear():
    # Hand-made grid and values

    x = np.arange(3)
    y = np.arange(3)
    z = np.arange(3)
    values = np.array(
        [
            [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
            [[10, 11, 12], [13, 14, 15], [16, 17, 18]],
            [[19, 20, 21], [22, 23, 24], [25, 26, 27]],
        ],
        dtype=np.float32,
    )

    # Single hand-made point
    point = np.array([[1, 1, 1]])

    # Run both methods
    scipy_interp = RegularGridInterpolator((x, y, z), values)
    scipy_result = scipy_interp(point)
    gridfit_result = trilinear(x, y, z, values, point)

    print("scipy_result:", scipy_result)
    print("gridfit_result:", gridfit_result)
    print("Max abs diff:", np.max(np.abs(scipy_result - gridfit_result)))


if __name__ == "__main__":
    check_trilinear()
