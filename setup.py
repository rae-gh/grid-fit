from setuptools import setup, find_packages
from pybind11.setup_helpers import Pybind11Extension, build_ext

ext_modules = [
    Pybind11Extension(
        "gridfit.gridfit_interp",
        sources=["python/gridfit/interp_py.cpp", "src/interp.cpp", "src/gridfit.cpp"],
        include_dirs=["include"],  # pybind11 handles numpy include automatically
        language="c++",
        cxx_std=11,  # or 14, 17 depending on what you need
    ),
]

setup(
    name="gridfit",
    version="0.1.0",
    packages=find_packages(where="python"),
    package_dir={"": "python"},
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},  # Use pybind11's build_ext
    install_requires=[
        "numpy",
        "pybind11>=2.6.0",
    ],
    # ... other metadata ...
)
