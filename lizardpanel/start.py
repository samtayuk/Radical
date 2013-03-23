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
from auth import AuthController, require, member_of, name_is

from template import serve_template

class RestrictedArea:
    
    # all methods in this controller (and subcontrollers) is
    # open only to members of the admin group
    
    _cp_config = {
        'auth.require': [member_of('admin')]
    }
    
    @cherrypy.expose
    def index(self):
        return """This is the admin only area."""


class Root:
    
    _cp_config = {
        'tools.sessions.on': True,
        'tools.auth.on': True
    }
    
    auth = AuthController()
    
    restricted = RestrictedArea()
    
    @cherrypy.expose
    @require()
    def index(self):
        return """Index"""
    
    @cherrypy.expose
    def open(self):
        return """This page is open to everyone"""
    
    @cherrypy.expose
    @require(name_is("joe"))
    def only_for_joe(self):
        return """Hello Joe - this page is available to you only"""

    # This is only available if the user name is joe _and_ he's in group admin
    @cherrypy.expose
    @require(name_is("joe"))
    @require(member_of("admin"))   # equivalent: @require(name_is("joe"), member_of("admin"))
    def only_for_joe_admin(self):
        return """Hello Joe Admin - this page is available to you only"""


if __name__ == '__main__':

    conf = {
            '/interface':{
                'tools.staticdir.on': True,
                'tools.staticdir.dir': "/home/samtayuk/Projects/lizardpanel/data/interface"
            },
            '/bootstrap':{
                'tools.staticdir.on': True,
                'tools.staticdir.dir': "/home/samtayuk/Projects/lizardpanel/data/bootstrap"
            },
        }

    cherrypy.quickstart(Root(), '/', config=conf)