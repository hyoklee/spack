# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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
    # version("23.01", tag="v23.01", submodules=True)
    version("22.01.1", tag="v22.01.1", submodules=True)

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

    depends_on("libaio")
    # depends_on("dpdk@22.11:", when="+dpdk")
    depends_on("dpdk", when="+dpdk")
    # depends_on("dpdk@22.11.1", when="@22.01.1+dpdk")
    depends_on("dpdk@main", when="@22.01.1+dpdk")
    depends_on("fio@3.33", when="+fio")
    depends_on("libaio")
    depends_on("meson")
    depends_on("nasm@2.12.02:", type="build")
    depends_on("numactl")
    depends_on("py-pyelftools")
    depends_on("rdma-core", when="+rdma")

    patch(
        "https://github.com/spdk/spdk/commit/b0aba3fcd5aceceea530a702922153bc75664978.diff",
        when="@22.01.1",
        sha256="fe04d364928575397e7ca474ee1dfa32c1ff535b1f31b2deee8748e2a1b3355c",
    )

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

    # def install_dpdk_files(self):
    #     spec = self.spec
    #     prefix = self.prefix

    #     dpdk_build_dir = join_path(spec["dpdk"].prefix, "lib")

    #     install_tree(join_path(dpdk_build_dir, "pkgconfig"), join_path(prefix.lib, "pkgconfig"))

    #     for file in os.listdir(dpdk_build_dir):
    #         f = join_path(dpdk_build_dir, file)
    #         if os.path.isfile(f):
    #             install(f, prefix.lib)

    #     mkdir(join_path(prefix.include, "dpdk"))
    #     install_tree(join_path(spec["dpdk"].prefix, "include"),
    # join_path(prefix.include, "dpdk"))
    # @run_after("install")
    # def install_additional_files(self):
    #     spec = self.spec
    #     prefix = self.prefix
    #     if "+dpdk" in spec:
    #         self.install_dpdk_files()
    #     # Copy the config.h file, as some packages might require it.
    #     mkdir(prefix.share)
    #     mkdir(join_path(prefix.share, "spdk"))
    #     install_tree("examples/nvme/fio_plugin", join_path(prefix.share, "spdk", "fio_plugin"))
    #     install_tree("include", join_path(prefix.share, "spdk", "include"))
    #     install_tree("scripts", join_path(prefix.share, "spdk", "scripts"))
