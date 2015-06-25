#!/usr/bin/env python
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
# Please read the COPYING file

import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from ui_summarydialog import Ui_SummaryDialog
from ui_appitem import Ui_ApplicationItem
from pds import QIconLoader
from pmutils import *

import backend
import localedata
import desktopparser

class ApplicationItem(QListWidgetItem):
    def __init__(self, name, genericName, icon, command, parent=None):
        QListWidgetItem.__init__(self, parent)

        self.name = name
        self.genericName = genericName
        self.icon = icon
        self.command = command.split()[0]

class ApplicationItemWidget(QWidget, Ui_ApplicationItem):
    def __init__(self, item, parent=None):
        QListWidgetItem.__init__(self, parent)
        self.setupUi(self)
        self.item = item
        self.initialize()

    def initialize(self):
        self.appGenericName.setText(self.item.genericName)
        self.appName.setText(self.item.name)

        icon = str(self.item.icon).split('.')[:-1]
        icon = QIconLoader.load(icon)

        if icon.isNull():
            icon = QIconLoader.load('package')

        self.appIcon.setPixmap(
                               icon.scaled(QSize(32, 32),
                               Qt.KeepAspectRatio,
                               Qt.SmoothTransformation)
                              )

        self.appName.hide()

    def enterEvent(self, event):
        self.appName.show()

    def leaveEvent(self, event):
        self.appName.hide()

    def mouseDoubleClickEvent(self, event):
        os.popen('%s&' % self.item.command)

class SummaryDialog(QDialog, Ui_SummaryDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.iface = backend.pm.Iface()
        self.lang = localedata.setSystemLocale(justGet = True)
        self.closeButton.clicked.connect(self._reject)

    def setDesktopFiles(self, desktopFiles):
        self.appList.clear()
        for desktopFile in desktopFiles:
            self.addApplication(desktopFile)

    def checkIcon(self, iconFileName):
        extensions = ['png', 'jpg','jpeg', 'svg']
        pixmapsDir = '/usr/share/pixmaps/'
        if os.path.isfile(iconFileName) == True:
            return iconFileName
        else:
            for ext in extensions:
                fname = '%s%s.%s' % (pixmapsDir, iconFileName, ext)
                if os.path.isfile(fname):
                    return fname

    def addApplication(self, desktopFile):
        parser = desktopparser.DesktopParser()
        parser.read("/%s" % str(desktopFile))

        nodisplay = parser.safe_get_locale('Desktop Entry', 'NoDisplay', None)
        terminal = parser.safe_get_locale('Desktop Entry', 'Terminal', None)
        if nodisplay == "true" or terminal == "true":
            return

        icon = self.checkIcon(parser.safe_get_locale('Desktop Entry', 'Icon', None))
        command = parser.safe_get_locale('Desktop Entry', 'Exec', None)
        if not command:
            return
        name = parser.safe_get_locale('Desktop Entry', 'Name', self.lang)
        genericName = parser.safe_get_locale('Desktop Entry', 'GenericName', self.lang)
        if not genericName:
            genericName = name
            name = ""

        item = ApplicationItem(name, genericName, icon, command, self.appList)
        item.setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled)
        item.setSizeHint(QSize(0,48))
        itemWidget = ApplicationItemWidget(item, self)
        self.appList.setItemWidget(item, itemWidget)

    def hasApplication(self):
        return bool(self.appList.count())

    def closeEvent(self, event):
        self._reject()

    def _reject(self):
        self.reject()

    def showSummary(self):
        if self.hasApplication():
            self.show()

