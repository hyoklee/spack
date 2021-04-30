# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Hdf5VolTests(CMakePackage):
    """This package Htests DF5 Virtual Object Layer (VOL)."""

    homepage = "https://www.hdfgroup.org"
    git      = "https://github.com/HDFGroup/vol-tests"

    maintainers = ['hyoklee']

    version('master', commit='9a147d3')
    version('hyoklee.master', commit='27209af',
            git='https://github.com/hyoklee/vol-tests', preferred=True)
    
    depends_on('hdf5-vol-async')
