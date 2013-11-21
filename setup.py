from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
from numpy.distutils.misc_util import get_numpy_include_dirs

setup(
    cmdclass = {'build_ext': build_ext},
    ext_modules = [
        Extension( "pycrf", ["pycrf.pyx",
                             "gco-v3.0/graph.cpp",
                             "gco-v3.0/GCoptimization.cpp",
                             "gco-v3.0/LinkedBlockList.cpp",
                             "gco-v3.0/maxflow.cpp"],
                   language="c++",
                   include_dirs=get_numpy_include_dirs()+["gco-v3.0/"],
                  )
        ]
    )
