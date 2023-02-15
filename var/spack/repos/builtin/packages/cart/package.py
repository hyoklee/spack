# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Cart(SConsPackage):
    """Collective and RPC Transport (CaRT)"""

    homepage = 'https://github.com/daos-stack/cart'
    git      = 'https://github.com/daos-stack/cart.git'

    version('master', branch='master', submodules=True)
    version('daos-1.0', commit='4cd401d159b14f431f4a77e94ae0e0eebce5f0e3', submodules=True)
    version('daos-0.9', commit='63fa727c055c2446f4f6f2d06d3aec8e84071c2b', submodules=True)
    version('daos-0.8', commit='4d03620dcb0304ab969d61b46b4263acc8b878c4', submodules=True)
    version('daos-0.7', commit='d570c336237262d534ecc07c587e0eee7a778da2', submodules=True)
    version('daos-0.6', commit='7bde2eaec684faa02372caca464b96136348aad4', submodules=True)

    depends_on('boost',  type='build')
    depends_on('cmocka', type='build')
    depends_on('mercury+boostsys')
    depends_on('openmpi', when='@:daos-0.8')
    depends_on('pmix',   when='@:daos-0.8')
    depends_on('openssl')
    depends_on('libuuid')
    depends_on('libyaml')

    patch('cart_include.patch')
    patch('cart_noblock.patch',       when='@daos-0.9:')
    patch('cart_load_mpi.patch',      when='@daos-0.9:')
    patch('cart_werror_scons.patch',  when='@:daos-0.9')
    patch('cart_werror_master.patch', when='@daos-0.8:')
    patch('cart_werror_0_6.patch',    when='@:daos-0.7')
    patch('cart_group_alloc.patch',   when='@daos-0.6')
    patch('cart_na_error.patch',      when='@daos-0.6')
    patch('cart_hg_0_9.patch',        when='@:daos-0.9')

    def build_args(self, spec, prefix):
        args = [
            'PREFIX={0}'.format(prefix),
            'BOOST_PREBUILT={0}'.format(spec['boost'].prefix),
            'CMOCKA_PREBUILT={0}'.format(spec['cmocka'].prefix),
            'CRYPTO_PREBUILT={0}'.format(spec['openssl'].prefix),
            'MERCURY_PREBUILT={0}'.format(spec['mercury'].prefix),
            'UUID_PREBUILT={0}'.format(spec['libuuid'].prefix),
        ]

        if self.spec.satisfies('@:daos-0.8'):
            args.append('OMPI_PREBUILT={0}'.format(spec['openmpi'].prefix))
            args.append('PMIX_PREBUILT={0}'.format(spec['pmix'].prefix))

        return args 
