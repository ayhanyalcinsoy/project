#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

# SyStem
import sys
import dbus

# Pds Stuff
import historymanager.context as ctx

# Application Stuff
import historymanager.about as about

# Qt Stuff
from PyQt5.QtCore import *



if __name__ == '__main__':

    # DBUS MainLoop
    if not dbus.get_default_main_loop():
        from dbus.mainloop.pyqt5 import DBusQtMainLoop
        DBusQtMainLoop(set_as_default = True)
        
    # Application Stuff
    from historymanager.window import MainManager

     # Pds Stuff
    from pds.quniqueapp import QUniqueApplication

    # Create a QUniqueApllication instance
    app = QUniqueApplication(sys.argv, catalog=about.appName)

     # Create Main Widget and make some settings
    mainWindow = MainManager(None, app= app)
    mainWindow.show()
    mainWindow.resize(640, 480)
    mainWindow.setWindowTitle(about.PACKAGE)

    # Create connection for lastWindowClosed signal to quit app
    app.connect(app, pyqtSignal('lastWindowClosed()'), app.quit)

    # Run the applications
    app.exec_()
