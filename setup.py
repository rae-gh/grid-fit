"""
Minimal setup.py for C++ extension building.
All metadata is in pyproject.toml (modern best practice).
This file only exists because setuptools doesn't yet support
declaring C++ extensions in pyproject.toml alone.
"""
from setuptools import setup, find_packages
from pybind11.setup_helpers import Pybind11Extension, build_ext

ext_modules = [
    Pybind11Extension(
        "gridfit._core",
        [
            "python/gridfit/interp_py.cpp",  # Your pybind11 bindings
            "src/interp.cpp",                 # Your core C++ code
        ],
        include_dirs=["src", "include"],  # Now it can find interp.h in include/
        cxx_std=11,
    ),
]

# All other metadata is in pyproject.toml
setup(
    packages=find_packages(where="python"),
    package_dir={"": "python"},
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
)