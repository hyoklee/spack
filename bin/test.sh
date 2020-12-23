#!/usr/bin/tcsh
# cd /scr/hyoklee/src/
# tar cvf hdf5_plugins.tar hdf5_plugins/*
# gzip hdf5_plugins.tar
# mv hdf5_plugins.tar.gz ../x/
# cd spack-hyoklee/bin/
rm -rf ~/.spack/cache
rm -rf /tmp/hyoklee
./spack uninstall --all --force --yes-to-all hdf5-cmake
./spack install hdf5-cmake~lzf~lz4
source ../share/spack/setup-env.csh
# For Bash
# . ../share/spack/setup-env.sh
spack load hdf5-cmake
# This will fail.
h5dump-shared /scr/hyoklee/data/test_zfp_be.h5
# Change install path.
setenv HDF5_PLUGIN_PATH /scr/hyoklee/src/spack-hyoklee/opt/spack/linux-centos7-haswell/gcc-4.8.5/hdf5-cmake-develop-uqtei4sbgqc33w5gmi6zfxmajxvyckm6/lib/plugin/

# These test will succeed.
h5dump-shared /scr/hyoklee/data/test_zfp_be.h5
h5dump-shared /scr/hyoklee/data/test_zfp_le.h5
h5dump-shared /scr/hyoklee/data/test_sz.h5
