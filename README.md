# gridfit_interp Library Scaffold

This is a cross-language library for linear interpolation, implemented in C++ and callable from Python and R.

## Quick Start
[Installation and basic example]

## What are Alcraft Matrices?
[Brief explanation]

## C++
- Library source: `src/interp.cpp`, header: `include/interp.h`
- Build with CMake: `mkdir build && cd build && cmake .. && make`

## Python
- Wrapper in `python/interp_py.cpp`, build with `python/setup.py`
- Test: `python/test_interp.py`

## R
- R package structure in `R/`
- Main wrapper: `R/src/interp.cpp`
- Test: `R/tests/testthat.R`

## Example
- Interpolating between 0 and 1 with 1 point: `interp(0, 1, 1)` returns `[0.5]` in all languages.

# grid-fit

Fast N-dimensional polynomial interpolation on regular grids using precomputed Alcraft matrices.

## Features
- Trilinear interpolation (faster than scipy)
- Extends naturally to tricubic, higher dimensions
- Python and R bindings
- Efficient precomputed matrix approach

```

**.gitignore:**
```
# Build artifacts
build/
dist/
*.so
*.dll
*.dylib
*.o

# Python
__pycache__/
*.pyc
*.egg-info/
.pytest_cache/

# R
*.Rcheck/
.Rhistory

# IDE
.vscode/
.idea/
*.swp