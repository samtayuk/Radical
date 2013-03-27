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
from radical.helpers.template import serve_template

from radical.BoxFactory import BoxFactory

class BoxManagerHandler:
    
    # all methods in this controller (and subcontrollers) is
    # open only to members of the admin group
    
    _cp_config = {
        'auth.require': [member_of('admin')]
    }
    
    @cherrypy.expose
    def index(self):
        boxes = BoxFactory().get_all_boxes()
        return serve_template(templatename="box.html", title="Radical", boxes=boxes)

    @cherrypy.expose
    def add(self, name=None, ip=None, ssh_user=None, ssh_password=None, ssh_port=None, notes=None):
        if name == None and ip == None and ssh_user == None and ssh_password == None and ssh_port == None and notes == None:
            return serve_template(templatename="editbox.html", title="Radical", pageTitle="Add Box")
        else:
            b = BoxFactory().create_new_box(name, ip, ssh_user, ssh_password, ssh_port, notes)
            raise cherrypy.HTTPRedirect("/box")

