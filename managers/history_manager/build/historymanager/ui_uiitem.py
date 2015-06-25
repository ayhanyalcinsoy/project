# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/uiitem.ui'
#
# Created: Wed Jun 24 12:13:22 2015
#      by: PyQt4 UI code generator 4.9.6
#
# WARNING! All changes made in this file will be lost!

import gettext
__trans = gettext.translation('history-manager', fallback=True)
i18n = __trans.ugettext
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QGuiApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QGuiApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QGuiApplication.translate(context, text, disambig)

class Ui_HistoryItemWidget(object):
    def setupUi(self, HistoryItemWidget):
        HistoryItemWidget.setObjectName(_fromUtf8("HistoryItemWidget"))
        HistoryItemWidget.resize(661, 48)
        HistoryItemWidget.setMinimumSize(QtCore.QSize(0, 48))
        HistoryItemWidget.setWindowTitle(_fromUtf8("Form"))
        self.gridLayout_3 = QtGui.QGridLayout(HistoryItemWidget)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.iconLabel = QtGui.QLabel(HistoryItemWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.iconLabel.sizePolicy().hasHeightForWidth())
        self.iconLabel.setSizePolicy(sizePolicy)
        self.iconLabel.setMinimumSize(QtCore.QSize(36, 0))
        self.iconLabel.setText(_fromUtf8(""))
        self.iconLabel.setPixmap(QtGui.QPixmap(_fromUtf8("../../service-manager/manager/ui/icons/stopped.png")))
        self.iconLabel.setObjectName(_fromUtf8("iconLabel"))
        self.gridLayout_2.addWidget(self.iconLabel, 0, 0, 2, 1)
        self.labelLabel = QtGui.QLabel(HistoryItemWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.labelLabel.setFont(font)
        self.labelLabel.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.labelLabel.setObjectName(_fromUtf8("labelLabel"))
        self.gridLayout_2.addWidget(self.labelLabel, 0, 1, 1, 1)
        self.typeLabel = QtGui.QLabel(HistoryItemWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.typeLabel.sizePolicy().hasHeightForWidth())
        self.typeLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.typeLabel.setFont(font)
        self.typeLabel.setStyleSheet(_fromUtf8("color:gray;"))
        self.typeLabel.setObjectName(_fromUtf8("typeLabel"))
        self.gridLayout_2.addWidget(self.typeLabel, 1, 1, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_2, 0, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(50, 20, QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem, 0, 1, 1, 1)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.restorePB = QtGui.QPushButton(HistoryItemWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.restorePB.sizePolicy().hasHeightForWidth())
        self.restorePB.setSizePolicy(sizePolicy)
        self.restorePB.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/dotakeback.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.restorePB.setIcon(icon)
        self.restorePB.setObjectName(_fromUtf8("restorePB"))
        self.gridLayout.addWidget(self.restorePB, 0, 2, 1, 1)
        self.detailsPB = QtGui.QPushButton(HistoryItemWidget)
        self.detailsPB.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/details.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.detailsPB.setIcon(icon1)
        self.detailsPB.setObjectName(_fromUtf8("detailsPB"))
        self.gridLayout.addWidget(self.detailsPB, 0, 0, 1, 1)
        self.planPB = QtGui.QPushButton(HistoryItemWidget)
        self.planPB.setText(_fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/plan.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.planPB.setIcon(icon2)
        self.planPB.setObjectName(_fromUtf8("planPB"))
        self.gridLayout.addWidget(self.planPB, 0, 1, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout, 0, 2, 1, 1)

        self.retranslateUi(HistoryItemWidget)
        QtCore.QMetaObject.connectSlotsByName(HistoryItemWidget)

    def retranslateUi(self, HistoryItemWidget):
        self.labelLabel.setText(i18n("History Date - Time /Label"))
        self.typeLabel.setText(i18n("No: Type:"))
        self.restorePB.setToolTip(i18n("Take back to this point"))
        self.detailsPB.setToolTip(i18n("Details"))
        self.planPB.setToolTip(i18n("Show operation plan"))

import data_rc
