# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/configure.ui'
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
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Configure(object):
    def setupUi(self, Configure):
        Configure.setObjectName(_fromUtf8("Configure"))
        Configure.resize(227, 63)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/history-manager.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Configure.setWindowIcon(icon)
        self.gridLayout = QtGui.QGridLayout(Configure)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.maxHistoryLabel = QtGui.QLabel(Configure)
        self.maxHistoryLabel.setObjectName(_fromUtf8("maxHistoryLabel"))
        self.horizontalLayout.addWidget(self.maxHistoryLabel)
        self.maxHistorySB = QtGui.QSpinBox(Configure)
        self.maxHistorySB.setMaximum(15000)
        self.maxHistorySB.setSingleStep(25)
        self.maxHistorySB.setProperty("value", 200)
        self.maxHistorySB.setObjectName(_fromUtf8("maxHistorySB"))
        self.horizontalLayout.addWidget(self.maxHistorySB)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(Configure)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(Configure)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Configure.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Configure.reject)
        QtCore.QMetaObject.connectSlotsByName(Configure)

    def retranslateUi(self, Configure):
        Configure.setWindowTitle(i18n("Options"))
        self.maxHistoryLabel.setText(i18n("Startup Load :"))
        self.maxHistorySB.setSuffix(i18n(" Operations"))

import data_rc
