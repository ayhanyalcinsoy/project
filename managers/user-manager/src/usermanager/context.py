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
import pds
import traceback
from time import time
from pds.qiconloader import QIconLoader

#Load PyQt libraries
from PyQt5.QtWidgets import *

Pds = pds.Pds('user-manager', debug = True)
# Force to use Default Session for testing
#Pds.session = pds.DefaultDe
print('Current session is : %s %s') % (Pds.session.Name, Pds.session.Version)

i18n = Pds.i18n

time_counter = 0
start_time = time()
last_time = time()


def _time():
    global last_time, time_counter
    trace = list(traceback.extract_stack())
    diff = time() - start_time
    print('%s ::: %s:%s' % (time_counter, trace[-2][0].split('/')[-1], trace[-2][1])), diff, diff - last_time
    last_time = diff
    time_counter += 1
def askForActions(packages, reason, title, details_title):
    msgbox = QMessageBox()
    msgbox.setText('<b>%s</b>' % reason)
    msgbox.setInformativeText(i18n("Do you want to continue ?"))
    msgbox.setDetailedText(details_title + '\n' + '-'*60 + '\n  - ' + '\n  - '.join(packages))
    msgbox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    return msgbox.exec_() == QMessageBox.Yes
