from datetime import datetime
import json
import numpy as np
from scipy.interpolate import RegularGridInterpolator
from gridfit import GridFit
import timeit
import platform
from sysinfo import get_system_info

# Dummy import for your future trilinear function
# from gridfit import trilinear


def benchmark_trilinear(cube_size=10, sampled_points=10, num_benches=10, runs="n*", print_res=False):        
    runs = f",{runs},"  # all possible "2,2*,3,3*"
    runs_data = []
    if ",2," in runs:
        x = np.arange(2, dtype=np.float32)
        y = np.arange(2, dtype=np.float32)
        z = np.arange(2, dtype=np.float32)
        values = np.random.rand(2, 2, 2).astype(np.float32)
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
        x = np.arange(2, dtype=np.float32)
        y = np.arange(2, dtype=np.float32)
        z = np.arange(2, dtype=np.float32)
        values = np.random.rand(2, 2, 2).astype(np.float32)
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
        x = np.arange(3, dtype=np.float32)
        y = np.arange(3, dtype=np.float32)
        z = np.arange(3, dtype=np.float32)
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
        x = np.arange(3, dtype=np.float32)
        y = np.arange(3, dtype=np.float32)
        z = np.arange(3, dtype=np.float32)
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
        x = np.arange(cube_size, dtype=np.float32)
        y = np.arange(cube_size, dtype=np.float32)
        z = np.arange(cube_size, dtype=np.float32)
        values = np.random.rand(cube_size, cube_size, cube_size).astype(np.float32)
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

        scipy_interp = RegularGridInterpolator((x, y, z), values)
        gridfit_obj = GridFit(x, y, z, values)

        def scipy_construct():
            return RegularGridInterpolator((x, y, z), values)

        def scipy_run():
            return scipy_interp(points)

        def gridfit_construct():
            return GridFit(x, y, z, values, order=2)

        def gridfit_run():
            return gridfit_obj.interpolate(points)

        
        benchmark_result = {
                'grid_size': n,
                'n_interp_points': n_points,
                'n_repetitions': number,
                'gridfit_construct_time': "",
                'scipy_construct_time': "",
                'gridfit_interp_time': "",
                'scipy_interp_time': "",
                'max_error': "",
                'mean_error': "",
            }
        
        t_scipyconstruct = timeit.timeit(scipy_construct, number=number)
        print(f"scipy RegularGridInterpolator:\t{t_scipyconstruct:.4f} s ({number}x)")
        benchmark_result['scipy_construct_time'] = t_scipyconstruct

        t_scipy = timeit.timeit(scipy_run, number=number)
        print(f"scipy points:\t{t_scipy:.4f} s ({number}x)")
        benchmark_result['scipy_interp_time'] = t_scipy

        t_gridfitconstruct = timeit.timeit(gridfit_construct, number=number)
        print(f"gridfit GridFit\t\t{t_gridfitconstruct:.4f} s ({number}x)")
        benchmark_result['gridfit_construct_time'] = t_gridfitconstruct

        t_gridfit = timeit.timeit(gridfit_run, number=number)
        print(f"gridfit interpolate\t\t{t_gridfit:.4f} s ({number}x)")
        benchmark_result['gridfit_interp_time'] = t_gridfit

        # compare outputs for accuracy (single run, not timed)
        scipy_result = scipy_interp(points)
        gridfit_result = gridfit_obj.interpolate(points)
        # make float32 for and 4 dpecimals for comparison
        scipy_result = np.round(scipy_result.astype(np.float32), 4)
        gridfit_result = np.round(gridfit_result.astype(np.float32), 4)

        differences = np.abs(gridfit_result - scipy_result)
        max_error = np.max(differences)
        mean_error = np.mean(differences)
        benchmark_result['max_error'] = float(max_error)
        benchmark_result['mean_error'] = float(mean_error)

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
            if print_res:
                print(scipy_result)
                print(gridfit_result)
        # Print which is faster and by how much
        cons, inter = "", ""
        if t_gridfitconstruct < t_scipyconstruct:
            print(f"gridfit is faster by {t_scipyconstruct / t_gridfitconstruct:.2f}x")
            cons = f"gridfit is faster by {t_scipyconstruct / t_gridfitconstruct:.2f}x"
        else:
            print(f"scipy is faster by {t_gridfitconstruct / t_scipyconstruct:.2f}x")
            cons = f"scipy is faster by {t_gridfitconstruct / t_scipyconstruct:.2f}x"

        if t_gridfit < t_scipy:
            print(f"gridfit is faster by {t_scipy / t_gridfit:.2f}x")
            inter = f"gridfit is faster by {t_scipy / t_gridfit:.2f}x"
        else:
            print(f"scipy is faster by {t_gridfit / t_scipy:.2f}x")
            inter = f"scipy is faster by {t_gridfit / t_scipy:.2f}x"
        
        return benchmark_result


if __name__ == "__main__":

    # Primary benchmark - most realistic
    benches = [10]
    sampled_points_list = [100, 1000, 10000, 100000]
    cube_sizes = [50, 100, 256, 512, 1024]
    
    results = {
        'metadata': {
            'system': get_system_info(),
            'timestamp': datetime.now().isoformat(),
            'benchmark_version': '1.0',
        },
        'benchmarks': []
    }

    for nb in benches:
        for ns in sampled_points_list:
            for gs in cube_sizes:
                ans = benchmark_trilinear(cube_size=gs, sampled_points=ns, num_benches=nb, runs="n*")

            results['benchmarks'].append(ans)

    print(results)

    # Save with descriptive filename
    hostname = platform.node().split('.')[0]  # short hostname
    filename = f'benchmark_results_{hostname}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Results saved to {filename}")
    
    
