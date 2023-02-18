# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Daos2(MakefilePackage):
    """The Distributed Asynchronous Object Storage (DAOS) is an open-source
       software-defined object store designed from the ground up for massively
       distributed Non Volatile Memory (NVM)."""

    homepage = 'https://github.com/daos-stack/daos'
    git      = 'https://github.com/hyoklee/daos.git'

    version('master', branch='master', submodules=True)
    depends_on('argobots')
    depends_on('boost@develop+python', type='build')
    depends_on('cmocka', type='build')
    depends_on('go', type='build')        
    depends_on('hwloc@master')
    depends_on('isa-l')
    depends_on('isa-l_crypto')
    depends_on('libfuse@3.6.1:')    
    depends_on('libunwind')    
    depends_on('libuuid')
    depends_on('libyaml')
    depends_on('libfabric')
    depends_on('mercury@master+boostsys')
    depends_on('mpich')
    depends_on('openssl')
    depends_on('pmdk')
    depends_on('protobuf-c')
    depends_on('py-distro')
    depends_on('readline')
    depends_on('scons')    
    depends_on('spdk')    
    
