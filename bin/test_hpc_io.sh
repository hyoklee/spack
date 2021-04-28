#!/bin/tcsh
./spack uninstall --all --force --yes-to-all hdf5-hpc-io
rm -rf ~/.spack/cache
rm -rf /tmp/hyoklee

./spack install hdf5-hpc-io

source ../share/spack/setup-env.csh
spack load hdf5-hpc-io

# Set filter plugin environment variable.
set p="`./spack find --paths hdf5-hpc-io | tail  -1 | cut -d' ' -f 3-`"
setenv HDF5_PLUGIN_PATH $p/lib/plugin/

# Show installed plugin.
ls $p/lib/plugin/


