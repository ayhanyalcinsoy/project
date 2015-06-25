#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Forked from Pardus Firewall Manager
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

# PyQt
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

#Context
from context import i18n
# UI
from firewallmanager.ui_service import Ui_ServiceWidget


class ServiceWidget(QWidget, Ui_ServiceWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.state = False

        # Signals
        self.connect(self.pushToggle, pyqtSignal("clicked()"), lambda: self.emit(pyqtSignal("stateChanged(int)"), not self.getState()))

    def setState(self, state):
        self.state = state
        if state:
            self.labelStatus.setText(i18n("Firewall is activated."))
            self.labelIcon.setPixmap(QIcon("document-encrypt").pixmap(48, 48))
            self.pushToggle.setIcon(QIcon("media-playback-stop"))
            self.pushToggle.setText(i18n("Stop"))
        else:
            self.labelStatus.setText(i18n("Firewall is deactivated."))
            self.labelIcon.setPixmap(QIcon("document-decrypt").pixmap(48, 48))
            self.pushToggle.setIcon(QIcon("media-playback-start"))
            self.pushToggle.setText(i18n("Start"))

    def getState(self):
        return self.state

    def setEnabled(self, enabled):
        self.pushToggle.setEnabled(enabled)
