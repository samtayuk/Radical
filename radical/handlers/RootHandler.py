# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
# This file is part of LizardPanel
### BEGIN LICENSE
# Copyright (C) 2013 Samuel Taylor <samtaylor.uk@gmail.com>
# This program is free software: you can redistribute it and/or modify it 
# under the terms of the GNU General Public License version 3, as published 
# by the Free Software Foundation.
# 
# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranties of 
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR 
# PURPOSE.  See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along 
# with this program.  If not, see <http://www.gnu.org/licenses/>.
### END LICENSE

import os
import sys

import cherrypy
from radical.auth import AuthController, require, member_of, name_is

from MemberManagerHandler import MemberManagerHandler
from ProfileHandler import ProfileHandler
from BoxManagerHandler import BoxManagerHandler
from GroupManagerHandler import GroupManagerHandler

from radical.handlers import Settings

from radical.database.Member import Member

from radical.lib.tool import template

class RootHandler:
    
    _cp_config = {
        'tools.sessions.on': True,
        'tools.auth.on': True,
    }
    
    auth = AuthController()
    member = MemberManagerHandler()
    box = BoxManagerHandler()
    profile = ProfileHandler()
    group = GroupManagerHandler()
    settings = Settings()
    
    @cherrypy.expose
    @require()
    @cherrypy.tools.mako(filename="index.html")
    def index(self):
        return {'title': 'Radical'}

    @cherrypy.expose
    @cherrypy.tools.mako(filename="wizard.html")
    def wizard(self, firstName=None, lastName=None, email=None, password=None, passwordConfirm=None):
        if firstName == None or lastName == None or email == None or password == None or passwordConfirm == None:
            return {}

        if not password == passwordConfirm:
            return {'msg':"Error: The passwords do not match."}

        db = cherrypy.request.db
        m = Member(email, password, firstName, lastName, True, "admin", "")

        db.add(m)
        db.commit()

        raise cherrypy.HTTPRedirect("/")

