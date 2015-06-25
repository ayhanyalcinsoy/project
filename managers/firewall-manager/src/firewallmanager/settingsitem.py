#ifndef SETTINGSITEM.PY
#define SETTINGSITEM.PY
#!/usr/bin/python
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
from context import *

# UI
from firewallmanager.ui_settingsitem import Ui_SettingsItemWidget


class SettingsItemWidget(QWidget, Ui_SettingsItemWidget):
    def __init__(self, parent, name, type_):
        QWidget.__init__(self, parent)
        self.setupUi(self)

        self.name = name
        self.type = type_

        self.lineItem.hide()
        self.comboItems.hide()
        self.listItems.hide()
        self.setDisabledAll()
        if type_ == "combo":
            self.comboItems.show()
        elif type_ == "editlist":
            self.listItems.show()
        elif type_ == "text":
            self.lineItem.show()

        self.connect(self.pushAdd, pyqtSignal("clicked()"), self.addItemToList)
        self.connect(self.pushDelete, pyqtSignal("clicked()"), self.removeItemToList)
        self.connect(self.pushUp, pyqtSignal("clicked()"), self.funcpushUp)
        self.connect(self.pushDown, pyqtSignal("clicked()"), self.funcpushDown)
        QObject.connect(self.listWidget, pyqtSignal(("currentItemChanged(QListWidgetItem*,QListWidgetItem*)")), self.HideButtons)
        QObject.connect(self.lineEdit, pyqtSignal(("textChanged(QString)")), self.hideAdd)
        self.pushAdd.setIcon(QIcon("list-add"))
        self.pushDelete.setIcon(QIcon("list-remove"))
        self.pushUp.setIcon(QIcon("arrow-up"))
        self.pushDown.setIcon(QIcon("arrow-down"))

    def setDisabledAll(self):
        self.pushAdd.setEnabled(0)
        self.pushDelete.setEnabled(0)
        self.pushUp.setEnabled(0)
        self.pushDown.setEnabled(0)

    def hideAdd(self):
        if not(self.lineEdit.text()==""):
            self.pushAdd.setEnabled(1)
        else :
            self.pushAdd.setEnabled(0)

    def alreadyInList(self):
        for i in range(self.listWidget.count()):
            if (self.lineEdit.text()==self.listWidget.item(i).text()):
                return False 
        return True

    def addItemToList(self):
        if (self.alreadyInList()):
            if self.listWidget.currentItem():
                self.listWidget.currentItem().setText(self.lineEdit.text())
            else:
                if not(self.lineEdit.text()== ""):
                    self.listWidget.insertItem(0,self.lineEdit.text())
        self.lineEdit.setText("")
        self.listWidget.setCurrentItem(None)
        self.setDisabledAll()

    def removeItemToList(self):
        self.listWidget.takeItem(self.listWidget.currentRow())
        if (self.listWidget.count()==0):
            self.pushDelete.setEnabled(0)
        if (self.listWidget.count()<2):
            self.pushUp.setEnabled(0)
            self.pushDown.setEnabled(0)

    def listToLineEdit(self):
        if (self.listWidget.currentItem()):
            self.lineEdit.setText(self.listWidget.currentItem().text())
        else:
            self.lineEdit.setText("")

    def HideButtons(self):
        self.listToLineEdit()
        if not(self.lineEdit.text()==""):
            self.pushAdd.setEnabled(1)
        if self.listWidget.currentRow() == 0 :
            self.pushUp.setEnabled(0)
            self.pushDown.setEnabled(1)
        elif self.listWidget.currentRow() == self.listWidget.count()-1:
            self.pushUp.setEnabled(1)
            self.pushDown.setEnabled(0)
        else:
            self.pushDown.setEnabled(1)
            self.pushUp.setEnabled(1)
        if self.listWidget.currentRow :
            self.pushDelete.setEnabled(1)
        if (self.listWidget.count()<2):
            self.pushUp.setEnabled(0)
            self.pushDown.setEnabled(0)

    #TODO Create backend file for listWidget 
    def funcpushDown(self):
        self.listWidget.setCurrentRow(self.listWidget.currentRow()+1)
        degisken = self.listWidget.currentItem().text()
        self.listWidget.setCurrentRow(self.listWidget.currentRow()-1)
        degisken_ = self.listWidget.currentItem().text()
        self.listWidget.currentItem().setText(degisken)
        self.listWidget.setCurrentRow(self.listWidget.currentRow()+1)
        self.listWidget.currentItem().setText(degisken_)
        self.listToLineEdit()

    def funcpushUp(self):
        self.listWidget.setCurrentRow(self.listWidget.currentRow()-1)
        degisken = self.listWidget.currentItem().text()
        self.listWidget.setCurrentRow(self.listWidget.currentRow()+1)
        degisken_ = self.listWidget.currentItem().text()
        self.listWidget.currentItem().setText(degisken)
        self.listWidget.setCurrentRow(self.listWidget.currentRow()-1)
        self.listWidget.currentItem().setText(degisken_)
        self.listToLineEdit()
    def setTitle(self, title):
        self.labelTitle.setText(title)

    def setOptions(self, options):
        for key, value in options.iteritems():
            if key == "choose" and self.type == "combo":
                for item in value.split("\n"):
                    name, label = item.split("\t")
                    self.comboItems.addItem(label, QVariant(name))
            elif key == "format" and self.type in ["editlist", "text"]:
                editor = self.lineEdit
                validator = QRegExpValidator(QRegExp(value), self)
                editor.setValidator(validator)

    def setValue(self, value):
        value = value
        if self.type == "combo":
            index = self.comboItems.findData(QVariant(value))
            if index == -1:
                return
            self.comboItems.setCurrentIndex(index)
        elif self.type == "editlist":
            for item in value.split():
                self.listWidget.insertItem(0,item)
        elif self.type == "text":
            self.lineItem.setText(value)

    def getValue(self):
        if self.type == "combo":
            index = self.comboItems.currentIndex()
            return self.comboItems.itemData(index).toString()
        elif self.type == "editlist":
            items = []
            for index in range(self.listWidget.count()):
                items.append(self.listWidget.item(index).text())
            return " ".join(items)
        elif self.type == "text":
            return self.lineItem.text()
#endif // SETTINGSITEM.PY
