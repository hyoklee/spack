# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Spdk(AutotoolsPackage):
    """The Storage Performance Development Kit (SPDK) provides a set of tools
    and libraries for writing high performance, scalable, user-mode storage
    applications. It achieves high performance by moving all of the
    necessary drivers into userspace and operating in a polled mode instead
    of relying on interrupts, which avoids kernel context switches and
    eliminates interrupt handling overhead.
    """

    homepage = "https://spdk.io"
    url = "https://github.com/spdk/spdk/archive/v23.01.tar.gz"
    git = "https://github.com/spdk/spdk"
    maintainers("hyoklee")

    version("master", branch="master", submodules=True)
    version("23.01", tag="v23.01", submodules=True)

    variant("crypto", default=False, description="Build vbdev crypto module")
    variant("dpdk", default=False, description="Build with dpdk")
    variant("fio", default=False, description="Build fio plugin")
    variant("iscsi-initiator", default=False, description="Build with iscsi bdev module")
    variant("ocf", default=False, description="Build OCF library and bdev module")
    variant("pmdk", default=False, description="Build persistent memory bdev")
    variant("rbd", default=False, description="Build Ceph RBD bdev module")
    variant(
        "rdma", default=False, description="Build RDMA transport for NVMf target and initiator"
    )
    variant("shared", default=False, description="Build spdk shared libraries")
    variant("uring", default=False, description="Build I/O uring bdev")
    variant(
        "virtio", default=False, description="Build vhost initiator and virtio-pci bdev modules"
    )
    variant("vhost", default=False, description="Build vhost target")
    variant("vtune", default=False, description="Profile I/O under Intel VTune Amplifier XE")

    mods = (
        "crypto",
        "dpdk",
        "iscsi-initiator",
        "ocf",
        "pmdk",
        "rbd",
        "rdma",
        "shared",
        "uring",
        "vhost",
        "virtio",
        "vtune",
    )

    depends_on("dpdk@22.11:", when="+dpdk")
    depends_on("fio@3.3", when="+fio")
    depends_on("libaio")
    depends_on("meson")
    depends_on("nasm@2.12.02:", type="build")
    depends_on("numactl")
    depends_on("py-pyelftools")
    depends_on("rdma-core", when="+rdma")

    def configure_args(self):
        spec = self.spec
        config_args = ["--disable-tests", "--disable-unit-tests", "--disable-apps"]

        if "+fio" in spec:
            config_args.append("--with-fio={0}".format(spec["fio"].prefix))

        for mod in self.mods:
            if "+" + mod in spec:
                config_args.append("--with-{0}".format(mod))
            else:
                config_args.append("--without-{0}".format(mod))

        return config_args

    @run_after("install")
    def install_additional_files(self):
        prefix = self.prefix

        dpdk_build_dir = join_path(self.stage.source_path, "dpdk", "build", "lib")
        mkdirs(dpdk_build_dir)
        mkdir(join_path(dpdk_build_dir, "pkgconfig"))
        install_tree(join_path(dpdk_build_dir, "pkgconfig"), join_path(prefix.lib, "pkgconfig"))
        for file in os.listdir(dpdk_build_dir):
            if os.path.isfile(join_path("dpdk", "build", "lib", file)):
                install(join_path("dpdk", "build", "lib", file), prefix.lib)
        mkdir(join_path(prefix.include, "dpdk"))
        install_tree("dpdk/build/include", join_path(prefix.include, "dpdk"))

        # Copy the config.h file, as some packages might require it.
        mkdir(prefix.share)
        mkdir(join_path(prefix.share, "spdk"))
        install_tree("examples/nvme/fio_plugin", join_path(prefix.share, "spdk", "fio_plugin"))
        install_tree("include", join_path(prefix.share, "spdk", "include"))
        install_tree("scripts", join_path(prefix.share, "spdk", "scripts"))
