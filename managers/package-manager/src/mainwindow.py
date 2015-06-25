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

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from ui_mainwindow import Ui_MainWindow

from mainwidget import MainWidget
from pdswidgets import PMessageBox
from statemanager import StateManager
from settingsdialog import SettingsDialog

from pds.qprogressindicator import QProgressIndicator
from tray import Tray
from pmutils import *

import backend
import config
import helpdialog
import localedata
import os
import pds

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, app = None):
        QMainWindow.__init__(self, None)
        self.setupUi(self)

        self.app = app
        self.iface = backend.pm.Iface()

        self.busy = QProgressIndicator(self)
        self.busy.setFixedSize(QSize(20, 20))

        self.setWindowIcon(QIcon(":/data/package-manager.png"))

        self.setCentralWidget(MainWidget(self))
        self.cw = self.centralWidget()

        self.settingsDialog = SettingsDialog(self)

        self.initializeActions()
        self.initializeStatusBar()
        self.initializeTray()
        self.connectMainSignals()

        self.pdsMessageBox = PMessageBox(self)

    def connectMainSignals(self):
        self.cw.connectMainSignals()
        self.connect(QShortcut(QKeySequence(Qt.CTRL + Qt.Key_Tab),self),
                pyqtSignal("activated()"), lambda: self.moveTab('next'))
        self.connect(QShortcut(QKeySequence(Qt.SHIFT + Qt.CTRL + Qt.Key_Tab),self),
                pyqtSignal("activated()"), lambda: self.moveTab('prev'))
        self.connect(QShortcut(QKeySequence(Qt.CTRL + Qt.Key_F),self),
                pyqtSignal("activated()"), self.cw.searchLine.setFocus)
        self.connect(QShortcut(QKeySequence(Qt.Key_F3),self),
                pyqtSignal("activated()"), self.cw.searchLine.setFocus)

        self.connect(self.settingsDialog, pyqtSignal("packagesChanged()"), self.cw.initialize)
        self.connect(self.settingsDialog, pyqtSignal("packageViewChanged()"), self.cw.updateSettings)
        self.connect(self.settingsDialog, pyqtSignal("traySettingChanged()"), self.tray.settingsChanged)
        self.connect(self.cw.state, pyqtSignal("repositoriesChanged()"), self.tray.populateRepositoryMenu)
        self.connect(self.cw, pyqtSignal("repositoriesUpdated()"), self.tray.updateTrayUnread)
        self.connect(qApp, pyqtSignal("shutDown()"), self.slotQuit)

    def moveTab(self, direction):
        new_index = self.cw.stateTab.currentIndex() - 1
        if direction == 'next':
            new_index = self.cw.stateTab.currentIndex() + 1
        if new_index not in range(self.cw.stateTab.count()):
            new_index = 0
        self.cw.stateTab.setCurrentIndex(new_index)

    def initializeTray(self):
        self.tray = Tray(self, self.iface)
        self.connect(self.cw.operation, pyqtSignal("finished(QString)"), self.trayAction)
        self.connect(self.cw.operation, pyqtSignal("finished(QString)"), self.tray.stop)
        self.connect(self.cw.operation, pyqtSignal("operationCancelled()"), self.tray.stop)
        self.connect(self.cw.operation, pyqtSignal("started(QString)"), self.tray.animate)
        self.connect(self.tray, pyqtSignal("showUpdatesSelected()"), self.trayShowUpdates)

    def trayShowUpdates(self):
        self.showUpgradeAction.setChecked(True)

        self.cw.switchState(StateManager.UPGRADE)

        QGuiApplication.applicationName(self).updateUserTimestamp()

        self.show()
        self.raise_()

    def trayAction(self, operation):
        if not self.isVisible() and operation in ["System.Manager.updateRepository", "System.Manager.updateAllRepositories"]:
            self.tray.showPopup()
        if self.tray.isVisible() and operation in ["System.Manager.updatePackage",
                                                   "System.Manager.installPackage",
                                                   "System.Manager.removePackage"]:
            self.tray.updateTrayUnread()

    def initializeStatusBar(self):
        self.cw.mainLayout.insertWidget(0, self.busy)
        self.statusBar().addPermanentWidget(self.cw.actions, 1)
        self.statusBar().show()

        self.updateStatusBar('')

        self.connect(self.cw, pyqtSignal("selectionStatusChanged(QString)"), self.updateStatusBar)
        self.connect(self.cw, pyqtSignal("updatingStatus()"), self.statusWaiting)

    def initializeActions(self):
        self.initializeOperationActions()

    def initializeOperationActions(self):

        self.showAllAction = QAction(QIcon(("applications-other", "package_applications")), i18n("All Packages"), self)
        self.connect(self.showAllAction, pyqtSignal("triggered()"), lambda:self.cw.switchState(StateManager.ALL))
        self.cw.stateTab.addTab(QWidget(), QIcon(("applications-other", "package_applications")), i18n("All Packages"))

        self.showInstallAction = QAction(QIcon(("list-add", "add")), i18n("Installable Packages"), self)
        self.connect(self.showInstallAction, pyqtSignal("triggered()"), lambda:self.cw.switchState(StateManager.INSTALL))
        self.cw.stateTab.addTab(QWidget(), QIcon(("list-add", "add")), i18n("Installable Packages"))

        self.showRemoveAction = QAction(QIcon(("list-remove", "remove")), i18n("Installed Packages"), self)
        self.connect(self.showRemoveAction, pyqtSignal("triggered()"), lambda:self.cw.switchState(StateManager.REMOVE))
        self.cw.stateTab.addTab(QWidget(), QIcon(("list-remove", "remove")), i18n("Installed Packages"))

        self.showUpgradeAction = QAction(QIcon(("system-software-update", "gear")), i18n("Updates"), self)
        self.connect(self.showUpgradeAction, pyqtSignal("triggered()"), lambda:self.cw.switchState(StateManager.UPGRADE))
        self.cw.stateTab.addTab(QWidget(), QIcon(("system-software-update", "gear")), i18n("Updates"))

        self.showPreferences = QAction(QIcon(("preferences-system", "package_settings")), i18n("Settings"), self)
        self.connect(self.showPreferences, pyqtSignal("triggered()"), self.settingsDialog.show)

        self.actionHelp = QAction(QIcon("help"), i18n("Help"), self)
        self.actionHelp.setShortcuts(QKeySequence.HelpContents)
        self.connect(self.actionHelp, pyqtSignal("triggered()"), self.showHelp)

        self.actionQuit = QAction(QIcon("exit"), i18n("Quit"), self)
        self.actionQuit.setShortcuts(QKeySequence.Quit)
        self.connect(self.actionQuit, pyqtSignal("triggered()"), qApp.exit)

        self.cw.menuButton.setMenu(QMenu('MainMenu', self.cw.menuButton))
        self.cw.menuButton.setIcon(QIcon(("preferences-system", "package_settings")))
        self.cw.menuButton.menu().clear()

        self.cw.contentHistory.hide()

        self.cw.menuButton.menu().addAction(self.showPreferences)
        self.cw.menuButton.menu().addSeparator()
        self.cw.menuButton.menu().addAction(self.actionHelp)
        self.cw.menuButton.menu().addAction(self.actionQuit)

        self.cw._states = {self.cw.state.ALL    :(0, self.showAllAction),
                           self.cw.state.INSTALL:(1, self.showInstallAction),
                           self.cw.state.REMOVE :(2, self.showRemoveAction),
                           self.cw.state.UPGRADE:(3, self.showUpgradeAction)}

        self.showAllAction.setChecked(True)
        self.cw.checkUpdatesButton.hide()
        self.cw.checkUpdatesButton.setIcon(QIcon(("view-refresh", "reload")))
        self.cw.showBasketButton.clicked.connect(self.cw.showBasket)

        # Little time left for the new ui
        self.menuBar().setVisible(False)
        self.cw.switchState(self.cw.state.ALL)

    def statusWaiting(self):
        self.updateStatusBar(i18n('Calculating dependencies...'), busy = True)

    def showHelp(self):
        self.Pds = pds.Pds()
        self.lang = localedata.setSystemLocale(justGet = True)

        if self.lang in os.listdir("/usr/share/package-manager/help"):
            pass
        else:
            self.lang = "en"

        helpdialog.HelpDialog(self,helpdialog.MAINAPP)

    def updateStatusBar(self, text, busy = False):
        if text == '':
            text = i18n("Currently your basket is empty.")
            self.busy.hide()
            self.cw.showBasketButton.hide()
        else:
            self.cw.showBasketButton.show()

        if busy:
            self.busy.busy()
            self.cw.showBasketButton.hide()
        else:
            self.busy.hide()

        self.cw.statusLabel.setText(text)
        self.cw.statusLabel.setToolTip(text)

    def queryClose(self):
        if config.PMConfig().systemTray():
            self.hide()
            return False
        return True

    def queryExit(self):
        if not self.iface.operationInProgress():
            if self.tray:
                del self.tray.notification
            return True
        return False

    def slotQuit(self):
        if self.iface.operationInProgress():
            return
