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

# PyQt
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

# Settings item widget
from firewallmanager.settingsitem import SettingsItemWidget
#Context
from context import i18n
import context as ctx

# Config
from firewallmanager.config import ANIM_SHOW, ANIM_HIDE, ANIM_TARGET, ANIM_DEFAULT, ANIM_TIME


class PageDialog(QDialog):
    def __init__(self, parent, parameters, savedParameters):
        self.animationLast = ANIM_HIDE
        QDialog.__init__(self,parent)
        self.setWindowTitle(i18n("Settings"))
        self.resize(548,180)
        self.page_widget = PageWidget(self, parameters,savedParameters)
        self.tab=QTabWidget(self)
        self.tab.addTab(self.page_widget,i18n("Settings"))
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setGeometry(QRect(4, 152, 540, 25))
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.layout=QVBoxLayout(self)
        self.layout.addWidget(self.tab)
        self.layout.addWidget(self.buttonBox)
        self.buttonBox.setObjectName(i18n("buttonBox"))
        QObject.connect(self.buttonBox, pyqtSignal(i18n("accepted()")), self.accept)
        QObject.connect(self.buttonBox, pyqtSignal(i18n("rejected()")),self.reject)
        QMetaObject.connectSlotsByName(self, QObject)

    def getValues(self):
        return self.page_widget.getValues()

    def hideEditBox(self):
        if self.animationLast == ANIM_SHOW:
           self.animationLast = ANIM_HIDE
           # Set range
           self.animator.setFrameRange(self.frameEdit.height(), ANIM_TARGET)
           # Go go go!
           self.animator.start()

    def slotCancelEdit(self):
        self.hideEditBox()
        
    def slotSaveEdit(self):
     # Hide edit box
     self.hideEditBox()

class PageWidget(QWidget):
    def __init__(self, parent, parameters=[], saved={}):
        QWidget.__init__(self, parent)
        layout = QVBoxLayout(self)
        self.widgets = {}
        for name, label, type_, options in parameters:
            widget = SettingsItemWidget(self, name, type_)
            widget.setTitle(label)
            widget.setOptions(options)
            if name in saved:
                widget.setValue(saved[name])
            self.widgets[name] = widget
            layout.addWidget(widget)

        self.item = QSpacerItem(10, 10, QSizePolicy.Fixed, QSizePolicy.Expanding)
        layout.addSpacerItem(self.item)

    def getValues(self):
        values = {}
        for name, widget in self.widgets.iteritems():
            values[name] = widget.getValue()
        return values

