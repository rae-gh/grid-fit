#!/bin/bash
# install.sh - Build, install, and test gridfit C++ core, Python, and R bindings
# Run from the project root
set -e

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

# Install Python package
if [ -f setup.py ] || [ -f pyproject.toml ]; then
    echo "Installing Python package..."
    python -m pip install -e .
fi

# Install R package
if [ -d R ]; then
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

echo "All builds, installs, and tests completed successfully."
