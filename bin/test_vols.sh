#!/bin/tcsh
set list = (async cache external-passthrough tests)
foreach a ($list)
    echo "Testing $a"
    ./spack uninstall --all --force --yes-to-all hdf5-vol-$a
    rm -rf ~/.spack/cache
    rm -rf /tmp/hyoklee
    ./spack install hdf5-vol-$a

    source ../share/spack/setup-env.csh
    spack load hdf5-vol-$a

    # Set VOL plugin environment variable.
    set p="`./spack find --paths hdf5-vol-$a | tail  -1 | cut -d' ' -f 3-`"
    setenv HDF5_PLUGIN_PATH $p/lib/
    switch ($a)
    case 'async':
        setenv HDF5_VOL_CONNECTOR "async under_vol=0;under_info={}"
        breaksw
    case 'cache':
        setenv HDF5_VOL_CONNECTOR "cache_ext config=config1.dat;under_vol=0;under_info={};"
        breaksw
    case 'external-passthrough'
        setenv HDF5_VOL_CONNECTOR "pass_through_ext under_vol=0;under_info={};"
        breaksw
    default:
        echo "$a is not supported."
        breaksw
    endsw

    # Show installed plugin.
    ls $p/lib/

    # Show installed header.
    ls $p/include/

end








