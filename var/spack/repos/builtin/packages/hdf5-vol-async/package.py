# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

class Hdf5VolAsync(CMakePackage):
    """This package enables asynchronous IO in HDF5."""

    homepage = "https://sdm.lbl.gov/"
    git      = "https://github.com/hpc-io/vol-async"
    maintainers = ['hyoklee']

    version('async_vol_register_optional', branch='async_vol_register_optional')
    version('hyoklee.async_vol_register_optional',
            branch='async_vol_register_optional',
            git = "https://github.com/hyoklee/vol-async"            
            preferred=True)

    depends_on('argobots@main')
    depends_on('hdf5-hpc-io')

    # These are for testing with generic 'make' command.
    # patch('Makefile.patch')
    # patch('src_Makefile.patch')
    # patch('test_Makefile.patch')
    def cmake_args(self):
        """Populate cmake arguments for HDF5 VOL."""
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
