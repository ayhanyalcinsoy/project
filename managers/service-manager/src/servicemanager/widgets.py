#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Forked from Pardus Service Manager
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

# Qt Stuff
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

# Pds
import servicemanager.context as ctx
from servicemanager.context import i18n

# Application Stuff
from servicemanager.ui_item import Ui_ServiceItemWidget
from servicemanager.ui_info import Ui_InfoWidget

# PDS Stuff
from pds.gui import *
from pds.qprogressindicator import QProgressIndicator

# Python Stuff
import time
import textwrap
import locale

# Pisi Stuff
import pisi

class ServiceItem(QListWidgetItem):

    def __init__(self, package, parent):
        QListWidgetItem.__init__(self, parent)

        self.package = package

class ServiceItemWidget(QWidget):

    def __init__(self, package, parent, item):
        QWidget.__init__(self, None)

        self.ui = Ui_ServiceItemWidget()
        self.ui.setupUi(self)

        self.busy = QProgressIndicator(self)
        self.busy.setMinimumSize(QSize(32, 32))
        self.ui.mainLayout.insertWidget(0, self.busy)
        self.ui.spacer.hide()
        self.busy.hide()

        self.ui.labelName.setText(package)

        self.toggleButtons()

        self.ui.buttonStart.setIcon(QIcon("media-playback-start"))
        self.ui.buttonStop.setIcon(QIcon("media-playback-stop"))
        self.ui.buttonReload.setIcon(QIcon("view-refresh"))
        self.ui.buttonInfo.setIcon(QIcon("dialog-information"))

        self.toggled = False
        self.root = parent
        self.iface = parent.iface
        self.item = item
        self.package = package
        self.info = ServiceItemInfo(self)

        self.type = None
        self.desc = None
        self.connect(self.ui.buttonStart, pyqtSignal("clicked()"), self.setService)
        self.connect(self.ui.buttonStop, pyqtSignal("clicked()"), self.setService)
        self.connect(self.ui.buttonReload, pyqtSignal("clicked()"), self.setService)
        self.connect(self.ui.checkStart, pyqtSignal("clicked()"), self.setService)
        self.connect(self.ui.buttonInfo, pyqtSignal("clicked()"), self.info.showDescription)

    def updateService(self, data, firstRun):
        self.type, self.desc, serviceState = data
        self.setState(serviceState, firstRun)
        self.ui.labelDesc.setText(self.desc)

    def setState(self, state, firstRun=False):
        if not firstRun:
            # There is a raise condition, FIXME in System.Service
            time.sleep(1)
            state = self.iface.info(self.package)[2]
        if state in ('on', 'started', 'conditional_started'):
            self.running = True
            icon = 'flag-green'
        else:
            self.running = False
            icon = 'flag-black'

        self.ui.buttonStop.setEnabled(self.running)
        self.ui.buttonReload.setEnabled(self.running)

        self.ui.labelStatus.setPixmap(QIcon(icon).pixmap(32, 32))
        self.showStatus()
        self.runningAtStart = False
        if state in ('on', 'stopped'):
            self.runningAtStart = True
        elif state in ('off', 'started', 'conditional_started'):
            self.runningAtStart = False
        self.ui.checkStart.setChecked(self.runningAtStart)
        self._last_state = self.ui.checkStart.isChecked()
        # print self.package, state

    def setService(self):
        try:
            self.showBusy()
            self._last_state = not self.ui.checkStart.isChecked()
            if self.sender() == self.ui.buttonStart:
                self.iface.start(self.package)
            elif self.sender() == self.ui.buttonStop:
                self.iface.stop(self.package)
            elif self.sender() == self.ui.buttonReload:
                self.iface.restart(self.package)
            elif self.sender() == self.ui.checkStart:
                self.iface.setEnable(self.package, self.ui.checkStart.isChecked())
        except Exception as msg:
            self.showStatus()
            self.root.showFail(msg)

    def switchToOld(self):
        self.ui.checkStart.setChecked(self._last_state)

    def showStatus(self):
        self.busy.hide()
        self.ui.spacer.hide()
        self.ui.labelStatus.show()

    def showBusy(self):
        self.busy.busy()
        self.ui.spacer.show()
        self.ui.labelStatus.hide()

    def enterEvent(self, event):
        if not self.toggled:
            self.toggleButtons(True)
            self.toggled = True

    def leaveEvent(self, event):
        if self.toggled:
            self.toggleButtons()
            self.toggled = False

    def toggleButtons(self, toggle=False):
        self.ui.buttonStart.setVisible(toggle)
        self.ui.buttonReload.setVisible(toggle)
        self.ui.buttonStop.setVisible(toggle)
        self.ui.buttonInfo.setVisible(toggle)
        self.ui.checkStart.setVisible(toggle)

def getDescription(service):
    try:
        # TODO add a package map for known services
        service = service.replace('_','-')
        lang = str(locale.getdefaultlocale()[0].split("_")[0])
        desc = pisi.api.info_name(service)[0].package.description
        if desc.has_key(lang):
            return desc[lang]
        return desc['en']
    except Exception as msg:
        # print "ERROR:", msg
        return i18n('Service information is not available')

class ServiceItemInfo(PAbstractBox):

    def __init__(self, parent):
        PAbstractBox.__init__(self, parent)

        self.ui = Ui_InfoWidget()
        self.ui.setupUi(self)
        self.ui.buttonHide.clicked.connect(self.hideDescription)
        self.ui.buttonHide.setIcon(QIcon("dialog-close"))

        self._animation = 2
        self._duration = 500

        self.enableOverlay()
        self.hide()

    def showDescription(self):
        self.resize(self.parentWidget().size())
        desc = getDescription(self.parentWidget().package)
        self.ui.description.setText(desc)
        self.ui.description.setToolTip('\n'.join(textwrap.wrap(desc)))
        self.animate(start = MIDLEFT, stop = MIDCENTER)
        qApp.processEvents()

    def hideDescription(self):
        if self.isVisible():
            self.animate(start = MIDCENTER,
                         stop  = MIDRIGHT,
                         direction = OUT)

