#!/usr/bin/tcsh
rm -rf ~/.spack/cache
rm -rf /tmp/hyoklee
./spack uninstall --all --force --yes-to-all hdf5-cmake
./spack install hdf5-cmake
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
