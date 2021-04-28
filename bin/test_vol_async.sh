#!/bin/tcsh
# ./spack uninstall --all --force --yes-to-all hdf5-av
# rm -rf ~/.spack/cache
# rm -rf /tmp/hyoklee

./spack install hdf5-vol-async

source ../share/spack/setup-env.csh
spack load hdf5-vol-async

# Set filter plugin environment variable.
set p="`./spack find --paths hdf5-vol-async | tail  -1 | cut -d' ' -f 3-`"
setenv HDF5_PLUGIN_PATH $p/lib/

# Show installed plugin.
ls $p/lib/

# Show installed header.
ls $p/include/







