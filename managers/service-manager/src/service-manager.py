#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Forked from Pardus Package Manager
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

# System
import sys
import dbus

# Pds Stuff
import servicemanager.context as ctx

# Application Stuff
import servicemanager.about as about

# Qt Stuff
from PyQt5.QtCore import *
from PyQt5.QtGui import *


if __name__ == '__main__':

    # DBUS MainLoop
    if not dbus.get_default_main_loop():
        from dbus.mainloop.qt import DBusQtMainLoop
        DBusQtMainLoop(set_as_default = True)

    # Application Stuff
    from servicemanager.base import MainManager

    # Pds Stuff
    from pds.quniqueapp import QUniqueApplication
    from servicemanager.context import i18n

    # Create a QUniqueApllication instance
    app = QUniqueApplication(sys.argv, catalog=about.appName)

    # Create Main Widget and make some settings
    mainWindow = MainManager(None)
    mainWindow.show()
    mainWindow.resize(640, 480)
    mainWindow.setWindowTitle(i18n(about.PACKAGE))
    mainWindow.setWindowIcon(QIcon(about.icon))

    # Create connection for lastWindowClosed signal to quit app
    app.connect(app, pyqtSignal('lastWindowClosed()'), app.quit)

    # Run the applications
    app.exec_()
