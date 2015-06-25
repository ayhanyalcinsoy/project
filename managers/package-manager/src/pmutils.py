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

import os
import sys
import pisi
import comar
import urllib
import socket
import unicodedata
import traceback

import backend

from pmlogging import logger

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtNetwork import *

import pds

Pds = pds.Pds('package-manager', debug = False)
# Force to use Default Session for testing
# Pds.session = pds.DefaultDe
# print 'Current session is : %s %s' % (Pds.session.Name, Pds.session.Version)

i18n = Pds.session.i18n

class PM:

    def connectOperationSignals(self):
        # Basic connections
        self.connect(self.operation, pyqtSignal("exception(QString)"), self.exceptionCaught)
        self.connect(self.operation, pyqtSignal("finished(QString)"), self.actionFinished)
        self.connect(self.operation, pyqtSignal("started(QString)"), self.actionStarted)
        self.connect(self.operation, pyqtSignal("operationCancelled()"), self.actionCancelled)

        # ProgressDialog connections
        self.connect(self.operation, pyqtSignal("started(QString)"), self.progressDialog.updateActionLabel)
        self.connect(self.operation, pyqtSignal("progress(int)"), self.progressDialog.updateProgress)
        self.connect(self.operation, pyqtSignal("operationChanged(QString,QString)"), self.progressDialog.updateOperation)
        self.connect(self.operation, pyqtSignal("packageChanged(int, int, QString)"), self.progressDialog.updateStatus)
        self.connect(self.operation, pyqtSignal("elapsedTime(QString)"), self.progressDialog.updateRemainingTime)
        self.connect(self.operation, pyqtSignal("downloadInfoChanged(QString, QString, QString)"), self.progressDialog.updateCompletedInfo)

    def notifyFinished(self):
        if not self.operation.totalPackages:
            return
        Pds.notify(i18n('Package Manager'), self.state.getSummaryInfo(self.operation.totalPackages))

    def exceptionCaught(self, message, package = '', block = False):
        self.runPreExceptionMethods()

        if any(warning in message for warning in ('urlopen error','Socket Error', 'PYCURL ERROR')):
            errorTitle = i18n("Network Error")
            errorMessage = i18n("Please check your network connections and try again.")
        elif "Access denied" in message or "tr.org.pardus.comar.Comar.PolicyKit" in message:
            errorTitle = i18n("Authorization Error")
            errorMessage = i18n("You are not authorized for this operation.")
        elif "HTTP Error 404" in message and not package == '':
            errorTitle = i18n("Pisi Error")
            errorMessage = i18n("Package <b>%s</b> not found in repositories.<br>"\
                                        "It may be upgraded or removed from the repository.<br>"\
                                        "Please try upgrading repository informations.") % package
        elif "MIXING PACKAGES" in message:
            errorTitle = i18n("Pisi Error")
            errorMessage = i18n("Mixing file names and package names not supported yet.")
        elif "FILE NOT EXISTS" in message:
            errorTitle = i18n("Pisi Error")
            errorMessage = i18n("File <b>%s</b> doesn't exists.") % package
        elif "ALREADY RUNNING" in message:
            errorTitle = i18n("Pisi Error")
            errorMessage = i18n("Another instance of PiSi is running. Only one instance is allowed.")
        else:
            errorTitle = i18n("Pisi Error")
            errorMessage = message

        self.messageBox = QMessageBox(errorTitle, errorMessage, QMessageBox.Critical, QMessageBox.Ok, 0, 0)

        if block:
            self.messageBox.exec_()
            self.runPostExceptionMethods()
        else:
            QTimer.singleShot(0, self.messageBox.exec_)
            self.messageBox.buttonClicked(self.runPostExceptionMethods)

    def runPreExceptionMethods(self):
        if hasattr(self, '_preexceptions'):
            for method in self._preexceptions:
                method()

    def runPostExceptionMethods(self, *args):
        if hasattr(self, '_postexceptions'):
            for method in self._postexceptions:
                method()

def get_real_paths(packages):
    # If packages are not from repo or remote, find their absolute paths
    return map(lambda x: x if not x.endswith('.pisi') or '://' in x else os.path.abspath(x), packages)

def isAllLocal(packages):
    return all(map(lambda x: x.endswith('.pisi') and not '://' in x, packages))

def askForActions(packages, reason, title, details_title):
    msgbox = QMessageBox()
    msgbox.setText('<b>%s</b>' % reason)
    msgbox.setInformativeText(i18n("Do you want to continue ?"))
    msgbox.setDetailedText(details_title + '\n' + '-'*60 + '\n  - ' + '\n  - '.join(packages))
    msgbox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    return msgbox.exec_() == QMessageBox.Yes

def waitCursor():
    QGuiApplication.setOverrideCursor(Qt.WaitCursor)


def restoreCursor():
    # According to the Qt Documentation it should be called twice to reset
    # cursor to the default if one use waitCursor twice.
    QGuiApplication.restoreOverrideCursor()
    QGuiApplication.restoreOverrideCursor()

def processEvents():
    QGuiApplication.processEvents()

def set_proxy_settings():
    http = backend.pm.Iface().getConfig().get("general", "http_proxy")
    if http and not http == "None":
        items = parse_proxy(http)
        QNetworkProxy.setApplicationProxy(
                QNetworkProxy(QNetworkProxy.HttpProxy,
                            items['host'], int(items['port']),
                            items['user'] or '', items['pass'] or ''))

def reset_proxy_settings():
    QNetworkProxy.setApplicationProxy(QNetworkProxy())

def network_available():
    return pisi.fetcher.Fetcher('http://appinfo.pisilinux.org').test()

def parse_proxy(line):
    settings = {'domain':None,'user':None,'pass':None,'host':None,'port':None}

    if '://' in line:
        line = line.replace('%s://' % line.split('://')[0], '', 1)

    if '\\' in line:
        settings['domain'] = line.split('\\')[0]
        line = line.replace('%s\\' % settings['domain'], '', 1)

    if '@' in line:
        auth = line.split('@')[0]
        settings['user'], settings['pass'] = auth.split(':')
        line = line.replace('%s@' % auth, '', 1)

    if ':' in line:
        settings['host'], settings['port'] = line.split(':')

    return settings

def repos_available(iface, check_repos = None):
    repos = iface.getRepositories(only_active = True, repos = check_repos)
    if not repos:
        return False

    for name, address in repos:
        if not pisi.fetcher.Fetcher('%s.sha1sum' % address).test():
            return False

    return True

def isPisiRunning():
    link = comar.Link()
    return any(operation.startswith('System.Manager') for operation in link.listRunning())

def handleException(exception, value, tb):
    """
    Exception Handler

    @param exception: exception object
    @param value: exception message
    @param tb: traceback log
    """
    logger.error("".join(traceback.format_exception(exception, value, tb)))

def humanReadableSize(size, precision=".1"):
    if not size:
        return 'N/A'

    symbols, depth = [' B', 'kB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'], 0

    while size > 1000 and depth < 8:
        size = float(size / 1024)
        depth += 1

    if size == 0:
        return "0 B"

    fmt = "%%%sf %%s" % precision
    return fmt % (size, symbols[depth])

# Python regex sucks
# http://mail.python.org/pipermail/python-list/2009-January/523704.html
def letters():
    start = end = None
    result = []
    for index in range(sys.maxunicode + 1):
        c = unichr(index)
        if unicodedata.category(c)[0] == 'L':
            if start is None:
                start = end = c
            else:
                end = c
        elif start:
            if start == end:
                result.append(start)
            else:
                result.append(start + "-" + end)
            start = None
    return ''.join(result)
