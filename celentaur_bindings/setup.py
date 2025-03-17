from setuptools import setup, Extension
import pybind11
import os

# Define include directories: pybind11's headers and the system include paths.
include_dirs = [
    pybind11.get_include(),
    "/usr/include" 
]

# Define library directories: where the Celantaur SDK (and its dependencies) are installed.
library_dirs = [
    "/usr/lib/x86_64-linux-gnu"
]

# Specify the libraries to link against. Update this to match the actual name of the SDK library.
libraries = [
    "celantur_processing"
]

# Extra compile arguments: setting the C++ standard.
extra_compile_args = ["-std=c++11"]

ext_modules = [
    Extension(
        "celantaur_bindings",
        sources=["celentaur_bindings.cpp"],
        include_dirs=include_dirs,
        library_dirs=library_dirs,
        libraries=libraries,
        language="c++",
        extra_compile_args=extra_compile_args
    )
]

setup(
    name="celantaur_bindings",
    version="0.1",
    description="Python bindings for Celantaur SDK using pybind11",
    ext_modules=ext_modules,
)
