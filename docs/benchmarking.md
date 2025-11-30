# Benchmarking

This page describes how to benchmark the performance of the grid-fit library against standard Python methods.

## How to Run the Benchmark

1. Make sure you have the required dependencies:
   - numpy
   - scipy

   You can install them with:
   ```bash
   python -m pip install numpy scipy
   ```

2. Navigate to the `examples/benchmarking/` directory.

3. Run the benchmark script:
   ```bash
   python benchmark_trilinear.py
   ```

This script compares the performance of the standard Python method (`scipy.interpolate.RegularGridInterpolator`) with the grid-fit trilinear interpolation (to be implemented). The script will print timing results for each method.

## Results

Results are a work in progress. Currently trilinear interpolation itself is a bit faster than scipy but the cosntruction of the grid object so slower:

```
Grid size: 50, Sampled points: 500      Construction:scipy is faster than gridfit by 5.36x      Interpolation:gridfit is faster than scipy by 3.56x
Grid size: 100, Sampled points: 500     Construction:scipy is faster than gridfit by 141.34x    Interpolation:gridfit is faster than scipy by 6.15x
Grid size: 200, Sampled points: 500     Construction:scipy is faster than gridfit by 1050.24x   Interpolation:gridfit is faster than scipy by 3.41x
Grid size: 256, Sampled points: 500     Construction:scipy is faster than gridfit by 3227.74x   Interpolation:gridfit is faster than scipy by 2.19x
Grid size: 384, Sampled points: 500     Construction:scipy is faster than gridfit by 11688.96x  Interpolation:gridfit is faster than scipy by 3.96x
Grid size: 50, Sampled points: 1000     Construction:scipy is faster than gridfit by 6.99x      Interpolation:gridfit is faster than scipy by 1.68x
Grid size: 100, Sampled points: 1000    Construction:scipy is faster than gridfit by 30.23x     Interpolation:gridfit is faster than scipy by 1.49x
Grid size: 200, Sampled points: 1000    Construction:scipy is faster than gridfit by 685.68x    Interpolation:gridfit is faster than scipy by 1.47x
Grid size: 256, Sampled points: 1000    Construction:scipy is faster than gridfit by 1646.25x   Interpolation:gridfit is faster than scipy by 1.74x
Grid size: 384, Sampled points: 1000    Construction:scipy is faster than gridfit by 10000.22x  Interpolation:gridfit is faster than scipy by 3.08x
Grid size: 50, Sampled points: 10000    Construction:scipy is faster than gridfit by 7.62x      Interpolation:gridfit is faster than scipy by 2.24x
Grid size: 100, Sampled points: 10000   Construction:scipy is faster than gridfit by 34.32x     Interpolation:gridfit is faster than scipy by 1.54x
Grid size: 200, Sampled points: 10000   Construction:scipy is faster than gridfit by 546.57x    Interpolation:gridfit is faster than scipy by 1.36x
Grid size: 256, Sampled points: 10000   Construction:scipy is faster than gridfit by 1315.01x   Interpolation:gridfit is faster than scipy by 2.39x
Grid size: 384, Sampled points: 10000   Construction:scipy is faster than gridfit by 9893.04x   Interpolation:gridfit is faster than scipy by 1.09x
Grid size: 50, Sampled points: 100000   Construction:scipy is faster than gridfit by 4.12x      Interpolation:gridfit is faster than scipy by 1.98x
Grid size: 100, Sampled points: 100000  Construction:scipy is faster than gridfit by 47.77x     Interpolation:gridfit is faster than scipy by 1.57x
Grid size: 200, Sampled points: 100000  Construction:scipy is faster than gridfit by 274.12x    Interpolation:gridfit is faster than scipy by 1.17x
Grid size: 256, Sampled points: 100000  Construction:scipy is faster than gridfit by 953.98x    Interpolation:gridfit is faster than scipy by 1.10x
Grid size: 384, Sampled points: 100000  Construction:scipy is faster than gridfit by 10873.93x  Interpolation:gridfit is faster than scipy by 1.20x
```
