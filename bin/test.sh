rm -rf ~/.spack/cache
rm -rf /tmp/hyoklee
./spack uninstall --all hdf5-cmake
./spack install hdf5-cmake
