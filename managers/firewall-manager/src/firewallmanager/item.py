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

# PyKDE
from context import *

# UI
from firewallmanager.ui_item import Ui_ItemWidget


class ItemListWidgetItem(QListWidgetItem):
    def __init__(self, parent, widget):
        QListWidgetItem.__init__(self, parent)
        self.widget = widget
        self.setSizeHint(QSize(300, 64))

    def getId(self):
        return self.widget.getId()

    def getType(self):
        return self.widget.getType()


class ItemWidget(QWidget, Ui_ItemWidget):
    def __init__(self, parent, id_, title="", description="", type_=None, icon=None, state=None):
        QWidget.__init__(self, parent)
        self.setupUi(self)

        self.id = id_
        self.type = type_

        self.setTitle(title)
        self.setDescription(description)

        if icon:
            self.setIcon(icon)
        else:
            self.labelIcon.hide()
        if state != None:
            self.setState(state)
        else:
            self.checkState.hide()

        # Buttons
        self.pushEdit.setIcon(QIcon("preferences-other"))
        self.pushDelete.setIcon(QIcon("edit-delete"))

        # Signals
        self.connect(self.checkState, pyqtSignal("stateChanged(int)"), lambda: self.emit(pyqtSignal("stateChanged(int)"), self.checkState.checkState()))
        self.connect(self.pushEdit, pyqtSignal("clicked()"), lambda: self.emit(pyqtSignal("editClicked()")))
        self.connect(self.pushDelete, pyqtSignal("clicked()"), lambda: self.emit(pyqtSignal("deleteClicked()")))

    def mouseDoubleClickEvent(self, event):
        self.pushEdit.animateClick(100)

    def getId(self):
        return self.id

    def getType(self):
        return self.type

    def setTitle(self, title):
        self.labelTitle.setText(title)

    def getTitle(self):
        return self.labelTitle.text()

    def setDescription(self, description):
        self.labelDescription.setText(description)

    def getDescription(self):
        return self.labelDescription.text()

    def setIcon(self, icon):
        self.labelIcon.setPixmap(icon.pixmap(32, 32))

    def getState(self):
        return self.checkState.checkState()

    def setState(self, state):
        if state == True:
            state = Qt.Checked
        elif state == False:
            state = Qt.Unchecked
        return self.checkState.setCheckState(state)

    def hideEdit(self):
        self.pushEdit.hide()

    def hideDelete(self):
        self.pushDelete.hide()
