#!/bin/tcsh
./spack uninstall --all --force --yes-to-all hdf5-hpc-io
rm -rf ~/.spack/cache
rm -rf /tmp/hyoklee

./spack install hdf5-hpc-io

source ../share/spack/setup-env.csh
spack load hdf5-hpc-io

# Show installed library.
set p="`./spack find --paths hdf5-hpc-io | tail  -1 | cut -d' ' -f 3-`"
ls $p/lib/



