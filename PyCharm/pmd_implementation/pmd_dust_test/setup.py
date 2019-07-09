from distutils.core import setup
from Cython.Build import cythonize

import numpy as np

setup(
    ext_modules=cythonize(['./cam_util/cy_collection_util.pyx', './distribution.pyx']),
    include_dirs=[np.get_include()]
)