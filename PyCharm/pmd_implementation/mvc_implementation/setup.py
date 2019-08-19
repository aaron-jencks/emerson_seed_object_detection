from distutils.core import setup
from Cython.Build import cythonize

import numpy as np

setup(
    ext_modules=cythonize(['data_util\\cy_scatter.pyx', 'cam_util\\cy_collection_util.pyx']),
    include_dirs=[np.get_include()]
)