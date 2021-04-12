#!/bin/tcsh
./spack uninstall --all --force --yes-to-all py-h5py
rm -rf ~/.spack/cache
rm -rf /var/folders/ff/*/T/hyoklee/spack-stage
./spack install py-h5py@master ^openblas@develop
./spack install py-pytest
./spack install py-ipython
./spack install py-pip
source ../share/spack/setup-env.csh
spack load py-h5py
spack load py-pytest
spack load py-ipython
spack load py-pip
pip install pytest-mpi
python -c "import h5py; h5py.run_tests(); print(h5py.version.info); "
