#!/usr/bin/python3
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

# PyQt
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

# UI
from usermanager.ui_question import Ui_DialogQuestion

#PDS

from context import *

class DialogQuestion(QDialog, Ui_DialogQuestion):
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        self.setupUi(self)

        self.pixmapIcon.setPixmap(QIcon("dialog-information").pixmap(48, 48))

    def setQuestion(self, question):
        self.labelQuestion.setText(question)

    def setCheckBox(self, message):
        self.checkBox.setText(message)

    def getCheckBox(self):
        return self.checkBox.checkState() == Qt.Checked
