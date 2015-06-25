#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Pisi Desktop Services
# Forked from Pardus Desktop Services
# Copyright (C) 2015, PisiLinux
# 2010 - Gökmen Göksel <gokmen:pardus.org.tr>
# 2015 - Muhammet Dilmaç <iletisim@muhammetdilmac.com.tr>
# 2015 - Ayhan Yalçınsoy<ayhanyalcinsoy@pisilinux.org>

#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.

import os
# Qt Libraries
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtXml import *
from PyQt5.Qt import *

#QX11EmbededContainer supported no more by qt5
class PApplicaitonContainer(QWidget):
    def __init__(self, parent = None, process = None, args = ()):
        QWidget.__init__(self, parent)

        self._label = None
        self._proc = None
        self._process = process
        self._args = args

    def start(self, process = None, args = ()):
        process = process or self._process
        args = args or self._args

        if not process:
            return (False, "Executable not given")

        self._process = process
        self._args = args

        self._proc = QProcess(self)
        self._proc.finished. connect(self._finished)
        self._proc.start(process, args)

        self.clientClosed.connect(self._proc.close)

        return (True, "'%s' process successfully started with pid = %s" % (process, self._proc.pid()))

    def closeEvent(self, event):
        if self.isRunning():
            self._proc.terminate()
            self._showMessage("Terminating process %s" % self._process)
            self._proc.waitForFinished()
        event.accept()

    def _finished(self, exitCode, exitStatus):
        self.emit(pyqtSignal("processFinished"), exitCode, exitStatus)
        if exitCode != 0:
            self._showMessage("%s process finished with code %s" % (self._process, exitCode))
        else:
            self.close()

    def _showMessage(self, message):
        if not self._label:
            self._label = QLabel(self)

        self._label.setText(message)
        self._label.show()

    def isRunning(self):
        if not self._proc:
            return False
        return not self._proc.state() == QProcess.NotRunning
