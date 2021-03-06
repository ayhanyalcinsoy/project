#!/usr/bin/python
# -*- coding: utf-8 -*-

# Pisi Desktop Services
# Forked from Pardus Desktop Services
# Copyright (C) 2015, PisiLinux
# 2010 - Gökmen Göksel <gokmen:pardus.org.tr>
# 2015 - Muhammet Dilmaç <iletisim@muhammetdilmac.com.tr>
# 2015 - Ayhan Yalçınsoy<ayhanyalcinsoy@pisilinux.org>

# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.

class DefaultDe(object):
    Name                 = 'X11'
    SessionTypes         = ()
    Version              = None
    VersionKey           = None
    ConfigPath           = '$HOME/.config'
    ConfigFile           = None
    ConfigType           = None
    ConfigBin            = None
    DefaultIconTheme     = 'hicolor'
    DefaultIconFile      = ''
    DefaultConfigPath    = None
    ExtraDirs            = None
    IconKey              = None
    i18n                 = staticmethod(lambda x: x)

class Kde4(DefaultDe):
    Name                 = 'kde'
    SessionTypes         = ('kde-plasma')
    Version              = '4'
    VersionKey           = 'KDE_SESSION_VERSION'
    ConfigPath           = ('$HOME/.kde4/', '$HOME/.kde/')
    ConfigFile           = 'share/config/kdeglobals'
    ConfigType           = 'ini'
    ConfigBin            = 'kde4-config'
    DefaultIconFile      = '/usr/share/icons/default.kde4'
    DefaultIconTheme     = 'oxygen'
    IconKey              = 'Icons/Theme'
    try:
        from PyKDE4 import kdecore, kdeui
        i18n                 = kdecore.i18n
    except:
        pass

class Kde3(DefaultDe):
    Name                 = 'kde'
    Version              = '3.5'
    ConfigPath           = '$HOME/.kde/'
    ConfigFile           = 'share/config/kdeglobals'
    ConfigType           = 'ini'
    ConfigBin            = 'kde-config'
    DefaultIconFile      = '/usr/share/icons/default.kde'
    DefaultIconTheme     = 'crystalsvg'
    IconKey              = 'Icons/Theme'
    ExtraDirs            = 'KDEDIRS'

class Xfce(DefaultDe):
    Name                 = 'xfce'
    Version              = '4'
    ConfigPath           = '$HOME/.config/xfce4/'
    ConfigFile           = 'xfconf/xfce-perchannel-xml/xsettings.xml'
    ConfigType           = 'xml'
    DefaultIconTheme     = 'Faenza'
    DefaultConfigPath    = '/etc/xdg/xfce4/%s' % ConfigFile
    IconKey              = 'IconThemeName'

class Enlightenment(DefaultDe):
    Name                 = 'enlightenment'
    Version              = '0.17'
    ConfigPath           = '$HOME/.e/e/'
    ConfigFile           = 'config/standard/e.cfg'
    ConfigType           = 'env'
    DefaultIconTheme     = 'Faenza'
    IconKey              = 'E_ICON_THEME'

class LxQt(DefaultDe):
    Name                 = 'LxQt'
    Version              = '0.5'
    ConfigPath           = '$HOME/.config'
    ConfigFile           = ''
    ConfigType           = None
    DefaultIconTheme     = 'Compass'
    IconKey              = 'theme/name'
    DefaultIconFile      = '/usr/share/lxqt/themes/Ambiance/mainmenu.svg'

class Fluxbox(DefaultDe):
    Name                 = 'fluxbox'
    Version              = '1.3.1'
    ConfigPath           = '$HOME/.config'
    ConfigFile           = ''
    ConfigType           = None
    DefaultIconTheme     = 'Faenza'

class Gnome(DefaultDe):
    Name                 = 'gnome'
    Version              = '2.32'
    ConfigPath           = '$HOME/.gnome2'
    ConfigFile           = ''
    ConfigType           = None
    DefaultIconTheme     = 'oxygen'


class Gnome3(DefaultDe):
    Name                 = 'gnome3'
    SessionTypes         = ('gnome-shell')
    Version              = '3.0'
    ConfigPath           = '$HOME/.gnome2'
    ConfigFile           = ''
    ConfigType           = None
    DefaultIconTheme     = 'oxygen'

class Mate(DefaultDe):
    Name                 = 'mate'
    Version              = '1.61'
    ConfigPath           = '$HOME/.config/mate'
    ConfigFile           = ''
    ConfigType           = None
    DefaultIconTheme     = 'matefaenza'
