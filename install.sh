#!/bin/bash
# install.sh - Build, install, and test gridfit C++ core, Python, and R bindings
# Run from the project root
set -e

# Set GRIDFIT_ROOT for R build
export GRIDFIT_ROOT=$(pwd)

# Clean previous builds
if [ -d lib ]; then
    echo "Cleaning C++ static library..."
    make clean || true
fi
if [ -d build ]; then
    echo "Cleaning CMake build directory..."
    rm -rf build
fi

# Build C++ core static library
if [ -f Makefile ]; then
    echo "Building C++ static library..."
    make
fi

# Clean Python build artifacts
if [ -d build ]; then
    echo "Removing Python build directory..."
    rm -rf build
fi
if [ -d python/build ]; then
    echo "Removing python/build directory..."
    rm -rf python/build
fi
# Optionally remove old .so files in python/gridfit
find python/gridfit -name '*.so' -delete 2>/dev/null || true

# Install Python package
if [ -f setup.py ] || [ -f pyproject.toml ]; then
    echo "Installing Python package..."
    python -m pip install -e .
fi

# Generate RcppExports and install R package
if [ -d R ]; then
    echo "Generating RcppExports..."
    Rscript -e 'Rcpp::compileAttributes("R")'
    echo "Installing R package..."
    Rscript -e 'devtools::install("R")'
fi

# Build and run C++ example
if [ -f examples/cpp/example_interp.cpp ]; then
    echo "Building C++ example..."    
    g++ -O3 -march=native -Iinclude examples/cpp/example_interp.cpp lib/libgridfit.a -o examples/cpp/example_interp
fi

# Run integration tests via bash example script
if [ -f examples/bash/interp.sh ]; then
    echo "Running integration tests (Python & R)..."
    bash examples/bash/interp.sh
fi

# Build and run C++ trilinear example
if [ -f examples/cpp/example_trilinear.cpp ]; then
    echo "Building C++ trilinear example..."
    g++ -O3 -march=native -Iinclude examples/cpp/example_trilinear.cpp lib/libgridfit.a -o examples/cpp/example_trilinear
    echo "Running C++ trilinear example:"
    ./examples/cpp/example_trilinear
fi

# Run Python trilinear example
if [ -f examples/python/example_trilinear.py ]; then
    echo "Running Python trilinear example:"
    python examples/python/example_trilinear.py
fi

# Run R trilinear example
if [ -f examples/R/example_trilinear.R ]; then
    echo "Running R trilinear example:"
    Rscript examples/R/example_trilinear.R
fi

# Run Python trilinear benchmark (scipy vs gridfit)
if [ -f benchmarks/benchmark_trilinear.py ]; then
    echo "--- Running Python trilinear benchmark (scipy vs gridfit) ---"
    # Ensure scipy and numpy are installed
    python -m pip install --quiet numpy scipy
    python benchmarks/benchmark_trilinear.py
    echo "--- End of Python trilinear benchmark ---"
fi


echo "All builds, installs, and tests completed successfully."