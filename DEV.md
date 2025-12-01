
# Developer Onboarding & Setup for grid-fit


## Getting Started (Recommended)

1. **Clone the repository:**
	```bash
	git clone https://github.com/rae-gh/grid-fit.git
	cd grid-fit
	```
2. **(Recommended) Create and activate a conda environment:**
	```bash
	conda create -n gridfit-dev -c conda-forge python=3.10 cmake make gxx_linux-64 -y
	conda activate gridfit-dev
	conda install -c conda-forge pybind11 pytest numpy scipy psutil r-devtools -y	
    Rscript -e "install.packages(c('Rcpp'), repos='https://cloud.r-project.org')"
	```
3. **Run the install script:**
	```bash
	./install.sh
	```

The `install.sh` script will:
- Clean previous builds
- Build the C++ core
- Build and install the Python and R bindings
- Run example scripts for C++, Python, and R
- Print output from all three so you know everything works

**If you see output from all three languages, your setup is correct!**

---

## Manual Developer Setup (Advanced)

If you want to set up a development environment for editing and testing code, follow these steps:

1. Clone the repository:
	```bash
	git clone https://github.com/rae-gh/grid-fit.git
	cd grid-fit
	```
2. (Optional) Create and activate a conda environment:
	```bash
	conda create -n gridfit-dev -c conda-forge python=3.10 cmake make gxx_linux-64 -y
	conda activate gridfit-dev
	conda install -c conda-forge pybind11 pytest numpy scipy -y
	Rscript -e 'install.packages("devtools")'
	```
3. Install the Python package in editable mode:
	```bash
	python -m pip install -e .
	```
4. Build the C++ core and R package as needed (see CMakeLists.txt and R/README).

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
Rscript tests/R/test_trilinear.R
```

Make sure both tests pass before pushing changes.

---

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

---

## Compiling the C++ Core (Advanced)

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

