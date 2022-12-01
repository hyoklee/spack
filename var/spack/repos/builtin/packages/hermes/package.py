# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Hermes(CMakePackage):
    """
    Hermes is a heterogeneous-aware, multi-tiered, dynamic, and distributed
    I/O buffering system that aims to significantly accelerate I/O performance.
    """

    homepage = "http://www.cs.iit.edu/~scs/assets/projects/Hermes/Hermes.html"
    git = "https://github.com/hyoklee/hermes.git"

    maintainers = ["hyoklee"]

    version("master", branch="master")
    version(
        "0.9.0-beta",
        url="https://github.com/HDFGroup/hermes/archive/refs/tags/v0.9.0-beta.tar.gz",
        sha256="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    )

    variant("vfd", default=False, description="Enable HDF5 VFD")

    depends_on("mochi-thallium~cereal@0.8:")
    depends_on("catch2")
    depends_on("glpk")
    depends_on("glog@0.4.0:")
    depends_on("mpi")
    depends_on("hdf5@1.13.0:", when="+vfd")
    depends_on("yaml-cpp")

    def cmake_args(self):
        args = [
            self.define("HERMES_RPC_THALLIUM", True),
            self.define("HERMES_INSTALL_TESTS", True),
            self.define("BUILD_TESTING", True),
            self.define_from_variant("HERMES_ENABLE_VFD", "vfd"),
        ]
        return args
