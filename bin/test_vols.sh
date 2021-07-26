#!/bin/tcsh
# set list = (async cache external-passthrough log adios2 rest)
set list = (rest)
foreach a ($list)
    echo "Testing $a"
    ./spack uninstall --all --force --yes-to-all hdf5-vol-tests
    ./spack uninstall --all --force --yes-to-all hdf5-vol-$a
    rm -rf ~/.spack/cache
    rm -rf /tmp/hyoklee
    if ( $a == "adios2" ) then
        ./spack install --test root adios2+shared+hdf5 ^hdf5@1.12.1
    else
        ./spack install --test root hdf5-vol-$a
    endif
    source ../share/spack/setup-env.csh
    if ( $a == "adios2" ) then
        spack load adios2
    else
        spack load hdf5-vol-$a
    endif
    
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
    case 'log'
        setenv HDF5_VOL_CONNECTOR "LOG under_vol=0;under_info={};"
        breaksw
    case 'adios2'
        setenv HDF5_VOL_CONNECTOR "ADIOS2_VOL"
        breaksw
    case 'rest'
        setenv HDF5_VOL_CONNECTOR "REST"
        breaksw        
    default:
        echo "$a is not supported."
        breaksw
    endsw

    # Show installed plugin.
    ls $p/lib/

    # Show installed header.
    ls $p/include/
    ./spack install --test all hdf5-vol-tests+vol-$a 
end








