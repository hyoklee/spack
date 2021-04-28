#!/bin/tcsh
./spack uninstall --all --force --yes-to-all hdf5-cmake
rm -rf ~/.spack/cache
rm -rf /tmp/hyoklee

# This is for all filters + Pass-through VOL using develop branch.
# ./spack install hdf5-cmake+pv

# This is for all VOLs using develop branch.
# ./spack install hdf5-cmake+pv+cv+av+mpi+threadsafe

# This is for hyoklee/OESS-126 branch.
./spack install hdf5-cmake@hyoklee.OESS-126~zfp~mafisc~szip~zstd~blosc~bshuf~bitgroom~av~pv~cv+mpi+threadsafe

# This is for Cache VOL using OESS-126 branch.
#./spack install hdf5-cmake~zfp~mafisc+szip~zstd~blosc~bshuf~bitgroom+cv+mpi

# This is for Async VOL.
# ./spack install hdf5-cmake~zfp~mafisc+szip~zstd~blosc~bshuf~bitgroom+av~pv~cv+mpi+threadsafe

# This is for all VOLs.
#./spack install hdf5-cmake~zfp~mafisc+szip~zstd~blosc~bshuf~bitgroom+av+cv+pv+mpi+threadsafe
source ../share/spack/setup-env.csh
spack load hdf5-cmake

unsetenv HDF5_PLUGIN_PATH
# This will fail.
h5dump-shared /scr/hyoklee/data/test_zfp_be.h5

# Set filter plugin environment variable.
set p="`./spack find --paths hdf5-cmake | tail  -1 | cut -d' ' -f 3-`"
setenv HDF5_PLUGIN_PATH $p/lib/plugin/

# Show installed plugin.
ls $p/lib/plugin/

# These tests will succeed.
h5dump-shared /scr/hyoklee/data/test_zfp_be.h5
h5dump-shared /scr/hyoklee/data/test_zfp_le.h5
h5dump-shared /scr/hyoklee/data/test_sz.h5
h5dump-shared /scr/hyoklee/data/h5ex_d_zstandard.h5
h5repack-shared -v -f GZIP=1 /scr/hyoklee/data/h5ex_d_zstandard.h5 test_zstd.h5
h5repack-shared -v -f UD=32015,1,3 test_zstd.h5 test_zstandard.h5
h5repack -v -f UD=32015,1,3 test_zstd.h5 test_zstandard.h5

