##############################################################################
# Copyright (c) 2013-2023, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *


class Daos2(MakefilePackage):
    """The Distributed Asynchronous Object Storage (DAOS) is an open-source
       software-defined object store designed from the ground up for massively
       distributed Non Volatile Memory (NVM)."""

    homepage = 'https://github.com/daos-stack/daos'
    git      = 'https://github.com/hyoklee/daos.git'

    version('master', branch='master', submodules=True)

    variant('fwd', default=True,
            description='Bypass root setup and privilege helper')
    variant('debug', default=False,
            description='Enable debugging info and strict compile warnings')

    depends_on('argobots')
    depends_on('mercury@master+boostsys', when='@1.1.0:')
    depends_on('boost@develop+python', type='build', when='@1.1.0:')
    depends_on('cart@daos-1.0', when='@1.0.0')
    depends_on('cart@daos-0.9', when='@0.9.0')
    depends_on('cart@daos-0.8', when='@0.8.0')
    depends_on('cart@daos-0.7', when='@0.7.0')
    depends_on('cart@daos-0.6', when='@0.6.0')
    depends_on('cmocka', type='build')
    depends_on('libfuse@3.6.1:')
    depends_on('hwloc@master')
    depends_on('hwloc@:1.999', when='@:1.0.0')
    depends_on('isa-l')
    depends_on('isa-l_crypto', when='@1.1.0:')
    depends_on('libuuid')
    depends_on('libyaml')
    depends_on('openmpi', when='@:0.8.0')
    depends_on('openssl')
    depends_on('pmdk')
    depends_on('pmdk@1.11.1:', when='@2.0.0:')
    depends_on('protobuf-c')
#    depends_on('py-distro')
#    depends_on('py-pip')
    depends_on('readline')
    depends_on('spdk@18.07.1+fio', when='@0.6.0')
    depends_on('spdk@19.04.1+shared', when='@0.7.0:1.0.0')
    depends_on('spdk@20.01+shared+rdma', when='@1.1.0:1.2.0')
    depends_on('libfabric', when='@0.7.0:')
    depends_on('libunwind')
    depends_on('scons@4.4.0')
    depends_on('go', type='build')


