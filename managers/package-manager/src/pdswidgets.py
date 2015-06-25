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

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from pds.gui import *
from pds.qprogressindicator import QProgressIndicator
from ui_message import Ui_MessageBox
from pmutils import *

class PMessageBox(PAbstractBox):

    # STYLE SHEET
    STYLE = """color:white;font-size:16pt;"""
    OUT_POS  = MIDCENTER
    IN_POS   = MIDCENTER
    STOP_POS = MIDCENTER

    def __init__(self, parent):
        PAbstractBox.__init__(self, parent)
        self.ui = Ui_MessageBox()
        self.ui.setupUi(self)

        self.busy = QProgressIndicator(self, "white")
        self.busy.setMinimumSize(QSize(32, 32))
        self.busy.hide()
        self.ui.mainLayout.insertWidget(1, self.busy)

        self._animation = 2
        self._duration = 1
        self.last_msg = None
        self.setStyleSheet(PMessageBox.STYLE)
        self.enableOverlay()
        self.setOverlayOpacity(150)
        self.hide()

    def showMessage(self, message, icon = None, busy = False):
        self.ui.label.setText(message)

        if busy:
            self.busy.busy()
            self.ui.icon.hide()
        else:
            if icon:
                if type(icon) == str:
                    icon = QIcon(icon).pixmap(32,32)
                self.ui.icon.setPixmap(QPixmap(icon))
                self.ui.icon.show()
            else:
                self.ui.icon.hide()
            self.busy.hide()

        self.last_msg = self.animate(start = PMessageBox.IN_POS, stop = PMessageBox.STOP_POS)
        qApp.processEvents()

    def hideMessage(self, force = False):
        if self.isVisible() or force:
            self.animate(start = PMessageBox.STOP_POS,
                         stop  = PMessageBox.OUT_POS,
                         direction = OUT,
                         dont_animate = True)

