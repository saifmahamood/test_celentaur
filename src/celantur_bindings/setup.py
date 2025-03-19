from setuptools import setup, Extension
import pybind11

include_dirs = [
    pybind11.get_include(),
    pybind11.get_include(user=True),
    "/usr/include",              # General system includes
    "/usr/include/opencv4",        # OpenCV headers are in opencv4
    "/usr/local/include/common-module",  # For CelanturDetection.h
    "/usr/local/include/CelanturSDK"       # For CelanturSDKInterface.h
]

library_dirs = [
    "/usr/lib/x86_64-linux-gnu",
    "/usr/local/lib"  # Where the Celantur SDK libraries are installed
]

# Link against libCelanturSDK.so and libcommon-module.so
libraries = [
    "CelanturSDK", "common-module"
]

extra_compile_args = ["-std=c++17"]

ext_modules = [
    Extension(
        "celantur_bindings",
        sources=["celantur_bindings.cpp"],
        include_dirs=include_dirs,
        library_dirs=library_dirs,
        libraries=libraries,
        language="c++",
        extra_compile_args=extra_compile_args
    )
]

setup(
    name="celantur_bindings",
    version="0.1",
    description="Python bindings for Celantur SDK using pybind11",
    ext_modules=ext_modules,
)
