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

import backend

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from pmutils import *
from pds import QIconLoader
from statemanager import StateManager


class GroupList(QListWidget):
    def __init__(self, parent=None):
        QListWidget.__init__(self, parent)
        self.iface = backend.pm.Iface()
        self.defaultIcon = QIcon(('applications-other', 'unknown'), QIconLoader.SizeSmallMedium)
        self.connect(self, pyqtSignal("itemClicked(QListWidgetItem*)"),
                            self.groupChanged)
        self._list = {}

    def setState(self, state):
        self.state = state

    def addGroups(self, groups):
        if groups:
            for name in groups:
                self.createGroupItem(name)
        else:
            self.createGroupItem('all',
                    (i18n('All'), 'media-optical', len(self.state.packages())))
        self.sortItems()
        self.moveAllToFirstLine()
        self.setCurrentItem(self.item(0))

    def createGroupItem(self, name, content = None):
        if not content:
            group = self.iface.getGroup(name)
            localName, icon_path = group.localName, group.icon
            package_count = len(self.state.groupPackages(name))
            if package_count <= 0:
                return
        else:
            localName, icon_path = content[0], content[1]
            package_count = content[2]

        icon = QIcon(icon_path, QIconLoader.SizeSmallMedium)
        if icon.isNull():
            icon = self.defaultIcon
        text = "%s (%d)" % (localName, package_count)
        item = QListWidgetItem(icon, text, self)
        item.setToolTip(localName)
        item.setData(Qt.UserRole, QVariant(name))
        item.setSizeHint(QSize(0, QIconLoader.SizeMedium))
        self._list[name] = item

    def moveAllToFirstLine(self):
        if not self.count():
            return

        for i in range(self.count()):
            key = self.item(i).data(Qt.UserRole).toString()
            if key == "all":
                item = self.takeItem(i)
                self.insertItem(0, item)

    def currentGroup(self):
        if not self.count():
            return
        if self.currentItem():
            return self.currentItem().data(Qt.UserRole).toString()

    def groupChanged(self):
        self.emit(pyqtSignal("groupChanged()"))
