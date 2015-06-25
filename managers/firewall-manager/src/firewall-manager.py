#!/usr/bin/python3
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

#SyStem

import sys
import dbus

import firewallmanager.context as ctx
from firewallmanager.context import *

#Qt

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        widget = MainWidget(self)
        self.resize(widget.size())
        self.setCentralWidget(widget)
        self.qtrans=QTranslator()
if __name__ == "__main__":


    if not dbus.get_default_main_loop():
        from dbus.mainloop.qt import DBusQtMainLoop
        DBusQtMainLoop(set_as_default=True)

    import gettext
        
    __trans = gettext.translation('firewall-manager', fallback=True)
    i18n = __trans.ugettext

    from firewallmanager.main import MainWidget
    from pds.quniqueapp import QUniqueApplication

    app = QUniqueApplication(sys.argv, catalog="firewall-manager")

    mainWindow = MainWidget(None)
    mainWindow.show()
    mainWindow.resize(640, 480)
    mainWindow.setWindowTitle(i18n("Firewall Manager"))
    mainWindow.setWindowIcon(QIcon("security-high"))
    app.connect(app, pyqtSignal('lastWindowClosed()'), app.quit)
    app.exec_()

def CreatePlugin(widget_parent, parent, component_data):
    return Module(component_data, parent)
