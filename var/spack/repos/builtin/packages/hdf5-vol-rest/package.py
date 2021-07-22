# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *


class Hdf5VolRest(CMakePackage):
    """The HDF5 REST VOL connector is a plugin for HDF5 designed with the goal of
allowing HDF5 applications to utilize web-based storage systems by translating
HDF5 API calls into HTTP-based REST calls, as defined by the HDF5 REST API."""

    homepage = "https://hdfgroup.org"
    url      = "https://github.com/HDFGroup/vol-rest"

    maintainers = ['hyoklee']

    version('develop', branch='hdf5_1_12_update', 
            git='https://github.com/HDFGroup/vol-rest.git', preferred=True)

    depends_on('cmake@3.19.7')
    depends_on('yajl')

    def cmake_args(self):
        """Set CMake arguments."""
        spec = self.spec

        args = [
            '-DBUILD_SHARED_LIBS:BOOL=ON',
            '-DBUILD_TESTING:BOOL=ON'
        ]

        return args
    

    #def setup_run_environment(self, env):
        # env.prepend_path('HDF5_PLUGIN_PATH', self.prefix.lib)
        # env.prepend_path('HDF5_VOL_CONNECTOR',
        #                 'async under_vol=0;under_info={}')        

    def check(self):
        make('test')
