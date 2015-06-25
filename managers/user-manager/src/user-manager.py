#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Forked from Pardus User Manager
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

import sys
import dbus

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from usermanager.about import *
from usermanager.main import MainWidget

#PDS Stuff

import usermanager.context as ctx
from usermanager.context import *


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self,parent)
        widget = MainWidget(self)
        self.resize(widget.size())
        self.setCentralWidget(widget)


if __name__ == "__main__":
   
    #DBUS MainLoop
    if not dbus.get_default_main_loop():
        from dbus.mainloop.qt import DBusQtMainLoop
        DBusQtMainLoop(set_as_default = True)

    import gettext

    __trans=gettext.translation('user-manager',fallback=True)
    i18n=__trans.ugettext

    from pds.quniqueapp import QUniqueApplication
    app=QUniqueApplication(sys.argv, catalog='user-manager')
    window=MainWindow()
    window.show()
    window.resize(680,500)
    window.setWindowTitle(i18n('User Manager'))
    window.setWindowIcon(QIcon('computer'))
    app.exec_()
