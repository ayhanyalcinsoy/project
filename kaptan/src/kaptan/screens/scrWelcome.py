# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2009, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#


from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from kaptan.screen import Screen
from kaptan.screens.ui_scrWelcome import Ui_welcomeWidget
from kaptan.tools import tools

import subprocess

class Widget(QWidget, Screen):

    title = i18n("Welcome")
    desc = i18n("Welcome to %s")

    def __init__(self, *args):
        QWidget.__init__(self,None)
        self.ui = Ui_welcomeWidget()
        self.ui.setupUi(self)
        Widget.desc = QVariant(str(Widget.desc.toString()) % tools.getRelease())

    def shown(self):
        pass

    def execute(self):
        return True

