#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Forked from Pardus by TUBITAK/BILGEM
# Copyright (C) 2012 - 2015 PisiLinux
# Renan Çakırerk <renan at pardus.org.tr>
# 2015 - Ayhan Yalçınsoy
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Library General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#  (See COPYING)

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


from notifier_backend import PAbstractBox
from notifier_backend import OUT, TOPCENTER, MIDCENTER, CURRENT, OUT
from notifier_backend import QProgressIndicator

FORMAT_STARTED, FORMAT_SUCCESSFUL, FORMAT_FAILED, LOADING_DEVICES, NO_DEVICE, PARTITION_TABLE_ERROR = range(0,6)
ICON_ERROR = ":/images/images/dialog-error.png"
ICON_SUCCESS = ":/images/images/dialog-ok-apply.png" 

class Notifier(PAbstractBox):

    def __init__(self, parent):
        PAbstractBox.__init__(self, parent)

        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setObjectName("verticalLayout")

        spacerItem = QSpacerItem(20, 139, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(10)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)

        self.icon = QLabel(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(32)
        sizePolicy.setVerticalStretch(32)
        sizePolicy.setHeightForWidth(self.icon.sizePolicy().hasHeightForWidth())
        self.icon.setSizePolicy(sizePolicy)
        self.icon.setMinimumSize(QSize(32, 32))
        self.icon.setMaximumSize(QSize(32, 32))
        self.icon.setText("")
        self.icon.setPixmap(QPixmap(ICON_SUCCESS))
        self.icon.setAlignment(Qt.AlignCenter)
        self.icon.setObjectName("icon")
        self.horizontalLayout_2.addWidget(self.icon)


        self.busy = QProgressIndicator(self, "white")
        self.busy.setFixedSize(30, 30)
        self.horizontalLayout_2.addWidget(self.busy)

        self.label = QLabel(self)
        self.label.setText("                                 ")
        self.label.setMinimumHeight(30)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setAlignment(Qt.AlignCenter)
        # Word wrap
        self.label.setWordWrap(False)

        self.label.setIndent(0)

        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)

        spacerItem2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)

        self.okButton = QPushButton(self)
        self.okButton.setStyleSheet("color: #222222")
        self.okButton.setObjectName("okButton")
        self.okButton.setText(i18n("OK"))
        self.okButton.hide()

        self.horizontalLayout.addWidget(self.okButton)
        spacerItem4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem4)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem5 = QSpacerItem(20, 138, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem5)

        self._animation = 2
        self._duration = 500

        self.okButton.clicked.connect(self.hideBox)


    def hideBox(self):
        self.animate(start=MIDCENTER, stop=TOPCENTER, direction=OUT)
        self.okButton.hide()

    def set_message(self, message, button=False, indicator=False, icon=None):
        self.icon.setPixmap(QPixmap(icon))

        if message == '':
            self.label.hide()
        else:
            if icon:
                self.icon.show()
            else:
                self.icon.hide()

            if button:
                self.okButton.show()
            else:
                self.okButton.hide()

            if indicator:
                self.busy.show()
            else:
                self.busy.hide()

            self.label.setText(message)
            self.label.setAlignment(Qt.AlignCenter)

        self.label.adjustSize()
        self.adjustSize()

    def setIcon(self, icon=None):
        if not icon:
            self.icon.hide()
        else:
            self.icon.setPixmap(icon.pixmap(22, 22))
            self.icon.show()
        self.adjustSize()

    def notify(self, state):
        if state == FORMAT_STARTED:
            self.set_message(i18n("Please wait while formatting..."), indicator=True)

        elif state == FORMAT_SUCCESSFUL:
            self.set_message(i18n("Format completed successfully."), button=True, icon=ICON_SUCCESS)

        elif state == FORMAT_FAILED:
            self.set_message(i18n("Cannot format this partition.\nThe device might be in use.\nPlease try again."), button=True, icon=ICON_ERROR)

        elif state == NO_DEVICE:
            self.set_message(i18n("There aren't any removable devices."), icon=ICON_ERROR)

        elif state == LOADING_DEVICES:
            self.set_message(i18n("Loading devices..."), indicator=True)

        elif state == PARTITION_TABLE_ERROR:
            self.set_message(i18n("The partition table seems corrupt.\nPlease re-partition this device and try again."), button=True, icon=ICON_ERROR)


        self.animate(start=MIDCENTER, stop=MIDCENTER)


