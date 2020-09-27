#! /usr/bin/env python
# coding=utf-8
#############################################################################
#                                                                           #
#   File: common.py                                                         #
#                                                                           #
#   Copyright (C) 2008 Du XiaoGang <dugang@188.com>                         #
#                                                                           #
#   Home: http://gappproxy.googlecode.com                                   #
#                                                                           #
#   This file is part of GAppProxy.                                         #
#                                                                           #
#   GAppProxy is free software: you can redistribute it and/or modify       #
#   it under the terms of the GNU General Public License as                 #
#   published by the Free Software Foundation, either version 3 of the      #
#   License, or (at your option) any later version.                         #
#                                                                           #
#   GAppProxy is distributed in the hope that it will be useful,            #
#   but WITHOUT ANY WARRANTY; without even the implied warranty of          #
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the           #
#   GNU General Public License for more details.                            #
#                                                                           #
#   You should have received a copy of the GNU General Public License       #
#   along with GAppProxy.  If not, see <http://www.gnu.org/licenses/>.      #
#                                                                           #
#############################################################################

LOAD_BALANCE = "http://gappproxy-center.appspot.com/available_fetchserver.py"
GOOGLE_PROXY = "www.google.cn:80"
DEF_LOCAL_PROXY = ""
DEF_FETCH_SERVER = "http://great-proxy.appspot.com"
DEF_LISTEN_PORT = 8000
DEF_CONF_FILE = "./proxy.conf"
DEF_COMM_FILE = "./.proxy.conf.tmp"


class GAppProxyError(Exception):
    def __init__(self, reason):
        self.reason = reason

    def __str__(self):
        return "<GAppProxy Error: %s>" % self.reason
