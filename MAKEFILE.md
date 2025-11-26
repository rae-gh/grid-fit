# Building grid-fit: C++, Python, and R Integration

This guide explains how to build and link the C++ core library, Python extension, and R package for the `grid-fit` project. It covers the build order, commands, and how the components are connected.

---

## 1. Build the C++ Core Library

The C++ core logic lives in `src/interp.cpp` and its header in `include/interp.h`. Build the static library first:

```sh
make
```
This creates `lib/libgridfit.a`, which contains the compiled C++ code.

---

## 2. Build and Install the Python Package

The Python extension uses the C++ core. You should configure your Python build (e.g., in `setup.py` or `pyproject.toml`) to:
- Include headers from `include/`
- Link against `lib/libgridfit.a`

**Typical steps:**
1. Ensure the C++ library is built (`make` as above).
2. From the project root, install the Python package (editable mode example):
   ```sh
   python -m pip install -e .
   ```
3. The Python extension module will be built and linked to the static library.

---

## 3. Build and Install the R Package

The R package also uses the C++ core. The build is controlled by `R/src/Makevars`, which:
- Adds `../../include` to the include path
- Links against `../../lib/libgridfit.a`

**Steps:**
1. Ensure the C++ library is built (`make` as above).
2. From the project root, install the R package:
   ```sh
   Rscript -e 'devtools::install("R")'
   ```
3. The R package will compile its bindings and link to the static library.

---

## 4. How Linking Works

- **C++ core**: All logic is implemented in `src/interp.cpp` and declared in `include/interp.h`.
- **Python**: The extension module (e.g., `python/gridfit/interp_py.cpp`) includes `interp.h` and links to `libgridfit.a`.
- **R**: The R binding (`R/src/interp.cpp`) includes `interp.h` and links to `libgridfit.a` via `Makevars`.

This ensures both Python and R use the same compiled C++ code, avoiding duplication and keeping all bindings in sync.

---

## 5. Clean Build

To remove all built files:
```sh
make clean
Rscript -e 'Rcpp::compileAttributes("R")'
```

---

## 6. Troubleshooting

- Always run `make` before building Python or R packages.
- If you change the C++ core, rebuild the library and reinstall the bindings.
- Ensure the include and library paths are correct in your build configs.

---

For more details, see the project documentation or ask for help!
