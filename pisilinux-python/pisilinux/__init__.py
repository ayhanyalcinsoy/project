#-*- coding: utf-8 -*-
#
# Forked from Pardus by TUBITAK/UEKAE
# Copyright (C) 2012-2015, PisiLinux
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

__version__ = "0.4.8"

__all__ = ["csapi",
           "deviceutils",
           "diskutils",
           "fileutils",
           "fstabutils",
           "grubutils",
           "iniutils",
           "localedata",
           "netutils",
           "netfilterutils",
           "shellutils",
           "strutils",
           "sysutils",
           "xorg"]


def versionString():
    return __version__

