# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyRetworkx(PythonPackage):
    """A high performance Python graph library implemented in Rust."""

    homepage = "https://github.com/Qiskit/retworkx"
    pypi = "retworkx/retworkx-0.5.0.tar.gz"

    version('0.10.2', sha256='ba81cb527de7ff338575905bb6fcbebdf2ab18ae800169a77ab863f855bf0951')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-setuptools-rust', type='build')
    depends_on('py-numpy@1.16.0:', type=('build', 'run'))
