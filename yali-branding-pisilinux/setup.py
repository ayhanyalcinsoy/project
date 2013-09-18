#!/usr/bin/env python
#
# Copyright (C) 2010 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.

import os
import glob
from distutils.core import setup
from distutils.cmd import Command
from distutils.command.build import build
from distutils.command.install import install

BRANDING_DIR = "usr/share/yali/branding/pisilinux"
IN_FILES = ("release.xml.in",)

class Build(build):
    def run(self):
        build.run(self)

        self.mkpath(self.build_base)

        for in_file in IN_FILES:
            name, ext = os.path.splitext(in_file)
            self.spawn(["intltool-merge", "-x", "po", in_file, os.path.join(self.build_base, name)])


class Install(install):
    def run(self):
        install.run(self)

        self.copy_file("build/release.xml", os.path.join(self.root or "/", BRANDING_DIR))


class UpdatePO(Command):
    description = "Update po files"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.chdir("po")
        self.spawn(["intltool-update", "--gettext-package=yali-branding-pisilinux", "-p"])
        for po_file in glob.glob("*.po"):
            lang, ext = os.path.splitext(po_file)
            self.spawn(["intltool-update", "--gettext-package=yali-branding-pisilinux", "--dist", "-o", po_file, lang])

        os.chdir("..")

setup(name="yali-branding-pisilinux",
      version= "0.2",
      description="Pisi Linux branding files for YALI (Yet Another Linux Installer)",
      license="Latest GNU GPL version",
      author="Pisi Linux Developers",
      author_email="admin@pisilinux.org",
      url="https://github.com/pisilinux/project/tree/master/yali-branding-pisilinux",
      data_files=[("/%s/slideshow" % BRANDING_DIR, glob.glob("slideshow/*.png"))],
      cmdclass = {'build': Build,
                  'install': Install,
                  'update_po': UpdatePO})
