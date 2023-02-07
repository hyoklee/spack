# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *


class Hdf5VolDaos(CMakePackage):
    """The HDF5 DAOS VOL connector is an external VOL connector that interfaces with the DAOS API"""

    homepage = ''
    url = 'https://github.com/HDFGroup/vol-daos/releases/download/v1.1.0/hdf5_vol_daos-1.1.0.tar.bz2'
    git = 'https://github.com/HDFGroup/vol-daos.git'

    maintainers = ['soumagne']

    version('master', branch='master', submodules=True)
    version('1.1.0', sha256='b3b20e1ee625321a54b3c193be42f68c8ac3c4f127cee6d53cd39b8f230d567a')

    depends_on('cmake@2.8.12.2:', type='build')
    depends_on('daos@2.0.0:')
    depends_on('hdf5@1.13.0:+hl+mpi+map')

    def cmake_args(self):
        """Populate cmake arguments for HDF5 DAOS."""
        spec = self.spec
        define = self.define        
        parallel_tests = '+mpi' in spec and self.run_tests

        cmake_args = [
            define('BUILD_SHARED_LIBS', True),
            define('BUILD_TESTING', self.run_tests),
        ]

        return cmake_args

    def setup_run_environment(self, env):
        env.prepend_path('HDF5_PLUGIN_PATH', self.prefix.lib)

    def check(self):
        """Unit tests fail when run in parallel."""

        with working_dir(self.build_directory):
            make('test', parallel=False)
