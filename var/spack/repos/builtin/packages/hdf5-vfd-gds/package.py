# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Hdf5VfdGds(CMakePackage, CudaPackage):
    """This pacakge enables GPU Direct Storage Virtual File Driver in HDF5."""

    # Package info
    homepage    = 'https://github.com/hpc-io/vfd-gds'
    # url         = 'https://github.com/LLNL/zfp/releases/download/0.5.5/zfp-0.5.5.tar.gz'
    git         = 'https://github.com/hpc-io/vfd-gds.git'
    maintainers = ['hyoklee']

    # Versions
    version('1.0.0', branch='master')
    version('hyoklee', branch='master', git='https://github.com/hyoklee/vfd-gds.git', default=True)
    
    # Dependencies
    depends_on('cmake@3.4.0:')
    depends_on('hdf5@develop-1.13')    
    depends_on('cuda')

    def cmake_args(self):
        spec = self.spec

        # CMake options
        args = [
            self.define('BUILD_TESTING', self.run_tests),
        ]

        return args
