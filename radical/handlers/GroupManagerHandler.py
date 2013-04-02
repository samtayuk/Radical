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

import cherrypy

from radical.auth import AuthController, require, member_of, name_is
from radical.lib.tool import template

from radical.database import Group

class GroupManagerHandler:
    
    # all methods in this controller (and subcontrollers) is
    # open only to members of the admin group
    
    _cp_config = {
        'auth.require': [member_of('admin')]
    }
    
    
    @cherrypy.expose
    @cherrypy.tools.mako(filename="group.html")
    def index(self):
    	groups = cherrypy.request.db.query(Group).all()

        return {'title':"Radical", 'groups':groups}

    @cherrypy.expose
    @cherrypy.tools.mako(filename="editgroup.html")
    def add(self, groupName=None, groupDescription=None):
    	if not groupName == None:
    		g = Group(groupName, 1)
    		cherrypy.request.db.add(g)
    		cherrypy.request.db.commit()
    		raise cherrypy.HTTPRedirect("/group")

    	return {'title':"Radical", 'pageTitle': "Create Group"}
