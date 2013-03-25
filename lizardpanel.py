#!/usr/bin/python
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
import cherrypy

from lizardpanel.handlers.RootHandler import RootHandler
from lizardpanel.handlers import ErrorHandlers

if __name__ == '__main__':

    conf = {
            '/interface':{
                'tools.staticdir.on': True,
                'tools.staticdir.dir': os.path.join(os.path.abspath(__file__), 'data', 'interface')
            },
            '/bootstrap':{
                'tools.staticdir.on': True,
                'tools.staticdir.dir': os.path.join(os.path.abspath(__file__), 'data', 'bootstrap')
            },
        }

    cherrypy.config.update({'error_page.404': ErrorHandlers.error_page_404, 'error_page.401': ErrorHandlers.error_page_401})
    cherrypy.quickstart(RootHandler(), '/', config=conf)
