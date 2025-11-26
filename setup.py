import numpy
from setuptools import setup, Extension, find_packages

ext_modules = [
    Extension(
        "gridfit.gridfit_interp",  # This is the important part!
        sources=["python/gridfit/interp_py.cpp", "src/interp.cpp"],
        include_dirs=[numpy.get_include(), "include"],
        language="c++",
    ),
]

setup(
    name="gridfit",
    version="0.1.0",
    packages=find_packages(where="python"),
    package_dir={"": "python"},
    ext_modules=ext_modules,
    # ... other metadata ...
)