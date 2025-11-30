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

Results are a work in progress. Currently trilinear interpolation itself is a bit faster than scipy but the construction of the grid object is slower:

```
Grid size:50,   Samples:500     Interp:gridfit is faster by 6.45x       Construct:scipy is faster by 6.28x
Grid size:100,  Samples:500     Interp:gridfit is faster by 5.37x       Construct:scipy is faster by 42.60x
Grid size:200,  Samples:500     Interp:gridfit is faster by 2.61x       Construct:scipy is faster by 301.96x
Grid size:256,  Samples:500     Interp:gridfit is faster by 3.71x       Construct:scipy is faster by 278.20x
Grid size:384,  Samples:500     Interp:gridfit is faster by 2.45x       Construct:scipy is faster by 2100.23x
Grid size:512,  Samples:500     Interp:gridfit is faster by 2.18x       Construct:scipy is faster by 6136.64x
Grid size:1024, Samples:500     Interp:gridfit is faster by 2.12x       Construct:scipy is faster by 57075.40x

Grid size:50,   Samples:1000    Interp:gridfit is faster by 3.97x       Construct:scipy is faster by 3.08x
Grid size:100,  Samples:1000    Interp:gridfit is faster by 2.41x       Construct:scipy is faster by 30.54x
Grid size:200,  Samples:1000    Interp:gridfit is faster by 2.14x       Construct:scipy is faster by 226.45x
Grid size:256,  Samples:1000    Interp:gridfit is faster by 1.81x       Construct:scipy is faster by 692.20x
Grid size:384,  Samples:1000    Interp:gridfit is faster by 2.68x       Construct:scipy is faster by 2014.38x
Grid size:512,  Samples:1000    Interp:gridfit is faster by 1.66x       Construct:scipy is faster by 4721.84x
Grid size:1024, Samples:1000    Interp:gridfit is faster by 2.49x       Construct:scipy is faster by 36303.35x

Grid size:50,   Samples:10000   Interp:gridfit is faster by 1.97x       Construct:scipy is faster by 1.90x
Grid size:100,  Samples:10000   Interp:gridfit is faster by 1.42x       Construct:scipy is faster by 31.64x
Grid size:200,  Samples:10000   Interp:gridfit is faster by 1.35x       Construct:scipy is faster by 126.81x
Grid size:256,  Samples:10000   Interp:gridfit is faster by 1.17x       Construct:scipy is faster by 1611.38x
Grid size:384,  Samples:10000   Interp:gridfit is faster by 1.48x       Construct:scipy is faster by 2386.44x
Grid size:512,  Samples:10000   Interp:gridfit is faster by 1.23x       Construct:scipy is faster by 5081.75x
Grid size:1024, Samples:10000   Interp:gridfit is faster by 1.99x       Construct:scipy is faster by 61036.42x

Grid size:50,   Samples:100000  Interp:gridfit is faster by 1.76x       Construct:scipy is faster by 1.03x
Grid size:100,  Samples:100000  Interp:gridfit is faster by 1.65x       Construct:scipy is faster by 19.09x
Grid size:200,  Samples:100000  Interp:gridfit is faster by 1.41x       Construct:scipy is faster by 115.44x
Grid size:256,  Samples:100000  Interp:gridfit is faster by 1.47x       Construct:scipy is faster by 541.33x
Grid size:384,  Samples:100000  Interp:gridfit is faster by 1.50x       Construct:scipy is faster by 2459.59x
Grid size:512,  Samples:100000  Interp:gridfit is faster by 1.20x       Construct:scipy is faster by 4504.84x
Grid size:1024, Samples:100000  Interp:gridfit is faster by 1.70x       Construct:scipy is faster by 31330.62x
```
