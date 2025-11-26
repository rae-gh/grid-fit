from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import sys

ext_modules = [
    Extension(
        'gridfit_interp',
        sources=['interp_py.cpp'],
        include_dirs=['../include'],
        language='c++'
    )
]

setup(
    name='gridfit_interp',
    version='0.1',
    ext_modules=ext_modules,
    cmdclass={'build_ext': build_ext},
)
