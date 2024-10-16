# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import shutil
import sys

from spack import *


class Hdf5Cmake(CMakePackage):
    """HDF5 is a data model, library, and file format for storing and managing
    data. It supports an unlimited variety of datatypes, and is designed for
    flexible and efficient I/O and for high volume and complex data.
    """

    homepage = "https://portal.hdfgroup.org"
    url      = "https://support.hdfgroup.org/ftp/HDF5/releases/hdf5-1.10/hdf5-1.10.7/src/hdf5-1.10.7.tar.gz"
    list_url = "https://support.hdfgroup.org/ftp/HDF5/releases"
    list_depth = 3
    git = "https://github.com/HDFGroup/hdf5.git"
    maintainers = ['lrknox', 'hyoklee']

    # Forked versions for VOLs
    version('hpc-io.develop',
            branch='develop',
            git='https://github.com/hpc-io/hdf5.git')
    version('hyoklee.OESS-126', branch='OESS-126',
            git='https://github.com/hyoklee/hdf5.git')
    version('hyoklee.develop', branch='develop',
            git='https://github.com/hyoklee/hdf5.git')

    # A forked version for GPUDirect Storage VFD
    version('jhendersonHDF.H5FD_dynamic', branch='H5FD_dynamic',
            git="https://github.com/jhendersonHDF/hdf5.git")

    # Official HDF5 GitHub repository branches
    version('develop', branch='develop', preferred=True)
    version('develop-1.12', branch='hdf5_1_12')
    version('develop-1.10', branch='hdf5_1_10')
    version('develop-1.8', branch='hdf5_1_8')

    version('1.12.0', sha256='a62dcb276658cb78e6795dd29bf926ed7a9bc4edf6e77025cd2c689a8f97c17a')
    # HDF5 1.12 broke API compatibility, so we currently prefer the latest
    # 1.10 release.  packages that want later versions of HDF5 should specify,
    # e.g., depends_on("hdf5@1.12:") to get 1.12 or higher.
    # version('1.10.7', sha256='7a1a0a54371275ce2dfc5cd093775bb025c365846512961e7e5ceaecb437ef15', preferred=True)
    version('1.10.7', sha256='7a1a0a54371275ce2dfc5cd093775bb025c365846512961e7e5ceaecb437ef15')
    version('1.10.6', sha256='5f9a3ee85db4ea1d3b1fa9159352aebc2af72732fc2f58c96a3f0768dba0e9aa')
    version('1.10.5', sha256='6d4ce8bf902a97b050f6f491f4268634e252a63dadd6656a1a9be5b7b7726fa8')
    version('1.10.4', sha256='8f60dc4dd6ab5fcd23c750d1dc5bca3d0453bdce5c8cdaf0a4a61a9d1122adb2')
    version('1.10.3', sha256='b600d7c914cfa80ae127cd1a1539981213fee9994ac22ebec9e3845e951d9b39')
    version('1.10.2', sha256='bfec1be8c366965a99812cf02ddc97e4b708c1754fccba5414d4adccdc073866')
    version('1.10.1', sha256='048a9d149fb99aaa1680a712963f5a78e9c43b588d0e79d55e06760ec377c172')
    version('1.10.0-patch1', sha256='6e78cfe32a10e6e0629393cdfddf6cfa536571efdaf85f08e35326e1b4e9eff0')
    version('1.10.0', sha256='81f6201aba5c30dced5dcd62f5d5477a2790fd5850e02ac514ca8bf3e2bb375a')

    version('1.8.21', sha256='87d8c82eba5cf766d97cd06c054f4639c1049c4adeaa3a79f77f8bd374f80f37')
    version('1.8.19', sha256='a4335849f19fae88c264fd0df046bc321a78c536b2548fc508627a790564dc38')
    version('1.8.18', sha256='cdb195ad8d9e6782acf24b2488061289f615628c2ccda8457b0a0c3fb7a8a063')
    version('1.8.17', sha256='d9cda297ee76ade9881c4208987939250d397bae6252d0ccb66fa7d24d67e263')
    version('1.8.16', sha256='ed17178abd9928a7237f30370189ba767b9e39e0db45917c2ac4665eb9cb4771')
    version('1.8.15', sha256='4e963216b7d32469596bc1321a8c3f6e0c278dcbbdb7be6414c63c081b34c275')
    version('1.8.14', sha256='1dbefeeef7f591897c632b2b090db96bb8d35ad035beaa36bc39cb2bc67e0639')
    version('1.8.13', sha256='82f6b38eec103b4fccfbf14892786e0c27a8135d3252d8601cf5bf20066d38c1')
    version('1.8.12', sha256='b5cccea850096962b5fd9e96f22c4f47d2379224bb41130d9bc038bb6c37dfcb')
    version('1.8.10', sha256='4813b79c5fb8701a625b9924b8203bc7154a77f9b826ad4e034144b4056a160a')

    variant('debug', default=False,
            description='Builds a debug version of the library')
    variant('shared', default=True,
            description='Builds a shared version of the library')
    variant('static', default=True,
            description='Builds a static version of the library')
    conflicts('~static', '~shared')

    variant('hl', default=False, description='Enable the high-level library')
    variant('cxx', default=False, description='Enable C++ support')
    variant('fortran', default=False, description='Enable Fortran support')
    variant('java', default=False, description='Enable Java support')
    variant('threadsafe', default=False,
            description='Enable thread-safe capabilities')
    variant('tools', default=True, description='Enable build tools')
    variant('mpi', default=False, description='Enable MPI support')
    variant('szip', default=True, description='Enable szip support')
    variant('zlib', default=True, description='Enable zlib support')
    variant('pic', default=True,
            description='Produce position-independent code (for shared libs)')
    # Build HDF5 with API compatibility.
    variant('api', default='none', description='Choose api compatibility',
            values=('none', 'v114', 'v112', 'v110', 'v18', 'v16'), multi=False)

    variant('vfd-gds', default=False, description='Enable GPUDirect Storage VFD')

    # Build filter plugins.
    variant('blosc', default=True, description='Enable blosc support')
    variant('bshuf', default=True, description='Enable bshuf support')
    variant('bz2', default=True, description='Enable bz2 support')
    variant('jpeg', default=True, description='Enable jpeg support')
    variant('lz4', default=True, description='Enable lz4 support')
    variant('lzf', default=True, description='Enable lzf support')
    variant('szf', default=True, description='Enable szf support')
    variant('zfp', default=True, description='Enable zfp support')
    variant('zstd', default=True, description='Enable zstd support')
    variant('bitgroom', default=True, description='Enable bitgroom support')
    variant('mafisc', default=True, description='Enable mafisc support')
    variant('pv', default=False, description='Enable pass-through ext. VOL')
    variant('av', default=False, description='Enable async VOL')
    variant('cv', default=False, description='Enable cache VOL')

    conflicts('api=v114', when='@1.6:1.12.99', msg='v114 is not compatible with this release')
    conflicts('api=v114', when='@:develop-1.12.99', msg='v114 is not compatible with this release')
    conflicts('api=v112', when='@1.6:1.10.99', msg='v112 is not compatible with this release')
    conflicts('api=v112', when='@:develop-1.10.99', msg='v112 is not compatible with this release')
    conflicts('api=v110', when='@1.6:1.8.99', msg='v110 is not compatible with this release')
    conflicts('api=v110', when='@:develop-1.8.99', msg='v110 is not compatible with this release')
    conflicts('api=v18', when='@1.6:1.6.99', msg='v18 is not compatible with this release')
    conflicts('api=v18', when='@:develop-1.6.99', msg='v18 is not compatible with this release')

    depends_on('cmake@3.12.4:', type='build')
    depends_on('mpi', when='+mpi')
    depends_on('java', type=('build', 'run'), when='+java')
    conflicts('+java', when='~shared')
    # numactl does not currently build on darwin
    if sys.platform != 'darwin':
        depends_on('numactl', when='+mpi+fortran')
    depends_on('szip', when='+szip')
    depends_on('zlib@1.2.5:', when='+zlib')
    depends_on('zstd', when='+zstd')
    depends_on('argobots', when='+av')

    # The Java wrappers and associated libhdf5_java library
    # were first available in 1.10
    conflicts('+java', when='@:1.9')

    # There are several officially unsupported combinations of the features:
    # 1. Thread safety is not guaranteed via high-level C-API but in some cases
    #    it works.
    # conflicts('+threadsafe+hl')

    # 2. Thread safety is not guaranteed via Fortran (CXX) API, but it's
    #    possible for a dependency tree to contain a package that uses Fortran
    #    (CXX) API in a single thread and another one that uses low-level C-API
    #    in multiple threads. To allow for such scenarios, we don't specify the
    #    following conflicts.
    # conflicts('+threadsafe+cxx')
    # conflicts('+threadsafe+fortran')

    # 3. Parallel features are not supported via CXX API, but for the reasons
    #    described in #2 we allow for such combination.
    # conflicts('+mpi+cxx')

    # There are known build failures with intel@18.0.1. This issue is
    # discussed and patch is provided at
    # https://software.intel.com/en-us/forums/intel-fortran-compiler-for-linux-and-mac-os-x/topic/747951.
    patch('h5f90global-mult-obj-same-equivalence-same-common-block.patch',
          when='@1.10.1%intel@18')

    # Turn line comments into block comments to conform with pre-C99 language
    # standards. Versions of hdf5 after 1.8.10 don't require this patch,
    # either because they conform to pre-C99 or neglect to ask for pre-C99
    # language standards from their compiler. The hdf5 build system adds
    # the -ansi cflag (run 'man gcc' for info on -ansi) for some versions
    # of some compilers (see hdf5-1.8.10/config/gnu-flags). The hdf5 build
    # system does not provide an option to disable -ansi, but since the
    # pre-C99 code is restricted to just five lines of line comments in
    # three src files, this patch accomplishes the simple task of patching the
    # three src files and leaves the hdf5 build system alone.
    patch('pre-c99-comments.patch', when='@1.8.10')

    # There are build errors with GCC 8, see
    # https://forum.hdfgroup.org/t/1-10-2-h5detect-compile-error-gcc-8-1-0-on-centos-7-2-solved/4441
    patch('https://salsa.debian.org/debian-gis-team/hdf5/raw/bf94804af5f80f662cad80a5527535b3c6537df6/debian/patches/gcc-8.patch',
          sha256='57cee5ff1992b4098eda079815c36fc2da9b10e00a9056df054f2384c4fc7523',
          when='@1.10.2%gcc@8:')

    # Disable MPI C++ interface when C++ is disabled, otherwise downstream
    # libraries fail to link; see https://github.com/spack/spack/issues/12586
    patch('h5public-skip-mpicxx.patch', when='@1.8.10:1.10.5+mpi~cxx',
          sha256='b61e2f058964ad85be6ee5ecea10080bf79e73f83ff88d1fa4b602d00209da9c')

    # The argument 'buf_size' of the C function 'h5fget_file_image_c' is
    # declared as intent(in) though it is modified by the invocation. As a
    # result, aggressive compilers such as Fujitsu's may do a wrong
    # optimization to cause an error.
    def patch(self):
        filter_file(
            'INTEGER(SIZE_T), INTENT(IN) :: buf_size',
            'INTEGER(SIZE_T), INTENT(OUT) :: buf_size',
            'fortran/src/H5Fff.F90',
            string=True, ignore_absent=True)
        filter_file(
            'INTEGER(SIZE_T), INTENT(IN) :: buf_size',
            'INTEGER(SIZE_T), INTENT(OUT) :: buf_size',
            'fortran/src/H5Fff_F03.f90',
            string=True, ignore_absent=True)

    filter_compiler_wrappers('h5cc', 'h5c++', 'h5fc', relative_root='bin')

    def url_for_version(self, version):
        url = "https://support.hdfgroup.org/ftp/HDF5/releases/hdf5-{0}/hdf5-{1}/src/hdf5-{1}.tar.gz"
        return url.format(version.up_to(2), version)

    @property
    def libs(self):
        """HDF5 can be queried for the following parameters:

        - "hl": high-level interface
        - "cxx": C++ APIs
        - "fortran": Fortran APIs
        - "java": Java APIs

        :return: list of matching libraries
        """
        query_parameters = self.spec.last_query.extra_parameters

        shared = '+shared' in self.spec

        # This map contains a translation from query_parameters
        # to the libraries needed
        query2libraries = {
            tuple(): ['libhdf5'],
            ('cxx', 'fortran', 'hl', 'java'): [
                'libhdf5hl_fortran',
                'libhdf5_hl_cpp',
                'libhdf5_hl',
                'libhdf5_fortran',
                'libhdf5_java',
                'libhdf5',
            ],
            ('cxx', 'hl'): [
                'libhdf5_hl_cpp',
                'libhdf5_hl',
                'libhdf5',
            ],
            ('fortran', 'hl'): [
                'libhdf5hl_fortran',
                'libhdf5_hl',
                'libhdf5_fortran',
                'libhdf5',
            ],
            ('hl',): [
                'libhdf5_hl',
                'libhdf5',
            ],
            ('cxx', 'fortran'): [
                'libhdf5_fortran',
                'libhdf5_cpp',
                'libhdf5',
            ],
            ('cxx',): [
                'libhdf5_cpp',
                'libhdf5',
            ],
            ('fortran',): [
                'libhdf5_fortran',
                'libhdf5',
            ],
            ('java',): [
                'libhdf5_java',
                'libhdf5',
            ]
        }

        # Turn the query into the appropriate key
        key = tuple(sorted(query_parameters))
        libraries = query2libraries[key]

        return find_libraries(
            libraries, root=self.prefix, shared=shared, recursive=True
        )

    @run_before('cmake')
    def fortran_check(self):
        if '+fortran' in self.spec and not self.compiler.fc:
            msg = 'cannot build a Fortran variant without a Fortran compiler'
            raise RuntimeError(msg)

    def java_check(self):
        if '+java' in self.spec and not self.compiler.java:
            msg = 'cannot build a Java variant without a Java compiler'
            raise RuntimeError(msg)

    def cmake_use_cacheinit(self, args):
        # The following will not work.
        # args.append('-C /scr/hyoklee/src/hdf5-byrn/config/cmake/cacheinit.cmake')
        # Instead, split the arguments like the following
        args.append('-C')
        # Use full path instead of 'config/cmake/cacheinit.cmake'.
        # E.g., args.append('/scr/hyoklee/src/hdf5/config/cmake/cacheinit.cmake')
        cf = self.build_directory + '/../spack-src/config/cmake/cacheinit.cmake'
        args.append(cf)
        args.append('-DHDF5_ENABLE_PLUGIN_SUPPORT:BOOL=ON')
        args.append('-DPLUGIN_GIT_URL:STRING=https://github.com/hyoklee/hdf5_plugins.git')
        # Use git instead of tar.gz archives.
        args.append('-DHDF5_ALLOW_EXTERNAL_SUPPORT:STRING=GIT')

        # If you want to use tar.gz, use the followings.
        # args.append('-DHDF5_ALLOW_EXTERNAL_SUPPORT:STRING=TGZ')
        # args.append('-DTGZPATH:STRING=/scr/hyoklee/x')

    def cmake_args(self):

        # Always enable this option. This does not actually enable any
        # features: it only *allows* the user to specify certain
        # combinations of other arguments. Enabling it just skips a
        # sanity check in configure, so this doesn't merit a variant.
        args = [self.define('ALLOW_UNSUPPORTED', True)]

        args.append(self.define_from_variant('BUILD_SHARED_LIBS', 'shared'))

        if '+pic' in self.spec:
            args.extend([
                'CFLAGS='   + self.compiler.cc_pic_flag,
                'CXXFLAGS=' + self.compiler.cxx_pic_flag,
                'FCFLAGS='  + self.compiler.fc_pic_flag,
            ])

        if '+zlib' in self.spec:
            args.append('-DHDF5_ENABLE_Z_LIB_SUPPORT:BOOL=ON')
            args.append(
                '-DZLIB_INCLUDE_DIR:PATH={0}'.format(
                    self.spec['zlib'].prefix.include))
            args.append(
                '-DZLIB_DIR:PATH={0}'.format(
                    self.spec['zlib'].prefix.lib))
        else:
            args.append('-DHDF5_ENABLE_Z_LIB_SUPPORT:BOOL=OFF')

        if '+szip' in self.spec:
            args.append('-DHDF5_ENABLE_SZIP_SUPPORT:BOOL=ON')
            args.append('-DHDF5_ENABLE_SZIP_ENCODING:BOOL=ON')
            args.append(
                '-DSZIP_INCLUDE_DIR:PATH={0}'.format(
                    self.spec['szip'].prefix.include))
            args.append(
                '-DSZIP_DIR:PATH={0}'.format(
                    self.spec['szip'].prefix.lib))
        else:
            args.append('-DHDF5_ENABLE_SZIP_SUPPORT:BOOL=OFF')

        # Build plugin filters.
        if '+vfd-gds' not in self.spec:
            self.cmake_use_cacheinit(args)
        if '~blosc' in self.spec:
            args.append('-DENABLE_BLOSC:BOOL=OFF')

        if '~bshuf' in self.spec:
            args.append('-DENABLE_BSHUF:BOOL=OFF')

        if '~bz2' in self.spec:
            args.append('-DENABLE_BZIP2:BOOL=OFF')

        if '~jpeg' in self.spec:
            args.append('-DENABLE_JPEG:BOOL=OFF')

        if '~lz4' in self.spec:
            args.append('-DENABLE_LZ4:BOOL=OFF')

        if '~lzf' in self.spec:
            args.append('-DENABLE_LZF:BOOL=OFF')

        if '~zfp' in self.spec:
            args.append('-DENABLE_ZFP:BOOL=OFF')

        if '~szf' in self.spec:
            args.append('-DENABLE_SZF:BOOL=OFF')

        if '~zstd' in self.spec:
            args.append('-DENABLE_ZSTD:BOOL=OFF')
        else:
            args.append(
                '-DZSTD_INCLUDE_DIR:PATH={0}'.format(
                    self.spec['zstd'].prefix.include))
            args.append(
                '-DZSTD_DIR:PATH={0}'.format(
                    self.spec['zstd'].prefix.lib))

        if '~bitgroom' in self.spec:
            args.append('-DENABLE_BITGROOM:BOOL=OFF')

        if '~mafisc' in self.spec:
            args.append('-DENABLE_MAFISC:BOOL=OFF')

        if '~pv' in self.spec:
            args.append('-DENABLE_PV:BOOL=OFF')

        if '~av' in self.spec:
            args.append('-DENABLE_AV:BOOL=OFF')

        if '~cv' in self.spec:
            args.append('-DENABLE_CV:BOOL=OFF')

        if '+mpi' in self.spec:
            args.append('-DHDF5_ENABLE_PARALLEL=ON')
            args.append('-DMPIEXEC_NUMPROC_FLAG:STRING=-n')
            args.append('-DMPIEXEC_MAX_NUMPROCS:STRING=6')
            args.append('-DCMAKE_C_COMPILER={0}'.format(self.spec['mpi'].mpicc))
            args.append('-DCMAKE_CXX_COMPILER={0}'.format(self.spec['mpi'].mpicxx))
            args.append(
                '-DCMAKE_Fortran_COMPILER={0}'.format(self.spec['mpi'].mpifc))
        else:
            args.append('-DHDF5_ENABLE_PARALLEL=OFF')

        if '+static' in self.spec:
            args.append('-DONLY_SHARED_LIBS=OFF')
        else:
            args.append('-DONLY_SHARED_LIBS=ON')

        if '+debug' in self.spec:
            args.append('-DCMAKE_BUILD_TYPE=Debug')
        else:
            args.append('-DCMAKE_BUILD_TYPE=Release')

        args.append(self.define_from_variant('HDF5_ENABLE_THREADSAFE', 'threadsafe'))

        args.append(self.define_from_variant('HDF5_BUILD_HL_LIB', 'hl'))

        args.append(self.define_from_variant('HDF5_BUILD_CPP', 'cxx'))

        args.append(self.define_from_variant('HDF5_BUILD_FORTRAN', 'fortran'))

        args.append(self.define_from_variant('HDF5_BUILD_JAVA', 'java'))

        args.append(self.define_from_variant('HDF5_BUILD_TOOLS', 'tools'))

        # if self.run_tests:
        #     args.append('-DBUILD_TESTING=ON')
        # else:
        #    args.append('-DBUILD_TESTING=OFF')

        if self.spec.variants['api'].value != 'none':
            args.append(
                '-DDEFAULT_API_VERSION={0}'.format(
                    self.spec.variants['api'].value))

        return args

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def test(self):
        # https://spack.readthedocs.io/en/latest/build_systems/custompackage.html
        make('test')

    def check_install(self):
        # Build and run a small program to test the installed HDF5 library
        spec = self.spec
        print("Checking HDF5 installation...")
        checkdir = "spack-check"
        with working_dir(checkdir, create=True):
            source = r"""
#include <hdf5.h>
#include <assert.h>
#include <stdio.h>
int main(int argc, char **argv) {
  unsigned majnum, minnum, relnum;
  herr_t herr = H5get_libversion(&majnum, &minnum, &relnum);
  assert(!herr);
  printf("HDF5 version %d.%d.%d %u.%u.%u\n", H5_VERS_MAJOR, H5_VERS_MINOR,
         H5_VERS_RELEASE, majnum, minnum, relnum);
  return 0;
}
"""
            expected = """\
HDF5 version {version} {version}
""".format(version=str(spec.version.up_to(3)))
            with open("check.c", 'w') as f:
                f.write(source)
            if '+mpi' in spec:
                cc = Executable(spec['mpi'].mpicc)
            else:
                cc = Executable(self.compiler.cc)
            cc(*(['-c', "check.c"] + spec['hdf5'].headers.cpp_flags.split()))
            cc(*(['-o', "check",
                  "check.o"] + spec['hdf5'].libs.ld_flags.split()))
            try:
                check = Executable('./check')
                output = check(output=str)
            except ProcessError:
                output = ""
            success = output == expected
            if not success:
                print("Produced output does not match expected output.")
                print("Expected output:")
                print('-' * 80)
                print(expected)
                print('-' * 80)
                print("Produced output:")
                print('-' * 80)
                print(output)
                print('-' * 80)
                raise RuntimeError("HDF5 install check failed")
        shutil.rmtree(checkdir)
