# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/mainwindow.ui'
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

class Ui_MainManager(object):
    def setupUi(self, MainManager):
        MainManager.setObjectName(_fromUtf8("MainManager"))
        MainManager.resize(756, 722)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainManager.sizePolicy().hasHeightForWidth())
        MainManager.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/history-manager.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainManager.setWindowIcon(icon)
        self.gridLayout_3 = QtGui.QGridLayout(MainManager)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.newSnapshotPB = QtGui.QPushButton(MainManager)
        self.newSnapshotPB.setObjectName(_fromUtf8("newSnapshotPB"))
        self.gridLayout_3.addWidget(self.newSnapshotPB, 0, 0, 1, 1)
        self.configurePB = QtGui.QPushButton(MainManager)
        self.configurePB.setObjectName(_fromUtf8("configurePB"))
        self.gridLayout_3.addWidget(self.configurePB, 0, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(503, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem, 0, 2, 1, 1)
        self.lw = QtGui.QListWidget(MainManager)
        self.lw.setProperty("showDropIndicator", False)
        self.lw.setAlternatingRowColors(True)
        self.lw.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.lw.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.lw.setResizeMode(QtGui.QListView.Adjust)
        self.lw.setObjectName(_fromUtf8("lw"))
        self.gridLayout_3.addWidget(self.lw, 1, 0, 1, 3)
        self.editBox = QtGui.QScrollArea(MainManager)
        self.editBox.setFrameShape(QtGui.QFrame.NoFrame)
        self.editBox.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.editBox.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.editBox.setWidgetResizable(True)
        self.editBox.setObjectName(_fromUtf8("editBox"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 748, 326))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.gridLayout_2 = QtGui.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.editGroup = QtGui.QGroupBox(self.scrollAreaWidgetContents)
        self.editGroup.setTitle(_fromUtf8(""))
        self.editGroup.setObjectName(_fromUtf8("editGroup"))
        self.gridLayout = QtGui.QGridLayout(self.editGroup)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.aliasLabel = QtGui.QLabel(self.editGroup)
        self.aliasLabel.setObjectName(_fromUtf8("aliasLabel"))
        self.horizontalLayout.addWidget(self.aliasLabel)
        self.aliasLE = QtGui.QLineEdit(self.editGroup)
        self.aliasLE.setInputMask(_fromUtf8(""))
        self.aliasLE.setText(_fromUtf8(""))
        self.aliasLE.setMaxLength(30)
        self.aliasLE.setFrame(True)
        self.aliasLE.setObjectName(_fromUtf8("aliasLE"))
        self.horizontalLayout.addWidget(self.aliasLE)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.buttonCancelMini = QtGui.QPushButton(self.editGroup)
        self.buttonCancelMini.setMinimumSize(QtCore.QSize(22, 22))
        self.buttonCancelMini.setMaximumSize(QtCore.QSize(22, 22))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.buttonCancelMini.setFont(font)
        self.buttonCancelMini.setText(_fromUtf8("X"))
        self.buttonCancelMini.setObjectName(_fromUtf8("buttonCancelMini"))
        self.horizontalLayout.addWidget(self.buttonCancelMini)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.textEdit = QtGui.QTextEdit(self.editGroup)
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.gridLayout.addWidget(self.textEdit, 1, 0, 1, 1)
        self.gridLayout_2.addWidget(self.editGroup, 0, 0, 1, 1)
        self.editBox.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_3.addWidget(self.editBox, 2, 0, 1, 3)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        spacerItem2 = QtGui.QSpacerItem(298, 21, QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.opTypeLabel = QtGui.QLabel(MainManager)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.opTypeLabel.setFont(font)
        self.opTypeLabel.setAutoFillBackground(False)
        self.opTypeLabel.setFrameShadow(QtGui.QFrame.Plain)
        self.opTypeLabel.setTextFormat(QtCore.Qt.RichText)
        self.opTypeLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.opTypeLabel.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.opTypeLabel.setObjectName(_fromUtf8("opTypeLabel"))
        self.horizontalLayout_3.addWidget(self.opTypeLabel)
        self.progressBar = QtGui.QProgressBar(MainManager)
        self.progressBar.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.progressBar.sizePolicy().hasHeightForWidth())
        self.progressBar.setSizePolicy(sizePolicy)
        self.progressBar.setMaximumSize(QtCore.QSize(150, 16777215))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.horizontalLayout_3.addWidget(self.progressBar)
        self.gridLayout_3.addLayout(self.horizontalLayout_3, 3, 0, 1, 3)
        self.takeBackAction = QtGui.QAction(MainManager)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/dotakeback.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.takeBackAction.setIcon(icon1)
        self.takeBackAction.setObjectName(_fromUtf8("takeBackAction"))
        self.copyAction = QtGui.QAction(MainManager)
        self.copyAction.setObjectName(_fromUtf8("copyAction"))

        self.retranslateUi(MainManager)
        QtCore.QMetaObject.connectSlotsByName(MainManager)

    def retranslateUi(self, MainManager):
        MainManager.setWindowTitle(i18n("History Manager"))
        self.newSnapshotPB.setText(i18n("New Snapshot"))
        self.configurePB.setText(i18n("History Settings"))
        self.lw.setSortingEnabled(True)
        self.aliasLabel.setText(i18n("Alias :"))
        self.buttonCancelMini.setToolTip(i18n("Cancel"))
        self.opTypeLabel.setText(i18n("- Loading Pisi History"))
        self.progressBar.setFormat(i18n("%p%"))
        self.takeBackAction.setText(i18n("Take back to this point"))
        self.copyAction.setText(i18n("Copy"))

import data_rc
