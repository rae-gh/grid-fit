import numpy as np
from scipy.interpolate import RegularGridInterpolator
import timeit

# Dummy import for your future trilinear function
# from gridfit import trilinear

def benchmark_trilinear():
    # Create a regular 3D grid
    x = np.linspace(0, 1, 20)
    y = np.linspace(0, 1, 20)
    z = np.linspace(0, 1, 20)
    values = np.random.rand(20, 20, 20)

    # Create interpolator
    interp = RegularGridInterpolator((x, y, z), values)

    # Generate random query points
    points = np.random.rand(10000, 3)

    # Time scipy
    t_scipy = timeit.timeit(lambda: interp(points), number=10)
    print(f"scipy RegularGridInterpolator: {t_scipy:.4f} s (10x)")

    # Uncomment and implement your trilinear function for comparison
    # t_gridfit = timeit.timeit(lambda: trilinear(x, y, z, values, points), number=10)
    # print(f"gridfit trilinear: {t_gridfit:.4f} s (10x)")

    # # Optionally compare outputs for accuracy
    # scipy_result = interp(points)
    # gridfit_result = trilinear(x, y, z, values, points)
    # print("Max abs diff:", np.max(np.abs(scipy_result - gridfit_result)))

if __name__ == "__main__":
    benchmark_trilinear()
