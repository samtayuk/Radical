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

from radical.auth import require, member_of

from radical.database import Box
from radical.lib.tool import template

class BoxManagerHandler:
    
    # all methods in this controller (and subcontrollers) is
    # open only to members of the admin group
    
    _cp_config = {
        'auth.require': [member_of('admin')]
    }
    
    @cherrypy.expose
    @cherrypy.tools.mako(filename="box.html")
    def index(self):
        boxes = cherrypy.request.db.query(Box).all()
        return {'title':"Radical", 'boxes':boxes}

    @cherrypy.expose
    @cherrypy.tools.mako(filename="editbox.html")
    def add(self, name=None, ip=None, ssh_user=None, ssh_password=None, ssh_port=None, notes=None):
        if name == None and ip == None and ssh_user == None and ssh_password == None and ssh_port == None and notes == None:
            return {'title':"Radical", 'pageTitle':"Add Box"}
        else:
            b = Box(name, ip, ssh_user, ssh_password, ssh_port, notes)

            cherrypy.request.db.add(b)
            cherrypy.request.db.commit()

            raise cherrypy.HTTPRedirect("/box")
