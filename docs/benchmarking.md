# Benchmarking

This page describes how to benchmark the performance of the grid-fit library against standard Python methods.

## How to Run the Benchmark

1. Make sure you have the required dependencies:
   - numpy
   - scipy

   You can install them with:
   ```bash
   pip install numpy scipy
   ```

2. Navigate to the `examples/benchmarking/` directory.

3. Run the benchmark script:
   ```bash
   python benchmark_trilinear.py
   ```

This script compares the performance of the standard Python method (`scipy.interpolate.RegularGridInterpolator`) with the grid-fit trilinear interpolation (to be implemented). The script will print timing results for each method.

## Results

Results pending implementation of the grid-fit trilinear function. Once available, this page will be updated with performance comparisons and analysis.
