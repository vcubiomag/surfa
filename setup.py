#!/usr/bin/env python

import re
import pathlib
from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy as np

# --- Version Reading Logic (Dynamic) ---
# This is needed because 'version' is marked as 'dynamic' in pyproject.toml
base_dir = pathlib.Path(__file__).parent.resolve()
init_file = base_dir.joinpath('surfa/__init__.py')
init_text = open(init_file, 'rt').read()
pattern = r"^__version__ = ['\"]([^'\"]*)['\"]"
match = re.search(pattern, init_text, re.M)
if not match:
    raise RuntimeError(f'Unable to find __version__ in {init_file}.')
version = match.group(1)


# --- Cython Extension Logic (Dynamic) ---
# This build logic cannot be expressed in pyproject.toml
ext_opts = dict(extra_compile_args=['-O3', '-std=c99'])
extensions = [
    Extension('surfa.image.interp', [f'surfa/image/interp.pyx'], **ext_opts),
    Extension('surfa.mesh.intersection', [f'surfa/mesh/intersection.pyx'], **ext_opts),
]

extensions = cythonize(extensions, compiler_directives={'language_level' : '3'})
include_dirs = [np.get_include()]


# --- Minimal Setup Call ---
# All static metadata (name, description, classifiers, etc.)
# has been moved to pyproject.toml.
setup(
    version=version,
    ext_modules=extensions,
    include_dirs=include_dirs,
)
