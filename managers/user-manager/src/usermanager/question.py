#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Forked from Pardus User Manager
# Copyright (C) 2012-2015, PisiLinux
# Muhammet Dilmaç <iletisim@muhammetdilmac.com.tr>
# Ayhan Yalçınsoy<ayhanyalcinsoy@pisilinux.org>
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

# PyQt
from PyQt5 import QtCore
from PyQt5 import QtGui

# UI
from usermanager.ui_question import Ui_DialogQuestion

#PDS

from context import *

class DialogQuestion(QtGui.QDialog, Ui_DialogQuestion):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)

        self.pixmapIcon.setPixmap(KIcon("dialog-information").pixmap(48, 48))

    def setQuestion(self, question):
        self.labelQuestion.setText(question)

    def setCheckBox(self, message):
        self.checkBox.setText(message)

    def getCheckBox(self):
        return self.checkBox.checkState() == QtCore.Qt.Checked
