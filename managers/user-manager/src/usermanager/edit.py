#!/usr/bin/python
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

# Python
import os

# PyQt
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

#PDS
from context import *

# UI
from usermanager.ui_edituser import Ui_EditUserWidget
from usermanager.ui_editgroup import Ui_EditGroupWidget

# Utilities
from usermanager.utility import nickGuess

# PolicyKit
import polkit

class PolicyItem(QTreeWidgetItem):
    def __init__(self, parent, text, action_id):
        QTreeWidgetItem.__init__(self, parent)
        self.action_id = action_id
        self.type = 0
        self.setText(0, text)
        self.setIcon(0,QIcon("security-medium"))

    def getAction(self):
        return self.action_id

    def setType(self, type_):
        self.type = type_
        if type_ == -1:
            self.setIcon(0,QIcon("security-low"))
        elif type_ == 0:
            self.setIcon(0,QIcon("security-medium"))
        elif type_ == 1:
            self.setIcon(0,QIcon("security-high"))

    def getType(self):
        return self.type


class EditUserWidget(QWidget, Ui_EditUserWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.setupUi(self)

        # List of unavailable nicks
        self.nicklist = []

        # Remove duplicate shells
        self.comboShell.setDuplicatesEnabled(False)

        # Build policy list
        self.buildPolicies()

        # Warning icon
        self.labelSign.setPixmap(QIcon("process-stop").pixmap(32, 32))
        self.labelSign.hide()

        # Signals
        self.connect(self.checkAutoId, pyqtSignal("stateChanged(int)"), self.slotCheckAuto)
        self.connect(self.lineUsername, pyqtSignal("textEdited(const QString&)"), self.slotUsernameChanged)
        self.connect(self.lineFullname, pyqtSignal("textEdited(const QString&)"), self.slotFullnameChanged)
        self.connect(self.listGroups, pyqtSignal("itemClicked(QListWidgetItem*)"), self.slotGroupSelected)
        self.connect(self.treeAuthorizations, pyqtSignal("currentItemChanged(QTreeWidgetItem*, QTreeWidgetItem*)"), self.slotPolicySelected)
        self.connect(self.radioAuthNo, pyqtSignal("toggled(bool)"), self.slotPolicyChanged)
        self.connect(self.radioAuthDefault, pyqtSignal("toggled(bool)"), self.slotPolicyChanged)
        self.connect(self.radioAuthYes, pyqtSignal("toggled(bool)"), self.slotPolicyChanged)
        self.connect(self.checkAdmin, pyqtSignal("stateChanged(int)"), self.slotAdmin)
        self.connect(self.pushAuth, pyqtSignal("clicked()"), self.slotAuth)

        self.connect(self.lineFullname, pyqtSignal("textEdited(const QString&)"), self.checkFields)
        self.connect(self.linePassword, pyqtSignal("textEdited(const QString&)"), self.checkFields)
        self.connect(self.linePasswordAgain, pyqtSignal("textEdited(const QString&)"), self.checkFields)
        self.connect(self.lineUsername, pyqtSignal("textEdited(const QString&)"), self.checkFields)
        self.connect(self.lineHomeDir, pyqtSignal("textEdited(const QString&)"), self.checkFields)

        #self.filterAuthorizations.setTreeWidget(self.treeAuthorizations)
        #self.filterGroups.setListWidget(self.listGroups)

        self.advancedGroup.hide()
        self.available_shells = []
        self._new = False

    def reset(self):
        self.wrn = ""
        self.setId(-1)
        self.setUsername("")
        self.setFullname("")
        self.setHomeDir("")
        self.setPassword()
        self.lineUsername.setEnabled(True)
        self.lineHomeDir.setEnabled(True)
        self.pushAdvanced.setChecked(False)
        self.labelWarning.setText("")
        self.labelSign.hide()
        self.advancedGroup.hide()
        self.comboShell.clear()
        self.comboShell.addItems(self.available_shells)
        self.emit(pyqtSignal("buttonStatusChanged(int)"),1)
        for index in xrange(self.treeAuthorizations.topLevelItemCount()):
            self.treeAuthorizations.collapseItem(self.treeAuthorizations.topLevelItem(index))

    def buildPolicies(self):
        self.actionItems = {}
        self._vendors = []

        categories = {"tr.org.pardus.comar.user.manager": (i18n("User/group operations"), "system-users"),
                      "tr.org.pardus.comar.system.manager": (i18n("Package operations"), "applications-other"),
                      "tr.org.pardus.comar.system.service": (i18n("Service operations"), "services"),
                      "tr.org.pardus.comar.time": (i18n("Date/time operations"), "clock"),
                      "tr.org.pardus.comar.boot.modules": (i18n("Kernel/Process operations"), "utilities-terminal"),
                      "tr.org.pardus.comar.boot.loader": (i18n("Bootloader settings"), "media-floppy")}

        # do not show policies require policy type yes or no, only the ones require auth_* type
        allActions = filter(lambda x: polkit.action_info(x)['policy_active'].startswith("auth_"),polkit.action_list())
        for _category in categories.keys():
            parent_item = QTreeWidgetItem(self.treeAuthorizations)
            parent_item.setIcon(0,QIcon(categories[_category][1]))
            parent_item.setText(0, categories[_category][0])
            for category in _category.split('|'):
                catactions = filter(lambda x: x.startswith(category), allActions)
                for action_id in catactions:
                    info = polkit.action_info(action_id)
                    item = PolicyItem(parent_item, info["description"], action_id)
                    self.actionItems[action_id] = item

    def getAuthorizations(self):
        grant = []
        revoke = []
        block = []
        for index in xrange(self.treeAuthorizations.topLevelItemCount()):
            tl_item = self.treeAuthorizations.topLevelItem(index)
            for child_index in xrange(tl_item.childCount()):
                item = tl_item.child(child_index)
                if item.getType() == -1:
                    block.append(item.getAction())
                elif item.getType() == 0:
                    revoke.append(item.getAction())
                elif item.getType() == 1:
                    grant.append(item.getAction())

        return grant, revoke, block

    def isNew(self):
        return self._new

    def getId(self):
        if self.checkAutoId.isChecked():
            return int(-1)
        return int(self.spinId.value())

    def setId(self, id):
        if id != -1:
            self.checkAutoId.setCheckState(Qt.Unchecked)
            self.checkAutoId.hide()
            self.spinId.setEnabled(False)
        else:
            self.checkAutoId.setCheckState(Qt.Checked)
            self.checkAutoId.show()
            self.spinId.setEnabled(False)
        self.spinId.setValue(id)

    def setNickList(self, nicklist):
        self.nicklist = nicklist

    def getUsername(self):
        return self.lineUsername.text()

    def setUsername(self, username):
        self.lineUsername.setText(username)
        self.lineUsername.setEnabled(False)

    def getFullname(self):
        return self.lineFullname.text()

    def setFullname(self, fullname):
        self.lineFullname.setText(fullname)

    def setHomeDir(self, homedir):
        self.lineHomeDir.setText(homedir)
        self.lineHomeDir.setEnabled(False)

    def getHomeDir(self):
        return self.lineHomeDir.text()

    def setShell(self, shell):
        shell_index = self.comboShell.findText(shell)
        if shell_index >= 0:
            self.comboShell.setCurrentIndex(shell_index)
        else:
            self.comboShell.insertItem(0, shell)
            self.comboShell.setCurrentIndex(0)

    def getShell(self):
        return str(self.comboShell.currentText())

    def setPassword(self):
        self.linePassword.setText("")
        self.linePasswordAgain.setText("")

    def getPassword(self):
        if self.linePassword.isModified() and self.linePassword.text() == self.linePasswordAgain.text():
            return self.linePassword.text()
        return ""

    def setGroups(self, all_groups, selected_groups):
        self.listGroups.clear()
        self.comboMainGroup.clear()
        for group in all_groups:
            # Groups
            item = QListWidgetItem(self.listGroups)
            item.setText(group)
            if group in selected_groups:
                item.setCheckState(Qt.Checked)
                # Add selected items to main group combo
                self.comboMainGroup.addItem(group)
                # Wheel group?
                if group == "wheel":
                    self.checkAdmin.setCheckState(Qt.Checked)
            else:
                item.setCheckState(Qt.Unchecked)
        # Select main group
        if selected_groups:
            self.comboMainGroup.setCurrentIndex(self.comboMainGroup.findText(selected_groups[0]))

    def getGroups(self):
        groups = []
        for index in range(self.listGroups.count()):
            item = self.listGroups.item(index)
            if item.checkState() == Qt.Checked:
                groups.append(item.text())
        # Main group
        main_group = self.comboMainGroup.currentText()
        groups.remove(main_group)
        groups.insert(0, main_group)
        return groups

    def setAuthorizations(self, authorizations):
        for action_id in self.actionItems:
            item = self.actionItems[action_id]
            item.setType(0)
        # print "\n Authorizations: %s " %authorizations
        for action_id, scope, description, policy_active, negative in authorizations:
            if action_id in self.actionItems:
                item = self.actionItems[action_id]
                if scope == negative:
                    item.setType(1)
                elif scope == polkit.SCOPE_ALWAYS:
                    item.setType(-1)
        self.slotPolicySelected(self.treeAuthorizations.currentItem())

    def slotCheckAuto(self, state):
        if state == Qt.Checked:
            self.spinId.setEnabled(False)
            self.spinId.setValue(-1)
        else:
            self.spinId.setEnabled(True)

    def slotAuth(self):
        if self.radioAuthNo.isChecked():
            type_ = -1
        elif self.radioAuthDefault.isChecked():
            type_ = 0
        elif self.radioAuthYes.isChecked():
            type_ = 1
        for index in xrange(self.treeAuthorizations.topLevelItemCount()):
            tl_item = self.treeAuthorizations.topLevelItem(index)
            for child_index in xrange(tl_item.childCount()):
                item = tl_item.child(child_index)
                item.setType(type_)

    def slotFullnameChanged(self, name):
        if self.lineUsername.isEnabled() and not self.lineUsername.isModified():
            self.lineUsername.setText(nickGuess(name, self.nicklist))
            if self.lineHomeDir.isEnabled() and not self.lineHomeDir.isModified():
                self.lineHomeDir.setText("/home/%s" % self.lineUsername.text())

    def slotUsernameChanged(self, name):
        if self.lineHomeDir.isEnabled() and not self.lineHomeDir.isModified():
            self.lineHomeDir.setText("/home/%s" % self.lineUsername.text())

    def checkLastItem(self):
        if self.comboMainGroup.count() == 1:
            QMessageBox.critical(self,"Error",i18n("There has to be at least one group selected"))
            return False
        return True

    def slotGroupSelected(self):
        item = self.listGroups.currentItem()
        if item.checkState() == Qt.Unchecked:
            # You can't remove last item
            if not self.checkLastItem():
                item.setCheckState(Qt.Checked)
                return
            # Remove from main group combo
            index = self.comboMainGroup.findText(item.text())
            self.comboMainGroup.removeItem(index)
            # Wheel group?
            if item.text() == "wheel":
                self.checkAdmin.setCheckState(Qt.Unchecked)
        else:
            # Add to main group combo
            self.comboMainGroup.addItem(item.text())
            # Wheel group?
            if item.text() == "wheel":
                self.checkAdmin.setCheckState(Qt.Checked)

    def slotPolicySelected(self, item, previous = None):
        if not item:
            return
        try:
            self.authGroup.setEnabled(True)
            self.radioAuthNo.setChecked(item.getType() == -1)
            self.radioAuthDefault.setChecked(item.getType() == 0)
            self.radioAuthYes.setChecked(item.getType() == 1)
        except:
            self.authGroup.setEnabled(False)

    def slotPolicyChanged(self, state):
        item = self.treeAuthorizations.currentItem()
        if self.radioAuthNo.isChecked():
            item.setType(-1)
        elif self.radioAuthDefault.isChecked():
            item.setType(0)
        elif self.radioAuthYes.isChecked():
            item.setType(1)

    def slotAdmin(self, state):
        if state == Qt.Unchecked:
            # You can't remove last item
            if not self.checkLastItem():
                self.checkAdmin.setCheckState(Qt.Checked)
                return
            # Remove from main group combo
            self.comboMainGroup.removeItem(self.comboMainGroup.findText("wheel"))
        else:
            # Add to combo
            if self.comboMainGroup.findText("wheel") < 0:
                self.comboMainGroup.addItem("wheel")
        # Update group list
        for index in range(self.listGroups.count()):
            item = self.listGroups.item(index)
            if item.text() == "wheel":
                # Change check state
                item.setCheckState(state)
                return

    def listShells(self):
        shells = open('/etc/shells').readlines()
        for shell in shells:
            if not shell.lstrip(' ').startswith('#'):
                shell = shell.rstrip('\n')
                if os.path.exists(shell):
                    self.available_shells.append(shell)

    def checkFields(self, *args):
        err = ""
        self.wrn = ""

        if self.lineFullname.text() == "" and self.lineUsername.text() == "" and self.isNew():
            err = i18n("Start with typing this user's full name.")

        if not err and self.isNew() and self.linePassword.text() == "":
            err = i18n("You should enter a password for this user.")

        if not err:
            pw = self.linePassword.text()

            # After removing the length check from COMAR backend we need to remove these
            if pw != "" and len(pw) < 4:
                self.wrn = i18n("Password must be longer.")

            if not err:
                if len(pw) and pw == self.lineFullname.text() or pw == self.lineUsername.text():
                    err = i18n("Don't use your full name or user name as a password.")

        if not err and self.linePassword.text() != self.linePasswordAgain.text():
            err = i18n("Passwords don't match.")

        nick = self.lineUsername.text()

        if not err and nick == "":
            err = i18n("You must enter a user name.")

        if not err and self.isNew() and nick in self.nicklist:
            err = i18n("This user name is used by another user.")

        if not err:
            if len(nick) > 0 and nick[0] >= "0" and nick[0] <= "9":
                err = i18n("User name must not start with a number.")

        if err:
            self.labelWarning.setText(u"<font color=red>%s</font>" % err)
            self.labelSign.show()
            self.emit(pyqtSignal("buttonStatusChanged(int)"),0)
        else:
            self.labelWarning.setText("")
            self.labelSign.hide()
            self.emit(pyqtSignal("buttonStatusChanged(int)"),1)
    def searchListWidget(self):
        srcList=self.filtergroups.text()
        for i in range(self.listGroups.count()):
            # for searching ListWidget item
            if self.listGroups.item(i).text().indexOf(srcList) == -1 :
                #print self.listGroups.item(i).text()
                self.listGroups.item(i).setHidden(True)
            else :
                self.listGroups.item(i).setHidden(False)
 
    def searchTreeListWidget(self):
        srcTreeList=str(self.filterAuthorizations.text()).lower()
        for i in range(self.treeAuthorizations.topLevelItemCount()):
            for j in range(self.treeAuthorizations.topLevelItem(i).childCount()):
               #print self.treeAuthorizations.topLevelItem(i).child(j).text(0)
               # for searching TreeListWidget root text and child text
               if (len([True for each in str(self.treeAuthorizations.topLevelItem(i).child(j).text(0)).lower().split(' ') if each.count(srcTreeList)>0])) or (len([True for each in str(self.treeAuthorizations.topLevelItem(i).text(0)).lower().split(' ') if each.count(srcTreeList)>0])):
                   self.treeAuthorizations.topLevelItem(i).setHidden(False)
               else:
                   self.treeAuthorizations.topLevelItem(i).setHidden(True)

class EditGroupWidget(QWidget, Ui_EditGroupWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.setupUi(self)

        self.connect(self.checkAutoId, pyqtSignal("stateChanged(int)"), self.slotCheckAuto)
        self.connect(self.lineGroupname, pyqtSignal("textEdited(const QString&)"), self.slotGroupnameChanged)

    def slotGroupnameChanged(self, name):
        self.emit(pyqtSignal("buttonStatusChanged(int)"),1)

    def reset(self):
        self.setId(-1)
        self.setGroupname("")

    def getId(self):
        if self.checkAutoId.checkState() == Qt.Checked:
            return -1
        return int(self.spinId.value())

    def setId(self, id):
        if id != -1:
            self.checkAutoId.setCheckState(Qt.Unchecked)
            self.checkAutoId.hide()
            self.spinId.setEnabled(False)
        else:
            self.checkAutoId.setCheckState(Qt.Checked)
            self.checkAutoId.show()
            self.spinId.setEnabled(False)
        self.spinId.setValue(id)

    def getGroupname(self):
        return self.lineGroupname.text()

    def setGroupname(self, groupname):
        self.lineGroupname.setText(groupname)

    def slotCheckAuto(self, state):
        if state == Qt.Checked:
            self.spinId.setEnabled(False)
            self.spinId.setValue(-1)
        else:
            self.spinId.setEnabled(True)

