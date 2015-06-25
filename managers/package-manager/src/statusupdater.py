#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Forked from Pardus Package Manager
# Copyright (C) 2012-2015, PisiLinux
# Gökmen Göksel
# Faik Uygur
# 2015 - Muhammet Dilmaç <iletisim@muhammetdilmac.com.tr>
# 2015 - Ayhan Yalçınsoy<ayhanyalcinsoy@pisilinux.org>
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

from PyQt5.QtCore import *
from pmutils import humanReadableSize as humanize

class StatusUpdater(QThread):
    def __init__(self):
        QThread.__init__(self)
        self.model = None
        self.needsUpdate = False
        self.calculate_deps = True

    def setModel(self, model):
        self.model = model

    def run(self):
        packages = len(self.model.selectedPackages())
        packagesSize = humanize(self.model.selectedPackagesSize())
        try:
            extraPackages = 0
            extraPackagesSize = ''
            if self.calculate_deps:
                extraPackages = len(self.model.extraPackages())
                extraPackagesSize = humanize(self.model.extraPackagesSize())
            self.emit(pyqtSignal("selectedInfoChanged(int, QString, int, QString)"), packages, packagesSize, extraPackages, extraPackagesSize)
        except Exception as e:
            self.emit(pyqtSignal("selectedInfoChanged(QString)"), e)

