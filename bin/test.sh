# cd /scr/hyoklee/src/
# tar cvf hdf5_plugins.tar hdf5_plugins/*
# gzip hdf5_plugins.tar
# mv hdf5_plugins.tar.gz ../x/
# cd spack-hyoklee/bin/
rm -rf ~/.spack/cache
rm -rf /tmp/hyoklee
./spack uninstall --all --force --yes-to-all hdf5-cmake
./spack install hdf5-cmake
