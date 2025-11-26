import numpy as np
from scipy.interpolate import RegularGridInterpolator
from gridfit import trilinear
import timeit

# Dummy import for your future trilinear function
# from gridfit import trilinear


def benchmark_trilinear(n=20, n_points=100):
    """
    n: grid size in each dimension (int)
    n_points: number of random query points (int)
    """
    # Create a regular 3D grid (0 to n)
    n = 2
    n_points = 2
    x = np.arange(n)
    y = np.arange(n)
    z = np.arange(n)
    values = np.random.rand(n, n, n)

    # Generate random query points (shared for both), scaled to [0, n]
    points = np.random.rand(n_points, 3) * (n - 1)

    # print(x)
    # print(y)
    # print(z)
    # print(values)
    # print(points)

    print(
        f"Benchmarking trilinear interpolation with grid size {n}^3 and {n_points} points."
    )

    # Time scipy: include setup (interpolator creation) and evaluation
    def scipy_run():
        interp = RegularGridInterpolator((x, y, z), values)
        result = interp(points)
        print("scipy_run returned:", result)
        return result

    t_scipy = timeit.timeit(scipy_run, number=10)
    print(
        f"scipy RegularGridInterpolator (n={n}, points={n_points}): {t_scipy:.4f} s (10x)"
    )

    # Time gridfit: include setup if any (for fairness, same as scipy)
    def gridfit_run():
        # If trilinear has setup, put it here; otherwise just call
        result = trilinear(x, y, z, values, points)
        print("gridfit_run returned:", result)
        return result

    t_gridfit = timeit.timeit(gridfit_run, number=10)
    print(f"gridfit trilinear: {t_gridfit:.4f} s (10x)")

    # Optionally compare outputs for accuracy (single run, not timed)
    interp = RegularGridInterpolator((x, y, z), values)
    scipy_result = interp(points)
    gridfit_result = trilinear(x, y, z, values, points)
    max_diff = np.max(np.abs(scipy_result - gridfit_result))
    print("Max abs diff:", max_diff)
    if max_diff > 1e-5:
        print("[WARNING] gridfit values do no NOT match scipy..\n")
    else:
        print("Gridfit result is similar to scipy result.")
    # Print which is faster and by how much
    if t_gridfit < t_scipy:
        print(f"gridfit is faster than scipy by {t_scipy / t_gridfit:.2f}x")
    else:
        print(f"scipy is faster than gridfit by {t_gridfit / t_scipy:.2f}x")


if __name__ == "__main__":
    # Allow user to specify n and n_points via command line
    import argparse

    parser = argparse.ArgumentParser(
        description="Benchmark trilinear interpolation (scipy vs gridfit)"
    )
    parser.add_argument(
        "-n", type=int, default=20, help="Grid size in each dimension (default: 20)"
    )
    parser.add_argument(
        "-p",
        "--points",
        type=int,
        default=20,
        help="Number of query points (default: 20)",
    )
    args = parser.parse_args()
    benchmark_trilinear(n=args.n, n_points=args.points)
