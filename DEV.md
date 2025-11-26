# Developer Setup Instructions for grid-fit

## 1. Clone the Repository

```bash
git clone https://github.com/rae-gh/grid-fit.git
cd grid-fit
```

## 2. Set Up Conda Environment

Create and activate a conda environment for development:

```bash
conda create -n gridfit-dev -c conda-forge python=3.10 cmake make gxx_linux-64 -y
conda activate gridfit-dev
conda install -c conda-forge pybind11 pytest numpy scipy -y
Rscript -e 'install.packages("devtools")'
Rscript -e 'devtools::install("R")'
```

You can add more dependencies to this environment as needed (e.g., 
`conda install -c conda-forge pybind11 pytest numpy scipy -y`  
, etc.).

## 3. Install Python Library in Editable Mode

```bash
python -m pip install -e .
```

This allows you to edit the Python code and have changes reflected immediately.

## 4. Build C++ Core and Bindings

Follow the instructions in the README or CMakeLists.txt to build the C++ core and bindings for Python and R.

## 5. Keep R Library Consistent

When updating the C++ core, ensure the R bindings are updated as well. Use the examples in `examples/R/` to test.

---

You can expand this file with more details as your development workflow evolves.

---

## Manual Testing Before Push

### Python
Run the integration tests with pytest:

```bash
pytest tests/python
```

### R
Run the R integration test script:

```bash
Rscript tests/R/test_interp.R
```

Make sure both tests pass before pushing changes.

## Pre-commit Hooks

This project uses pre-commit hooks to help maintain code quality for Python and C++ files. Hooks will automatically check formatting and linting before each commit.

### Setup

1. Install pre-commit (if not already):
	```bash
	python -m pip install pre-commit
	```
2. Install the hooks:
	```bash
	pre-commit install
	```

Now, every time you commit, black and flake8 will check Python files, and clang-format will check C++ files. You can add more hooks or languages as needed.

## Compiling the C++ Core

To build the C++ core library directly (for development or testing):

1. Create a build directory and navigate into it:
	```bash
	mkdir -p build
	cd build
	```
2. Run CMake to configure the project:
	```bash
	cmake ..
	```
3. Build the library:
	```bash
	make
	```

The compiled library or executable will be placed in the `build/` directory. Adjust CMake options as needed for your platform or development workflow.

