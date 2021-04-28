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
#     spack install hdf-async
#
# You can edit this file again by typing:
#
#     spack edit hdf-async
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class Hdf5VolAsync(CMakePackage):
    """FIXME: Put a proper description of your package here."""

    homepage = "https://sdm.lbl.gov/"
    # git      = "https://github.com/hpc-io/vol-async"
    git      = "https://github.com/hyoklee/vol-async"
    maintainers = ['hyoklee']

    version('default', branch='async_vol_register_optional', preferred=True)

    # FIXME: Add dependencies if required.
    depends_on('hdf5-hpc-io')
    # patch('Makefile.patch')
    # patch('src_Makefile.patch')
    # patch('test_Makefile.patch')
    def cmake_args(self):
        """Populate cmake arguments for HDF5 DAOS."""
        spec = self.spec

        args = [
            '-DBUILD_SHARED_LIBS:BOOL=ON',
            '-DBUILD_TESTING:BOOL=ON'
        ]

        return args
    

    #def setup_run_environment(self, env):
        # env.prepend_path('HDF5_PLUGIN_PATH', self.prefix.lib)
        #env.prepend_path('HDF5_VOL_CONNECTOR',
        #                 'async under_vol=0;under_info={}')        

    def check(self):
        make('test')
