#!/bin/tcsh
./spack uninstall --all --force --yes-to-all hdf5-cmake@jhendersonHDF.H5FD_dynamic
rm -rf ~/.spack/cache
rm -rf /tmp/hyoklee

./spack install hdf5-cmake@jhendersonHDF.H5FD_dynamic~zfp~mafisc~zstd~blosc~bshuf~bitgroom~av~pv~cv~mpi~threadsafe+vfd-gds

source ../share/spack/setup-env.csh
spack load hdf5-cmake@jhendersonHDF.H5FD_dynamic

# Show installed library.
set p="`./spack find --paths hdf5-cmake@jhendersonHDF.H5FD_dynamic | tail  -1 | cut -d' ' -f 3-`"
ls $p/lib/
