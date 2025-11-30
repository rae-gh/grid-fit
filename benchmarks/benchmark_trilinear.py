import numpy as np
from scipy.interpolate import RegularGridInterpolator
from gridfit import trilinear, GridFit
import timeit

# Dummy import for your future trilinear function
# from gridfit import trilinear


def benchmark_trilinear(cube_size=10, sampled_points=10, runs="n*"):
    num_benches = 50
    runs = f",{runs},"  # all possible "2,2*,3,3*"
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
        runs_data.append((2, x, y, z, num_benches, values, points, shoulds))
    if ",2*," in runs:
        x = np.arange(2)
        y = np.arange(2)
        z = np.arange(2)
        values = np.random.rand(2, 2, 2)
        n_points = sampled_points
        points = np.column_stack(
            [
                np.random.uniform(np.min(x), np.max(x), n_points),
                np.random.uniform(np.min(y), np.max(y), n_points),
                np.random.uniform(np.min(z), np.max(z), n_points),
            ]
        )
        runs_data.append((2, x, y, z, num_benches, values, points, None))
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
        runs_data.append((3, x, y, z, num_benches, values, points, shoulds))
    if ",3*," in runs:
        x = np.arange(3)
        y = np.arange(3)
        z = np.arange(3)
        values = np.random.rand(3, 3, 3)
        n_points = sampled_points
        points = np.column_stack(
            [
                np.random.uniform(np.min(x), np.max(x), n_points),
                np.random.uniform(np.min(y), np.max(y), n_points),
                np.random.uniform(np.min(z), np.max(z), n_points),
            ]
        )
        runs_data.append((3, x, y, z, num_benches, values, points, None))

    if ",n*," in runs:
        x = np.arange(cube_size)
        y = np.arange(cube_size)
        z = np.arange(cube_size)
        values = np.random.rand(cube_size, cube_size, cube_size)
        n_points = sampled_points
        points = np.column_stack(
            [
                np.random.uniform(np.min(x), np.max(x), n_points),
                np.random.uniform(np.min(y), np.max(y), n_points),
                np.random.uniform(np.min(z), np.max(z), n_points),
            ]
        )
        runs_data.append((cube_size, x, y, z, num_benches, values, points, None))

    for n, x, y, z, number, values, points, shoulds in runs_data:
        n_points = len(points)
        print(
            "------------------------------------------------------\n",
            f"Benchmark trilinear interp, grid size {n}^3 and {n_points} points, {number} times.",
        )

        # Time scipy: include setup (interpolator creation) and evaluation
        def scipy_run():
            interp = RegularGridInterpolator((x, y, z), values)
            return interp(points)

        t_scipy = timeit.timeit(scipy_run, number=number)
        print(f"scipy RegularGridInterpolator:\t{t_scipy:.4f} s ({number}x)")

        # Time gridfit: include setup if any (for fairness, same as scipy)
        def gridfit_run():
            # If trilinear has setup, put it here; otherwise just call
            gridfit = GridFit(x, y, z, values)
            # return trilinear(x, y, z, values, points)
            return gridfit.interpolate(points)

        t_gridfit = timeit.timeit(gridfit_run, number=number)
        print(f"gridfit trilinear\t\t{t_gridfit:.4f} s ({number}x)")

        # Optionally compare outputs for accuracy (single run, not timed)
        interp = RegularGridInterpolator((x, y, z), values)
        scipy_result = interp(points)
        gridfit_result = trilinear(x, y, z, values, points)
        # make float32 for and 4 dpecimals for comparison
        scipy_result = np.round(scipy_result.astype(np.float32), 4)
        gridfit_result = np.round(gridfit_result.astype(np.float32), 4)

        max_diff = np.max(np.abs(scipy_result - gridfit_result))
        if not np.allclose(scipy_result, gridfit_result, atol=1e-4, rtol=1e-7):
            print("[!!!!! WARNING] gridfit values do NOT match scipy..\n")
            print("Max abs diff:", max_diff)
            mask = ~np.isclose(scipy_result, gridfit_result, atol=1e-4, rtol=1e-7)
            diff_indices = np.where(mask)[0]
            print(f"Number of differing points: {len(diff_indices)}")
            for idx in diff_indices[:]:
                print(
                    f"  idx {idx}: scipy={scipy_result[idx]}, gridfit={gridfit_result[idx]}, diff={scipy_result[idx] - gridfit_result[idx]}"
                )
        else:
            print("== results are equivalent ==")
        # Print which is faster and by how much
        if t_gridfit < t_scipy:
            print(f"gridfit is faster than scipy by {t_scipy / t_gridfit:.2f}x")
            return f"gridfit is faster than scipy by {t_scipy / t_gridfit:.2f}x"
        else:
            print(f"scipy is faster than gridfit by {t_gridfit / t_scipy:.2f}x")
            return f"scipy is faster than gridfit by {t_gridfit / t_scipy:.2f}x"


if __name__ == "__main__":
    # Primary benchmark - most realistic
    grid_sizes = [100, 200, 256, 384, 512]
    n_samples = [1000, 10000]
    results = []
    for gs in grid_sizes:
        for ns in n_samples:
            ans = benchmark_trilinear(cube_size=gs, sampled_points=ns, runs="n*")
            results.append(f"Grid size: {gs}, Sampled points: {ns}\tResult: {ans}")

    print("\n".join(results))
