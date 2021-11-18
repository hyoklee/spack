#!/bin/tcsh
./spack uninstall --all --force --yes-to-all hdf5-vfd-gds
rm -rf ~/.spack/cache
rm -rf /tmp/hyoklee

./spack install --test root hdf5-vfd-gds

source ../share/spack/setup-env.csh
spack load hdf5-vfd-gds

# Show installed library.
set p="`./spack find --paths hdf5-vfd-gds | tail  -1 | cut -d' ' -f 3-`"
ls $p/lib/
