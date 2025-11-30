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

Results are a work in progress. The trilinear method is faster than scipy at both construction and interpolation.
Derivatives, slices and tricubic to follow...

```
Grid size:50,   Samples:500     Interp:gridfit is faster by 5.12x       Construct:gridfit is faster by 4.38x
Grid size:100,  Samples:500     Interp:gridfit is faster by 5.15x       Construct:gridfit is faster by 3.16x
Grid size:200,  Samples:500     Interp:gridfit is faster by 5.67x       Construct:gridfit is faster by 3.08x
Grid size:256,  Samples:500     Interp:gridfit is faster by 1.72x       Construct:gridfit is faster by 3.93x
Grid size:384,  Samples:500     Interp:gridfit is faster by 2.99x       Construct:gridfit is faster by 2.42x
Grid size:512,  Samples:500     Interp:gridfit is faster by 2.82x       Construct:gridfit is faster by 2.21x
Grid size:1024, Samples:500     Interp:gridfit is faster by 2.83x       Construct:gridfit is faster by 6.58x

Grid size:50,   Samples:1000    Interp:gridfit is faster by 2.34x       Construct:gridfit is faster by 1.53x
Grid size:100,  Samples:1000    Interp:gridfit is faster by 2.23x       Construct:gridfit is faster by 4.11x
Grid size:200,  Samples:1000    Interp:gridfit is faster by 2.06x       Construct:gridfit is faster by 5.48x
Grid size:256,  Samples:1000    Interp:gridfit is faster by 1.97x       Construct:gridfit is faster by 5.76x
Grid size:384,  Samples:1000    Interp:gridfit is faster by 1.79x       Construct:gridfit is faster by 8.98x
Grid size:512,  Samples:1000    Interp:gridfit is faster by 1.75x       Construct:gridfit is faster by 7.85x
Grid size:1024, Samples:1000    Interp:scipy is faster by 1.10x Construct:gridfit is faster by 3.80x

Grid size:50,   Samples:10000   Interp:gridfit is faster by 1.49x       Construct:gridfit is faster by 3.18x
Grid size:100,  Samples:10000   Interp:gridfit is faster by 1.46x       Construct:gridfit is faster by 3.27x
Grid size:200,  Samples:10000   Interp:gridfit is faster by 1.54x       Construct:gridfit is faster by 3.36x
Grid size:256,  Samples:10000   Interp:gridfit is faster by 1.27x       Construct:gridfit is faster by 3.29x
Grid size:384,  Samples:10000   Interp:gridfit is faster by 1.45x       Construct:gridfit is faster by 2.87x
Grid size:512,  Samples:10000   Interp:gridfit is faster by 1.32x       Construct:gridfit is faster by 4.78x
Grid size:1024, Samples:10000   Interp:gridfit is faster by 1.65x       Construct:gridfit is faster by 18.46x

Grid size:50,   Samples:100000  Interp:gridfit is faster by 1.67x       Construct:gridfit is faster by 3.55x
Grid size:100,  Samples:100000  Interp:gridfit is faster by 1.49x       Construct:gridfit is faster by 3.46x
Grid size:200,  Samples:100000  Interp:gridfit is faster by 1.26x       Construct:gridfit is faster by 2.32x
Grid size:256,  Samples:100000  Interp:gridfit is faster by 1.31x       Construct:gridfit is faster by 2.78x
Grid size:384,  Samples:100000  Interp:gridfit is faster by 1.17x       Construct:gridfit is faster by 3.25x
Grid size:512,  Samples:100000  Interp:gridfit is faster by 1.61x       Construct:gridfit is faster by 4.60x
Grid size:1024, Samples:100000  Interp:gridfit is faster by 1.47x       Construct:gridfit is faster by 4.23x
```
