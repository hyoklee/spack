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
#     spack install hdf5-examples
#
# You can edit this file again by typing:
#
#     spack edit hdf5-examples
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class Hdf5Examples(AutotoolsPackage):
    """Example programs for HDF5"""

    homepage = 'https://www.hdfgroup.org'
    url      = 'https://github.com/HDFGroup/hdf5-examples'
    git = 'https://github.com/HDFGroup/hdf5-examples.git'
    maintainers = ['lrknox']

    version('master', branch='master', git=git,
            commit='9e4fb852f0e1a2019c9ab1e0952c1631f837addf')

    depends_on('hdf5~shared')
    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')
    
    def configure_args(self):
        args = []

        args.append('--disable-shared')
        return args
