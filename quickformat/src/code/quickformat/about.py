#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Forked from Pardus by TUBITAK/BILGEM
# Copyright (C) 2012 - 2015 PisiLinux
# Renan Çakırerk <renan at pardus.org.tr>
# 2015 - Ayhan Yalçınsoy
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
# (See COPYING)


# Application Data
appName     = "quickformat"
programName = i18n("Quick Format")
version     = "1.0.0"
description = i18n("Removable Device Formatting Tool")
license     = GPL
copyright   = i18n("Pisilinux Community")
text        = i18n(None)
homePage    = "https://github.com/pisilinux/project"
bugEmail    = "admins@pisilinux.org"
catalog     = appName
aboutData   = KAboutData(appName, catalog, programName, version, description, license, copyright, text, homePage, bugEmail)

# Author(s)
aboutData.addAuthor(i18n("Renan Cakirerk"), i18n("Current Maintainer"))
