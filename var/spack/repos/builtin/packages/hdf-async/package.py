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


class HdfAsync(Package):
    """FIXME: Put a proper description of your package here."""

    homepage = "https://sdm.lbl.gov/"
    git      = "https://github.com/hpc-io/vol-async"
    maintainers = ['hyoklee']

    version('default', branch='async_vol_register_optional', preferred=True)

    # FIXME: Add dependencies if required.
    depends_on('hdf5-av')
    patch('Makefile.patch')
    patch('src_Makefile.patch')
    def install(self, spec, prefix):
        make()
        make('install')
