#!/usr/bin/python3
#-*- coding: utf-8 -*-

# Forked from Pardus by TUBITAK/UEKAE
# Copyright (C) 2012-2015, PisiLinux
# 2015 - Ayhan Yalçınsoy

import os
import os.path
import sys
import glob
import shutil
from distutils.core import setup, Extension
from distutils.command.install import install

import pisilinux

distfiles = """
    setup.py
    pisilinux/*.py
    pisilinux/*.c
    pisilinux/xorg/*.py
    pisilinux/xorg/*.c
    po/*.po
    po/*.pot
    tools/*.py
    tools/*.sh
    MODULES
    README
"""

def make_dist():
    distdir = "pisilinux-python-%s" % pisilinux.versionString()
    list = []
    for t in distfiles.split():
        list.extend(glob.glob(t))
    if os.path.exists(distdir):
        shutil.rmtree(distdir)
    os.mkdir(distdir)
    for file_ in list:
        cum = distdir[:]
        for d in os.path.dirname(file_).split('/'):
            dn = os.path.join(cum, d)
            cum = dn[:]
            if not os.path.exists(dn):
                os.mkdir(dn)
        shutil.copy(file_, os.path.join(distdir, file_))
    os.popen("tar -czf %s %s" % ("pisilinux-python-" + pisilinux.versionString() + ".tar.gz", distdir))
    shutil.rmtree(distdir)

if "dist" in sys.argv:
    make_dist()
    sys.exit(0)

class Install(install):
    def finalize_options(self):
        # NOTE: for Pisilinux distribution
        if os.path.exists("/etc/pisilinux-release"):
            self.install_platlib = '$base/lib/pisilinux'
            self.install_purelib = '$base/lib/pisilinux'
        install.finalize_options(self)

    def run(self):
        install.run(self)
        self.installi18n()

    def installi18n(self):
        for name in os.listdir('po'):
            if not name.endswith('.po'):
                continue
            lang = name[:-3]
            print("Installing '%s' translations...") % lang
            os.popen("msgfmt po/%s.po -o po/%s.mo" % (lang, lang))
            if not self.root:
                self.root = "/"
            destpath = os.path.join(self.root, "usr/share/locale/%s/LC_MESSAGES" % lang)
            if not os.path.exists(destpath):
                os.makedirs(destpath)
            shutil.copy("po/%s.mo" % lang, os.path.join(destpath, "pisilinux-python.mo"))

setup(name="pisilinux",
      version=pisilinux.versionString(),
      description="Python Modules for Pisilinux",
      long_description="Python Modules for Pisilinux.",
      license="GNU GPL2",
      author="Pisilinux Developers",
      author_email="admin@pisilinux.org",
      url="http://www.pisilinux.org/",
      packages = ['pisilinux', 'pisilinux.xorg'],
      ext_modules = [Extension('pisilinux.xorg.capslock',
                               sources=['pisilinux/xorg/capslock.c'],
                               libraries=['X11']),
                     Extension('pisilinux.csapi',
                               sources=['pisilinux/csapi.c'],
                               libraries=[]),
                    ],
      cmdclass = {'install' : Install})
