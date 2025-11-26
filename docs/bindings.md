
# Bindings: How C++ Compiling Works for Python and R

## Overview Diagram

```mermaid
flowchart TD
	A[C++ Source Code] -->|Compile with CMake/pybind11| B(Python Shared Library .so)
	A -->|Compile with CMake/Rcpp| C(R Shared Library .so)
	B -->|Install with pip| D[Python Package]
	C -->|Install with devtools| E[R Package]
	D -->|import gridfit| F[Python User]
	E -->|library(gridfit)| G[R User]
```

## C++ Core Development
You write and edit your C++ code (e.g., in `src/`).

## Compiling for Bindings
- To use your C++ code in Python or R, you must compile it into a shared library (e.g., `.so` on Linux, `.dll` on Windows, `.dylib` on macOS).
- This is usually done with CMake or a similar build system, which creates the shared library and the necessary binding code (using pybind11 for Python, Rcpp for R).

## Python Package
- The Python package (created with pybind11) includes the compiled shared library (e.g., `gridfit.cpython-310-x86_64-linux-gnu.so`).
- When you install the Python package (e.g., with `pip install .`), the build process compiles the C++ code and places the shared library in the package directory.
- Python imports this shared library as a module.

## R Package
- The R package (created with Rcpp) also includes the compiled shared library (e.g., `gridfit.so`).
- When you build/install the R package (e.g., with `devtools::install()`), R compiles the C++ code and places the shared library in the package’s `libs/` directory.
- R loads this shared library when you load the package.

## Summary
- The C++ code is compiled into a shared library for both Python and R.
- The packages (Python and R) include the compiled version, not the raw C++ source (except for development or source distributions).
- You need to recompile whenever you change the C++ code and want those changes available in Python or R.
