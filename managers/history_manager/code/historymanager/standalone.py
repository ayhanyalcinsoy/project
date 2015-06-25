#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Forked from Pardus History Manager
# Copyright (C) 2012-2015, PisiLinux
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

# PyKDE4 Stuff
from PyKDE4.kdeui import *
from PyKDE4.kdecore import KGlobal

# Service Manager
from historymanager.window import MainManager


class HistoryManager(KMainWindow):
    def __init__(self):
        KMainWindow.__init__(self)
        self.setWindowIcon(KIcon("history-manager"))

        # This is very important for translations when running as kcm_module
        KGlobal.locale().insertCatalog("history-manager")

        self.resize(640, 480)
        self.setCentralWidget(MainManager(self))
