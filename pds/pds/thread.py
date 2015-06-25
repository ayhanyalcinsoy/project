#!/usr/bin/python
# -*- coding: utf-8 -*-

# Forked from Pardus
# PisiLinux Desktop Services
# Thread Module ~ thread.py

# Copyright (C) 2015, PisiLinux
# 2010 - Gökmen Göksel <gokmen:pardus.org.tr>
# 2015 - Ayhan Yalçınsoy <ayhanyalcinsoy:pisilinux.org>

# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.

from PyQt5.QtCore import QThread, pyqtSlot, pyqtSignal

class PThread(QThread):
    def __init__(self, parent, action, callback=None,
                 args=[], kwargs={}, exceptionHandler=None):
        QThread.__init__(self,parent)

        if callback:
            parent.connect(self, pyqtSignal("finished()"), callback)

        self.action = action
        self.args = args
        self.kwargs = kwargs
        self.exceptionHandler = exceptionHandler
        self.data = None

    def run(self):
        try:
            self.data = self.action(*self.args, **self.kwargs)
        except Exception as e:
            if self.exceptionHandler:
                self.exceptionHandler(e)
        finally:
            self.connect(self.parent(), pyqtSignal("cleanUp()"), pyqtSlot("deleteLater()"))

    def cleanUp(self):
        self.deleteLater()

    def get(self):
        return self.data

