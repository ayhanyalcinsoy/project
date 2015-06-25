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

# Qt Stuff
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import packagemodel # roles needed

class PackageProxy(QSortFilterProxyModel):

    def __init__(self, parent=None):
        QSortFilterProxyModel.__init__(self, parent)
        self.__modelCache = {}
        self.__filteredPackages = set()

    def data(self, index, role):
        sourceIndex = self.mapToSource(index)
        if role != Qt.CheckStateRole and self.__modelCache.has_key(sourceIndex.row()) and self.__modelCache[sourceIndex.row()].has_key(role):
            v = self.__modelCache[sourceIndex.row()][role]
        else:
            v = self.sourceModel().data(self.mapToSource(index), role)
            if not self.__modelCache.has_key(sourceIndex.row()):
                self.__modelCache[sourceIndex.row()] = {}
            if not self.__modelCache[sourceIndex.row()].has_key(role):
                self.__modelCache[sourceIndex.row()][role] = v
        return v

    def setData(self, index, value, role):
        return self.sourceModel().setData(self.mapToSource(index), value, role)

    def filterAcceptsRow(self, source_row, source_parent):
        if self.filterRole() == packagemodel.GroupRole:
            sourceIndex = self.sourceModel().index(source_row, 0, source_parent)
            return sourceIndex.data(Qt.DisplayRole).toString() in self.__filteredPackages
        else:
            return QSortFilterProxyModel.filterAcceptsRow(self, source_row, source_parent)

    def getFilteredPackages(self):
        return list(self.__filteredPackages)

    def setFilterPackages(self, packages):
        self.__filteredPackages = set(packages)
        self.invalidateFilter()

    def reset(self):
        self.__modelCache = {}
        QSortFilterProxyModel.reset(self)

    def resetModelCache(self):
        self.sourceModel().initPhase()
