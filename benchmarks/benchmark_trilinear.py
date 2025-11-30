import numpy as np
from scipy.interpolate import RegularGridInterpolator
from gridfit import trilinear
import timeit

# Dummy import for your future trilinear function
# from gridfit import trilinear


def benchmark_trilinear():
    runs = ",3,3*,"  # all possible "2,2*,3,3*,"
    runs_data = []
    if ",2," in runs:
        x = np.arange(2)
        y = np.arange(2)
        z = np.arange(2)
        values = np.random.rand(2, 2, 2)
        values = np.array(
            [
                [[1, 2], [3, 4]],
                [[5, 6], [7, 8]],
            ],
            dtype=np.float32,
        )
        # values[0, 0, 0] → 1,         # values[0, 0, 1] → 2
        # values[0, 1, 0] → 3,         # values[0, 1, 1] → 4
        # values[1, 0, 0] → 5,         # values[1, 0, 1] → 6
        # values[1, 1, 0] → 7,         # values[1, 1, 1] → 8
        points = np.array(
            [
                [0.0, 0.0, 0.0],  # Should return 1
                [1.0, 1.0, 1.0],  # Should return 8
                [0.5, 0.0, 0.0],  # edge half
                [0.0, 0.5, 0.0],  # edge half
                [0.0, 0.0, 0.5],  # edge half
                [0.5, 0.5, 0.5],  # Should interpolate to the center
            ]
        )
        shoulds = [1, 8, 1.5, 2.0, 2.5, 14.0]
        runs_data.append((2, 70, values, points, shoulds))
    if ",2*," in runs:
        x = np.arange(2)
        y = np.arange(2)
        z = np.arange(2)
        values = np.random.rand(2, 2, 2)
        # Generate 10 random points within the grid domain
        n_points = 10
        points = np.column_stack(
            [
                np.random.uniform(np.min(x), np.max(x), n_points),
                np.random.uniform(np.min(y), np.max(y), n_points),
                np.random.uniform(np.min(z), np.max(z), n_points),
            ]
        )
        runs_data.append((2, 70, values, points, None))
    if "3" in runs:
        x = np.arange(3)
        y = np.arange(3)
        z = np.arange(3)
        values = np.random.rand(3, 3, 3)
        values = np.array(
            [
                [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
                [[10, 11, 12], [13, 14, 15], [16, 17, 18]],
                [[19, 20, 21], [22, 23, 24], [25, 26, 27]],
            ],
            dtype=np.float32,
        )
        points = np.array(
            [
                [0.0, 0.0, 0.0],  # Should return 1
                [1.0, 1.0, 1.0],  # Should return 8
                [0.5, 0.0, 0.0],  # edge half
                [0.0, 0.5, 0.0],  # edge half
                [0.0, 0.0, 0.5],  # edge half
                [0.5, 0.5, 0.5],  # Should interpolate to the center
            ]
        )
        shoulds = [1, 14, 5.5, 10.0, 15.5, 14.0]
        runs_data.append((3, 50, values, points, shoulds))
    if "3*," in runs:
        x = np.arange(3)
        y = np.arange(3)
        z = np.arange(3)
        values = np.random.rand(3, 3, 3)
        # Generate 10 random points within the grid domain
        n_points = 10
        points = np.column_stack(
            [
                np.random.uniform(np.min(x), np.max(x), n_points),
                np.random.uniform(np.min(y), np.max(y), n_points),
                np.random.uniform(np.min(z), np.max(z), n_points),
            ]
        )
        runs_data.append((3, 50, values, points, None))

    for n, number, values, points, shoulds in runs_data:

        n_points = len(points)

        print(x)
        print(y)
        print(z)
        print("--- Values ---")
        print(values)
        print("--- Points ---")
        print(points)

        print(
            "------------------------------------------------------\n",
            f"Benchmarking trilinear interpolation with grid size {n}^3 and {n_points} points, running {number} times.",
        )

        # Time scipy: include setup (interpolator creation) and evaluation
        def scipy_run():
            interp = RegularGridInterpolator((x, y, z), values)
            result = interp(points)
            print("\tscipy_run returned:", result)
            return result

        t_scipy = timeit.timeit(scipy_run, number=number)
        print(
            f"scipy RegularGridInterpolator (n={n}, points={n_points}): {t_scipy:.4f} s ({number}x)"
        )

        # Time gridfit: include setup if any (for fairness, same as scipy)
        def gridfit_run():
            # If trilinear has setup, put it here; otherwise just call
            result = trilinear(x, y, z, values, points)
            print("\tgridfit_run returned:", result)
            return result

        t_gridfit = timeit.timeit(gridfit_run, number=number)
        print(f"gridfit trilinear: {t_gridfit:.4f} s ({number}x)")

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
    benchmark_trilinear()
