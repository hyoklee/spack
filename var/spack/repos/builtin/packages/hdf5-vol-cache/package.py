# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install hdf5-cv
#
# You can edit this file again by typing:
#
#     spack edit hdf5-cv
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class Hdf5VolCache(CMakePackage):
    """Package for HDF5 cache VOL."""

    homepage = "https://sdm.lbl.gov/"
    git      = "https://github.com/hpc-io/vol-cache.git"

    maintainers = ['hyoklee']

    version('default', branch='master')
    version('cmake', branch='master',
            git='https://github.com/hyoklee/vol-cache.git')
    version('cmake-local', branch='master',
            git='file:///home/hyoklee/vol-cache', preferred=True)
    
    # Set hdf5-cmake package option.
    o_flt = '~zfp~mafisc~szip~zstd~blosc~bshuf~bitgroom'
    o_vol = '~av~pv~cv'
    o_par = '+mpi+threadsafe'
    o = o_flt+o_vol+o_par
    # depends_on('hdf5-cmake@av'+o)
    depends_on('hdf5-av')
    
    def cmake_args(self):
        """Populate cmake arguments for HDF5 DAOS."""
        spec = self.spec

        args = [
            '-DBUILD_SHARED_LIBS:BOOL=ON',
            '-DBUILD_TESTING:BOOL=ON'
        ]
        return args
