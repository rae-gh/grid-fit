import numpy as np
from scipy.interpolate import RegularGridInterpolator
from gridfit import trilinear
import timeit
import sys

# Dummy import for your future trilinear function
# from gridfit import trilinear

def benchmark_trilinear(n=200, n_points=10000):
    """
    n: grid size in each dimension (int)
    n_points: number of random query points (int)
    """
    # Create a regular 3D grid
    x = np.linspace(0, 1, n)
    y = np.linspace(0, 1, n)
    z = np.linspace(0, 1, n)
    values = np.random.rand(n, n, n)

    # Create interpolator
    interp = RegularGridInterpolator((x, y, z), values)

    # Generate random query points
    points = np.random.rand(n_points, 3)

    print(f"Benchmarking trilinear interpolation with grid size {n}^3 and {n_points} points.")
    # Time scipy
    t_scipy = timeit.timeit(lambda: interp(points), number=10)
    print(f"scipy RegularGridInterpolator (n={n}, points={n_points}): {t_scipy:.4f} s (10x)")

    # Uncomment and implement your trilinear function for comparison
    t_gridfit = timeit.timeit(lambda: trilinear(x, y, z, values, points), number=10)
    print(f"gridfit trilinear: {t_gridfit:.4f} s (10x)")

    # Optionally compare outputs for accuracy
    scipy_result = interp(points)
    gridfit_result = trilinear(x, y, z, values, points)
    print("Max abs diff:", np.max(np.abs(scipy_result - gridfit_result)))
    # which is greater or are they similar    
    if np.max(np.abs(scipy_result - gridfit_result)) > 1e-5:
        if scipy_result.mean() > gridfit_result.mean():
            print("Scipy result is greater than Gridfit result on average.")
        else:
            print("Gridfit result is greater than Scipy result on average.")        
    else:
        print("Gridfit result is similar to scipy result.")

if __name__ == "__main__":
    # Allow user to specify n and n_points via command line
    import argparse
    parser = argparse.ArgumentParser(description="Benchmark trilinear interpolation (scipy vs gridfit)")
    parser.add_argument("-n", type=int, default=200, help="Grid size in each dimension (default: 20)")
    parser.add_argument("-p", "--points", type=int, default=10000, help="Number of query points (default: 10000)")
    args = parser.parse_args()
    benchmark_trilinear(n=args.n, n_points=args.points)
