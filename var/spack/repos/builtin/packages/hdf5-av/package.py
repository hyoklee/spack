# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import shutil
import sys

from spack import *


class Hdf5Av(CMakePackage):
    git = "https://github.com/hpc-io/hdf5.git"
    version('async', branch='async_vol_register_optional', preferred=True)
    maintainers = ['hyoklee']
    variant('hl', default=False, description='Enable the high-level library')
    variant('cxx', default=False, description='Enable C++ support')
    variant('fortran', default=False, description='Enable Fortran support')
    variant('debug', default=False,
            description='Builds a debug version of the library')
    variant('shared', default=True,
            description='Builds a shared version of the library')
    variant('threadsafe', default=True,
            description='Enable thread-safe capabilities')
    variant('tools', default=True, description='Enable build tools')
    variant('mpi', default=True, description='Enable MPI support')
    # variant('szip', default=True, description='Enable szip support')    
    # variant('zlib', default=True, description='Enable zlib support')    
    variant('pic', default=True,
            description='Produce position-independent code (for shared libs)')
    depends_on('cmake@3.12.4:', type='build')
    depends_on('mpi', when='+mpi')
    # numactl does not currently build on darwin
    if sys.platform != 'darwin':
        depends_on('numactl', when='+mpi+fortran')
    # depends_on('szip', when='+szip')    
    # depends_on('zlib@1.2.5:', when='+zlib')
    # depends_on('zstd', when='+zstd')
    depends_on('argobots@main')

    # patch('cmake.patch')
    patch('cacheinit.patch')    
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


    @property
    def libs(self):
        """HDF5 can be queried for the following parameters:

        :return: list of matching libraries
        """
        query_parameters = self.spec.last_query.extra_parameters

        shared = '+shared' in self.spec

        # This map contains a translation from query_parameters
        # to the libraries needed
        query2libraries = {
            tuple(): ['libhdf5'],
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


    def cmake_use_cacheinit(self, args):
        # The following will not work.
        # args.append('-C /scr/hyoklee/src/hdf5-byrn/config/cmake/cacheinit.cmake')
        # Instead, split the arguments like the following 
        args.append('-C')
        # Use full path instead of 'config/cmake/cacheinit.cmake'.
        # E.g., args.append('/scr/hyoklee/src/hdf5/config/cmake/cacheinit.cmake')
        cf = self.build_directory+'/../spack-src/config/cmake/cacheinit.cmake'
        args.append(cf)
        args.append('-DHDF5_ENABLE_PLUGIN_SUPPORT:BOOL=ON')
        args.append('-DPLUGIN_GIT_URL:STRING=https://github.com/hyoklee/hdf5_plugins.git')
        # Use git instead of tar.gz archives.
        args.append('-DHDF5_ALLOW_EXTERNAL_SUPPORT:STRING=GIT')

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

        # Build plugin filters.
        self.cmake_use_cacheinit(args)
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
        args.append(self.define_from_variant('HDF5_BUILD_TOOLS', 'tools'))
        
        args.append('-DENABLE_BITGROOM:BOOL=OFF')
        args.append('-DENABLE_BLOSC:BOOL=OFF')                
        args.append('-DENABLE_BSHUF:BOOL=OFF')
        args.append('-DENABLE_BZIP2:BOOL=OFF')
        args.append('-DENABLE_JPEG:BOOL=OFF')
        args.append('-DENABLE_LZ4:BOOL=OFF')
        args.append('-DENABLE_LZF:BOOL=OFF')
        args.append('-DENABLE_SZF:BOOL=OFF')
        args.append('-DENABLE_MAFISC:BOOL=OFF')
        args.append('-DENABLE_ZFP:BOOL=OFF')        
        args.append('-DENABLE_ZSTD:BOOL=OFF')
        args.append('-DENABLE_PV:BOOL=OFF')
        args.append('-DENABLE_CV:BOOL=OFF')
        
        if self.run_tests:
            args.append('-DBUILD_TESTING=ON')
        else:
           args.append('-DBUILD_TESTING=OFF')

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
